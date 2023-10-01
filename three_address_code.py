# Define data structures for AST nodes and three-address code instructions
class ASTNode:
    pass

class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class AssignmentNode(ASTNode):
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

class ThreeAddressCode:
    def __init__(self):
        self.instructions = []

    def emit(self, opcode, op1, op2, result):
        self.instructions.append((opcode, op1, op2, result))

# Example AST construction
expression = BinaryOpNode('+', BinaryOpNode('*', 'c', 'd'), 'b')
assignment = AssignmentNode('a', expression)

# Initialize the three-address code generator
tac = ThreeAddressCode()

# Helper function for generating temporary variables
temp_counter = 0
def get_temp():
    global temp_counter
    temp_counter += 1
    return f't{temp_counter}'

# Recursive function to generate three-address code
def generate_tac(node, target=None):
    if isinstance(node, BinaryOpNode):
        temp = get_temp()
        generate_tac(node.left, temp)
        generate_tac(node.right, temp)
        tac.emit(node.operator, node.left, node.right, temp)
        if target:
            tac.emit('=', temp, None, target)
    elif isinstance(node, AssignmentNode):
        generate_tac(node.expression, node.target)
    else:
        # Handle literals or variables
        if target:
            tac.emit('=', node, None, target)

# Generate three-address code for the assignment
generate_tac(assignment, 'a')

# Print the generated three-address code
for instruction in tac.instructions:
    print(instruction)
