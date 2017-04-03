import sys, textwrap

def create_range(text):
    total_range = ""
    range_from = ""
    text_ptr = 0
    escaping = False
    while text_ptr < len(text):
        ch = text[text_ptr]
        if ch == "-" and range_from != "" and not escaping:
            start = ord(range_from)
            end = ord(text[text_ptr + 1])
            if start < end:
                total_range += "".join(list(map(chr, range(start + 1, end))))
            else:
                total_range += "".join(list(map(chr, range(end + 1, start)[::-1])))
        elif ch == "\\" and not escaping:
            escaping = True
        else:
            range_from = ch
            total_range += ch
            escaping = False
        text_ptr += 1

    return total_range

if __name__ == "__main__":
    if "-h" in sys.argv:
        print(textwrap.dedent("""
                asciirange.py - Make ascii ranges
                    
                    Options:
                        -i  Read from STDIN aswell as args
                Examples:
                    a-z:              abcdefghijklmnopqrstuvwxyz
                    0-9a-zA-Z:        0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
                    a-zåäö:           abcdefghijklmnopqrstuvwxyzåäö
                    A-Za-z0-9+\\-/_    ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-/_
                """))

    for arg in sys.argv[1:]:
        if arg[0] == "-":
            continue
        print(create_range(arg))
    if "-i" in sys.argv:
        for arg in sys.stdin.readlines():
            print(create_range(arg))
