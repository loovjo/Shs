import subprocess
import sys
from asciirange import create_range

sys.setrecursionlimit(100)

chars_in_names = create_range('a-zA-Z0-9_')

def tokenize(code):
    # Split on non-alphanumerical characters
    res = []
    token = ''
    in_string = False
    in_number = False
    after_dot = False
    in_shell_command = False

    for ch in code:
        # print(ch, repr(token), in_string, in_number, after_dot)
        token_break = False
        after_number = False

        if ch == '\"':
            if not in_string:
                token_break = True
            else:
                token += ch
                ch = ""
                token_break = True

            in_string = not in_string
        elif in_string:
            token += ch
        elif in_number and ch.isdigit():
            token += ch
        elif ch.isdigit() and token == "":
            in_number = True
            token += ch
        elif ch == "-" and not in_number:
            after_number = True
            token_break = True
        elif ch == "." and in_number:
            if after_dot:
                in_number = False
                token_break = True
            else:
                after_dot = True
                token += ch
        elif ch not in chars_in_names:
            token_break = True
        elif ch != " ":
            if len(token) == 1 and token[0] not in chars_in_names:
                token_break = True
            else:
                token += ch
            in_number = after_dot = False

        if token_break:
            if token != "":
                res.append(token)
            token = ch.strip()
            in_number = after_number
            after_dot = False

    if token != '':
        res.append(token)
    return res

class ShellCommand(tuple):
    def __str__(self):
        return "!%s;" % " ".join(self)
    __repr__ = __str__

class Function(tuple):
    def __str__(self):
        return "Function{%s}" % " ".join(map(str, self))
    __repr__ = __str__
class Ordering:
    def __init__(self, before, after):
        self.before = tuple(before)
        self.after = tuple(after)
    def __str__(self):
        return "Ordering(%s - %s)" % (self.before, self.after)
    def __eq__(self, other):
        if isinstance(other, Ordering):
            return self.before == other.before and self.after == other.after
        return False
    __repr__ = __str__

def parse(code):
    if code == []:
        return ()
    if code[0] == "{":
        # Find matching brace
        depth = 0
        i = 0
        while i < len(code):
            token = code[i]
            if token == "{":
                depth += 1
            if token == "}":
                depth -= 1
            if depth == 0:
                break
            i += 1
        return (Function(parse(code[1:i])), *parse(code[i + 1:]))
    if code[0] == "!":
        # Find matching brace
        i = 0
        while i < len(code):
            if code[i] == ";":
                break
            i += 1

        return (ShellCommand(code[1:i]), *parse(code[i + 1:]))
    if code[0] == "(":
        # Find matching paren
        before = []
        after = []
        isBefore = True
        depth = 1
        i = 1
        while i < len(code):
            token = code[i]
            if token == "(":
                depth += 1
            if token == ")":
                depth -= 1
                if depth == 0:
                    break
            if token == "-" and depth == 1 and isBefore:
                isBefore = False
            elif isBefore:
                before.append(token)
            else:
                after.append(token)
            i += 1
        return (Ordering(before, after), *parse(code[i + 1:]))
    return (code[0], *parse(code[1:]))

if __name__ == "__main__":
    print(parse(tokenize('["hej" ]')))
