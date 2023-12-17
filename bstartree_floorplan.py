import random
import math

class Block:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class BStarNode:
    def __init__(self, key, block):
        self.key = key
        self.block = block
        self.left = None
        self.right = None
        self.size =1

class BStarTree:
    def __init__(self, blocks):
        self.root = self.build_tree(blocks)

    def build_tree(self, blocks):
        if not blocks:
            return None

        blocks.sort(key=lambda x: x.width)
        mid = len(blocks) // 2
        node = BStarNode(blocks[mid].width, blocks[mid])

        node.left = self.build_tree(blocks[:mid])
        node.right = self.build_tree(blocks[mid + 1:])

        if node.left:
            node.size += node.left.size
        if node.right:
            node.size += node.right.size

        return node

    def find_block(self, key):
        return self._find_block(self.root, key)

    def _find_block(self, node, key):
        if node is None:
            return None

        if key == node.key:
            return node.block
        elif key < node.key:
            return self._find_block(node.left, key)
        else:
            return self._find_block(node.right, key)

class BStarFloorplan:
    def __init__(self, blocks):
        self.block_keys = list(range(len(blocks)))
        self.b_star_tree = BStarTree(blocks)
        self.positions = {}
        for key, block in zip(self.block_keys, blocks):
            # Initialize positions with random values
            self.positions[key] = (random.randint(0, outline_width), random.randint(0, outline_height))

    def perturb(self):
        # Randomly select two different block keys to swap
        block1_key, block2_key = random.sample(self.block_keys, 2)
    
        block1 = self.b_star_tree.find_block(block1_key)
        block2 = self.b_star_tree.find_block(block2_key)
    
        # Find the positions of the two blocks
        pos1 = self.get_block_position(block1_key)
        pos2 = self.get_block_position(block2_key)
    
        print(f"Swapping positions: Block1 {block1_key} -> {pos1}, Block2 {block2_key} -> {pos2}")
    
        # Swap the positions of the two blocks
        self.positions[block1_key] = pos2
        self.positions[block2_key] = pos1

    def get_block_position(self, block_key):
        return self.positions.get(block_key, (0, 0))

    def evaluate_cost(self):
        total_wirelength = 0

        for block1_key in self.positions:
            for block2_key in self.positions:
                if block1_key != block2_key:
                    total_wirelength += self.calculate_wirelength(block1_key, block2_key)

        return total_wirelength

    def calculate_wirelength(self, block1_key, block2_key):
        # Assuming each block has a position (x, y) within the outline
        x1, y1 = self.get_block_position(block1_key)
        x2, y2 = self.get_block_position(block2_key)

        # Calculate Manhattan distance
        wirelength = abs(x1 - x2) + abs(y1 - y2)

        return wirelength

    def accept_new_solution(self, old_cost, new_cost, temperature):
        if new_cost < old_cost:
            # If the new solution is better (lower cost), accept it
            return True
        else:
            # If the new solution is worse (higher cost), accept it with a certain probability
            delta_cost = new_cost - old_cost
            acceptance_probability = math.exp(-delta_cost / temperature)
            return random.random() < acceptance_probability

    def modify_weights(self, iteration, max_iterations):
        # Example: Linearly decrease the weight of a specific cost component
        initial_weight = 1.0
        final_weight = 0.1

        alpha = (final_weight - initial_weight) / max_iterations
        current_weight = initial_weight + alpha * iteration

def update_temperature(current_temperature, cooling_rate):
    # Linearly reduce the temperature by the cooling rate
    new_temperature = current_temperature - cooling_rate
    return max(new_temperature, 0)

def fix_outline_floorplan(blocks, outline_width, outline_height):
    floorplan = BStarFloorplan(blocks)
    best_solution = floorplan
    temperature = initial_temperature
    cooling_rate = 1.0

    iteration = 0
    max_iterations = 100

    while not converged and temperature > cooling_down_threshold:
        old_cost = floorplan.evaluate_cost()
        floorplan.perturb()
        new_cost = floorplan.evaluate_cost()

        if floorplan.accept_new_solution(old_cost, new_cost, temperature):
            best_solution = floorplan

        floorplan.modify_weights(iteration, max_iterations)
        temperature = update_temperature(temperature, cooling_rate)

    return best_solution

if __name__ == "__main__":
    blocks = [Block(4, 5), Block(3, 7), Block(6, 2), Block(8, 4), Block(5, 6)]
    outline_width = 20
    outline_height = 15
    initial_temperature = 100.0
    cooling_down_threshold = 1e-3
    converged = False

    best_solution = fix_outline_floorplan(blocks, outline_width, outline_height)
    print("Best Floorplan:")
    for block_key, position in best_solution.positions.items():
        print(f"Block Position: ({position[0]}, {position[1]}) for Block {block_key}")