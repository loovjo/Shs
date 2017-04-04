
#SHS


Shs is a stack based imperative language with functional support.

What is a stack based language, you might be asking. A stack based language is a programming language where most of the data is stored in a list, called "the stack". Most of the commands work on the top elements of the stack, and place their result(s) on the top to. For example, a number is a command that pushes itself to the top of the stack, and the `+` command results in the sum of the top two elements of the stack, removing them in the process, so the program `3 4 +` results in just the number `7` on the top of the stack.


Types:
- String, denoted `""`
- Block, denoted `{}`
- Lists, denoted `[]`
- Numbers, denoted:
    `nN` for natural numbers
    `nZ` for integers
    `nR` for all numbers (complex included)

Commands: (`a` is top element, `b` is second, etc.)

    + 2
        a: nR, b: nR -> a + b
        a: "", b: "" -> b concat a
        a: [], b: [] -> b append a
        a: {}, b: {} -> {a b}

    - 2
        a: nR, b: nR -> a - b
        a: "", b: "" -> b with all a's removed
        a: [], b: [] -> b with all a's removed
    * 2
        a: nR, b: nR -> a * b
        a: nN, b: ""/[] -> b repeated a times
        a: nN, b: {} -> b executed a times
        a: "", b: [] -> b joined with a
    / 2
        a: nR, b: nR -> a / b
        a: "", b: "" -> b split at a
        a: {}, b: [] -> b.reduce(a)   (pop b, pop b, apply a, pop b, apply a, pop b, apply a ... collect)
    % 2
        a: nR, b: nR -> b % a
        a: {}, b: []/"" -> b.map(a)
    & 2
        a: {}, b: []/"" -> b.filter(x -> a(x) != 0)
        a: nZ, b: nZ -> a & b
    ^ 1
        a: {} -> Executes a while the top of the stack is non-falsey
    < 2
        a: *, b: * -> a is less than b
    > 2
        a: *, b: * -> a is greater than b
    = 2
        a: *, b: * -> a equals b
    , 1
        a: nN -> [0, 1, ... a - 1]
        a: [] -> length of a
    i 1
        a: nR -> floor(a)
        a: "" -> int(a)
    ! 1
        a: [] -> Run a as a shell command, a[0] as the command, a[1:] as arguments. Return the output of the command
    [ 0
        Append length of stack to the list-stack (different from the main stack)
    ] 0
        Pop an element from the list-stack, take the difference between it and the main stack length and wrap that many items into an array
    l 0
        Pop an element from the list-stack to the main stack
    L 1
        a: nN -> Push a to the list-stack
    W 0
        Decrease the top element on the list-stack.
        Usefull to wrap a few elements into a list, eg. [WWW] wraps the top three elements into a list.
    @ 2
        a: nN, b: [] -> a'th element of b
        a: [A], b: [] -> b[::A]
        a: [A,B], b: [] -> b[A:B]
        a: [A,B,C], b: [] -> b[A:B:c]
    ~ 1
        a: nZ -> 1 - a
        a: {} -> apply a
    p 1
        a: * -> print a with a trailing newline
    P 1
        a: * -> print a without a trailing newline
    inp 0
        Read a line from stdin and push it to the stack
    debug 0
        Print debug info, namely the stack, the list-stack and some other stuff.
    ` 1
        a: * -> repr(a)
    ' 1
        a: nN -> Unicode character of a
        a: "" -> Unicode value of a. Only works if len(a) == 1
    ? 1
        a: nN -> a random integer between 0 and a (not inclusive)
        a: nR, a > 0 -> a random number between 0 and a (not inclusive)
    ; 1
        a: * -> Nothing, just pop a. Same as (a -). See reorderings
    . 1:
        a: * -> Push two copies of a. Same as (a - a a). See reorderings

    :   See variables

### Reorderings

If you want to manipulate the positions of the elements of the stack and/or duplicate or remove them, you can use a "reordering"

Reorderings are made in the following format:

    (var1 var2 var3 ... varN - var1 var2 var3 ... varN)

The tokens before the - are called "binders", while the tokens after are called "orderings". Neither the order nor the count of each binder must match with the corresponding orderings, so all of these are valid reorderings:

    (a b c - b a c)
    (a b c - a)
    (a - a a)
    (a b - a b a b)

What these does is the following: say we have a reordering like this: `(a b c - b c b a)` and a stack like this: `[1 2 "3"]`. Now, the first part of the reordering, before the `-` become binded to the values on the top of the stack, `a` is binded with `1`, `b` is with `2` and `c` is with `"3"`. Now, after the `-` each binded element is put back. In this case, `b c b a` corresponds to `2 "3" 2 1`. These values are added to the top of the stack, while the originals are removed.

Some reorderings, namely `(a - a a)` and `(a -)` are so commonly used that they have been added as regular commands, `(a - a a)` is `.` and `(a -)` is `;`.

If you don't have a `-` in the reordering, it will automatically be inserted in the end. Therefore, the "remove top element" reordering can be written as `(a)`.

The binders, in the previous case `"a"`, `"b"` and `"c"`, can be any valid token in shs. If you want to use multiple words in a token, you can surround it by quotes, `("like this")`. Keep in mind that the quotes are actually a part of the binder, so `("binder")` and `(binder)`, are two different entities.

Some other notes:

* In repl-mode, a reordering doesn't have to be closed, so if, say, you quickly want to remove the first three elements of the stack you could do `(;;;` or even `(((` since parentheses are a valid token. This also works at the end of scripts.

Useful tips and tricks:

* Manipulating the last elements of a list: 
    If you have a list, and for example want to remove the first element, you could do this:

        [W {}/ (a)]

    Here, the {}/ dumps all the elements of the list onto the stack, and the [W ] construct wraps them back into a list afterwards.

### Comments
Shs doesn't have a specific comment syntax, but instead you could use the fact that functions aren't syntax checked, and write a comment in this way: `{Comment Here}(_)`, this just pushes the comment in a function to the stack and then popping it off.

### Variables
Shs has command to save a value into a variable, the `:` command. The `:` command takes one argument from the stack, which isn't popped and another argument, the next token in front of it in the code. The token after the `:` isn't executed. When executed, the command saves the value on the stack with the next token as its name. When a command is executed which matches the name of a variables, instead of executing the command, the value of the variable is instead pushed to the stack.

Variables can be set multiple times, but cannot be un-set.

Some examples:

    10 :x       Save the value 10 in the variable x, keeps the 10 on the stack
    ; [x x]     Remove the 10, and push a list containing two 10's from the variable x

This program is a bit more complex:

    5 :x P         Save the number 5 in x and print it
    {               Start a block
        x 10 + :x       Push the variable, add 10 to it and save it again. Keeps the value of the variable on the stack
        ", "P P         Print it with a comma before
    }               End the block
    5*              Execute that code in the block 5 times

It results in the output `5, 15, 25, 35, 45, 55` by updating the value of `x`

