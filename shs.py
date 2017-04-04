import sys
import readline
import subprocess

from ast import literal_eval

import Parser
import Commands

run_string = lambda x, env=None: run(Parser.parse(Parser.tokenize(x)), env)

class Enviroment:
    def __init__(self, stack=[], variables={}):
        self.stack = stack
        self.variables = {}
        self.list_stack = []
    def pop(self, amount=1):
        res, self.stack = self.stack[:amount], self.stack[amount:]
        return res
    def peek(self, amount=1):
        return self.stack[:amount]
    def push(self, value):
        self.stack = [value] + self.stack
    def list_stack_pop(self):
        if self.list_stack == []:
            return 0
        return self.list_stack.pop()
    def setvar(self, var, value):
        self.variables[var] = value
    def getvar(self, var):
        return self.variables[var]
    def __str__(self):
        return "Env(stack=%r,vars=%r,l_stack=%r)" % (self.stack, self.variables, self.list_stack)
    def is_enviroment(self):
        return True

def run_process(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    return p.stdout.read().decode()

def is_number(text):
    try:
        float(text)
        return True
    except (ValueError, TypeError):
        return False

def run(code, env=None):
    if env == None:
        env = Enviroment()
    while code:
        item, code = code[0], code[1:]
        if isinstance(item, Parser.Ordering):
            if len(env.stack) < len(item.before):
                print("Not enough items on stack!")
                continue
            args = env.pop(len(item.before))
            big_dic = dict()
            for i, ch in enumerate(item.before):
                big_dic[ch] = args[len(args) - i - 1]
            for ch in item.after:
                if ch in big_dic:
                    item = big_dic[ch]
                    env.push(item)
        elif isinstance(item, Parser.Function):
            env.push(item)
        elif item in env.variables:
            env.push(env.variables[item])
        elif item == ":":
            var_name = code[0]
            value = env.peek()[0]
            env.variables[var_name] = value
            code = code[1:]
        elif isinstance(item, Parser.ShellCommand) and len(item) > 0:
            run_process(item)
        elif len(item) > 0 and item[0] == item[-1] == '"':
            env.push(literal_eval(item))
        elif is_number(item):
            if "." in item:
                env.push(float(item))
            else:
                env.push(int(item))
        else:
            if isinstance(item, Parser.ShellCommand):
                item = "!"
            command = Commands.get_command(item)
            if command is None:
                print("Command %s not found" % repr(item))
                return env
            if command.arity > len(env.stack):
                print("Not enough arguments!")
            else:
                args = env.pop(command.arity)
                res = command.apply(args, env)
                if res != None:
                    if hasattr(res, "is_enviroment") and res.is_enviroment:
                        env = res
                    else:
                        env.push(res)
    return env

if __name__ == "__main__":
    env = Enviroment()
    if len(sys.argv) > 1:
        for a in sys.argv[1:]:
            prog = open(a, "r").read()
            run_string(prog, env)
    else:
        while True:
            try:
                line = input("%s> " % env.stack)
            except EOFError:
                break
            env = run_string(line, env)

