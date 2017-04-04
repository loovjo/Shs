import random

from Parser import Function
import shs

commands = []

class Command:
    command_char = ""
    arity = -1
    def apply(self, args, env):
        pass

class PlusCommand(Command):
    command_char = "+"
    arity = 2
    def apply(self, args, env):
        if isinstance(args[0], str) or isinstance(args[1], str):
            return str(args[1]) + str(args[0])
        if isinstance(args[0], Function) and isinstance(args[1], Function):
            return Function(args[1] + args[0])
        return args[1] + args[0]
commands.append(PlusCommand())

class MinusCommand(Command):
    command_char = "-"
    arity = 2
    def apply(self, args, env):
        if isinstance(args[0], str) and isinstance(args[1], str):
            while args[0] in args[1]:
                args[1] = args[1][:args[1].find(args[0])] + args[1][args[1].find(args[0]) + len(args[0]):]
                print(args)
            return args[1]
        if isinstance(args[0], tuple) or isinstance(args[0], list) and isinstance(args[1], tuple) or isinstance(args[1], list):
            return [a for a in args[1] if a not in args[0]]
        return args[1] - args[0]
commands.append(MinusCommand())

class StarCommand(Command):
    command_char = "*"
    arity = 2
    def apply(self, args, env):
        if isinstance(args[1], Function):
            return shs.run(tuple(args[1] * int(args[0])), env)
        if isinstance(args[1], list):
            if isinstance(args[0], str):
                return args[0].join(map(str, args[1]))
            else:
                return list(args[1] * int(args[0]))
        if isinstance(args[1], tuple):
            return tuple(args[1] * int(args[0]))
        return args[0] * args[1]

commands.append(StarCommand())

class SlashCommand(Command):
    command_char = "/"
    arity = 2
    def apply(self, args, env):
        if isinstance(args[0], str) and isinstance(args[1], str):
            return args[1].split(args[0])
        if isinstance(args[0], Function):
            env.push(args[1][0])
            for e in args[1][1:]:
                env.push(e)
                env = shs.run(args[0], env)
            return env
        return args[1] / args[0]
commands.append(SlashCommand())

class ModulusCommand(Command):
    command_char = "%"
    arity = 2
    def apply(self, args, env):
        if isinstance(args[0], Function):
            res = []
            for e in args[1]:
                env.push(e)
                env = shs.run(args[0], env)
                res.append(env.pop()[0])
            env.push(res)
            return env

        return args[1] % args[0]
commands.append(ModulusCommand())

class AmpersandCommand(Command):
    command_char = "&"
    arity = 2
    def apply(self, args, env):
        if isinstance(args[0], Function):
            res = []
            for e in args[1]:
                env.push(e)
                env = shs.run(tuple(args[0]), env)
                last = env.pop(1)[0]
                if last:
                    res.append(e)
            return res
        return args[1] & args[0]
commands.append(AmpersandCommand())

class HatCommand(Command):
    command_char = "^"
    arity = 1
    def apply(self, args, env):
        if isinstance(args[0], Function):
            while True:
                env = shs.run(tuple(args[0]), env)
                last = env.pop()[0]
                if not last:
                    break
            return env
commands.append(HatCommand())

class LessThanCommand(Command):
    command_char = "<"
    arity = 2
    def apply(self, args, env):
        return args[1] < args[0]
commands.append(LessThanCommand())

class GreaterThanCommand(Command):
    command_char = ">"
    arity = 2
    def apply(self, args, env):
        return args[1] > args[0]
commands.append(GreaterThanCommand())

class EqualsCommand(Command):
    command_char = "="
    arity = 2
    def apply(self, args, env):
        return args[0] == args[1]
commands.append(EqualsCommand())

class CommaCommand(Command):
    command_char = ","
    arity = 1
    def apply(self, args, env):
        if isinstance(args[0], int):
            return list(range(args[0]))
        if hasattr(args[0], "__len__"):
            return len(args[0])
commands.append(CommaCommand())

class IntCommand(Command):
    command_char = "i"
    arity = 1
    def apply(self, args, env):
        return int(args[-1])
commands.append(IntCommand())

class BangCommand(Command):
    command_char = "!"
    arity = 1
    def apply(self, args, env):
        if isinstance(args[0], tuple) or isinstance(args[0], list):
            return shs.run_process(args[0])
        elif isinstance(args[0], str):
            return shs.run_process(args[0].split(" "))
commands.append(BangCommand())

class OpenBracketCommand(Command):
    command_char = "["
    arity = 0
    def apply(self, args, env):
        env.list_stack.append(len(env.stack))
commands.append(OpenBracketCommand())

class CloseBracketCommand(Command):
    command_char = "]"
    arity = 0
    def apply(self, args, env):
        amount = len(env.stack) - env.list_stack_pop()
        return env.pop(amount)[::-1]
commands.append(CloseBracketCommand())

class LetterLCommand(Command):
    command_char = "L"
    arity = 1
    def apply(self, args, env):
        return env.list_stack.append(args[0])
commands.append(LetterLCommand())

class LetterlCommand(Command):
    command_char = "l"
    arity = 0
    def apply(self, args, env):
        return env.list_stack.pop()
commands.append(LetterlCommand())

class LetterWCommand(Command):
    command_char = "W"
    arity = 0
    def apply(self, args, env):
        env.list_stack.append(env.list_stack_pop() - 1)

commands.append(LetterWCommand())

class AtCommand(Command):
    command_char = "@"
    arity = 2
    def apply(self, args, env):
        if hasattr(args[1], "__getitem__"):
            if isinstance(args[0], int):
                return args[1][args[0]]
            if hasattr(args[0], "__getitem__") and hasattr(args[0], "__len__"):
                if len(args[0]) == 1:
                    print(args[0], args[1])
                    return args[1][::args[0][0]]
                if len(args[0]) == 2:
                    return args[1][args[0][0]:args[0][1]]
                if len(args[0]) == 3:
                    return args[1][args[0][0]:args[0][1]:args[0][3]]
commands.append(AtCommand())

class TidleCommand(Command):
    command_char = "~"
    arity = 1
    def apply(self, args, env):
        if isinstance(args[0], int):
            return 1 - args[0]
        if isinstance(args[0], Function):
            return shs.run(tuple(args[0]), env=env)
        if isinstance(args[0], str):
            return shs.run_string(args[0], env=env)
commands.append(TidleCommand())

class PrintUpperCommand(Command):
    command_char = "P"
    arity = 1
    def apply(self, args, env):
        for arg in args:
            print(arg, end="", flush=True)
commands.append(PrintUpperCommand())

class PrintCommand(Command):
    command_char = "p"
    arity = 1
    def apply(self, args, env):
        for arg in args:
            print(arg)
commands.append(PrintCommand())

class InputCommand(Command):
    command_char = "inp"
    arity = 0
    def apply(self, args, env):
        env.push(input())
commands.append(InputCommand())

class DebugCommand(Command):
    command_char = "debug"
    arity = 0
    def apply(self, args, env):
        print(env)
commands.append(DebugCommand())

class RandomCommand(Command):
    command_char = "?"
    arity = 1
    def apply(self, args, env):
        if isinstance(args[0], int):
            return random.randrange(0, args[0])
        return random.random() * args[0]
commands.append(RandomCommand())

class BacktickCommand(Command):
    command_char = "`"
    arity = 1
    def apply(self, args, env):
        return repr(args[0])
commands.append(BacktickCommand())

class UnicodeCommand(Command):
    command_char = "'"
    arity = 1
    def apply(self, args, env):
        if isinstance(args[0], int):
            return chr(args[0])
        return ord(args[0])
commands.append(UnicodeCommand())

class PopComamnd(Command):
    command_char = ";"
    arity = 1
    def apply(self, args, env):
        return env
commands.append(PopComamnd())

class DupComamnd(Command):
    command_char = "."
    arity = 1
    def apply(self, args, env):
        env.push(args[0])
        env.push(args[0])
        return env
commands.append(DupComamnd())

def get_command(name):
    for command in commands:
        if command.command_char == name:
            return command
    return None
