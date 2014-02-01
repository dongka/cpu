from ast import *
from visitor import Visitor


class Render(Visitor):
    def __init__(self, lines, errors):
        self.errors = errors
        self.lines = []
        
        self.visit(lines)
    
    def visit_Label(self, label):
        line = label.name + ':'
        if label.public:
            line = line + ':'
        self.add_line(line)

    def visit_Jump(self, jump):
        line = 'jmp ' + jump.target
        self.add_line(line)

    def visit_Instruction(self, instr):
        self.visit_parts(instr)

    def visit_BinaryOperation(self, op):
        if op.parts[1] == '=' and isinstance(op.parts[2], Numeral):
            line = 'mov %d, %s' % (op.parts[2].value, op.parts[0].name)
        elif op.parts[1] == '=' and isinstance(op.parts[2], BinaryOperation):
            dest = op.parts[0]
            arg1 = op.parts[2].parts[0]
            arg2 = op.parts[2].parts[2]
            opr = op.parts[1]
            if opr == '<':
                line = 'slt %s, %s, %s' % (arg1.name, arg2.name, dest.name)
            elif opr == '+':
                line = 'add %s, %s, %s' % (arg1.name, arg2.name, dest.name)
            else:
                raise NotImplementedError(repr(op))
        else:
            raise NotImplementedError(repr(op))
        self.add_line(line)

    def visit_FunctionCall(self, fc):
        if fc.name.declaration == out_builtin:
            line = 'out %s, %s' % (fc.args[0].name, fc.args[1].name)
        else:
            raise NotImplementedError(repr(op))
        self.add_line(line)

    def add_line(self, line):
        self.lines.append(line)
