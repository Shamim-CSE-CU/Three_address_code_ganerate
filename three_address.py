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

class TempVariableGenerator:
    def __init__(self):
        self.counter = 0

    def get_temp(self):
        self.counter += 1
        return f't{self.counter}'

class ThreeAddressCode:
    def __init__(self):
        self.instructions = []

    def emit(self, op, arg1, arg2, result):
        self.instructions.append((op, arg1, arg2, result))

# Example AST construction
expression = BinaryOpNode('+', BinaryOpNode('*', 'c', 'd'), 'b')
assignment = AssignmentNode('a', expression)

# Initialize temporary variable generator and TAC generator
temp_generator = TempVariableGenerator()
tac = ThreeAddressCode()

# Recursive function to generate TAC
def generate_tac(node, target=None):
    if isinstance(node, BinaryOpNode):
        temp1 = temp_generator.get_temp()
        generate_tac(node.left, temp1)
        temp2 = temp_generator.get_temp()
        generate_tac(node.right, temp2)
        tac.emit(node.operator, temp1, temp2, target)
    elif isinstance(node, AssignmentNode):
        temp3 = temp_generator.get_temp()
        generate_tac(node.expression, temp3)
        tac.emit('=', temp3, None, node.target)
    else:
        tac.emit('=', node, None, target)

# Generate TAC for the assignment
generate_tac(assignment)

# Print the generated TAC
for instruction in tac.instructions:
    print(instruction)
