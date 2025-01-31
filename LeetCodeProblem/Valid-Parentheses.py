def isValid(s: str) -> bool:
    str_size = len(s)
    stack = []

    if str_size % 2 != 0:
        return False

    for char in s:
        if isOpenBrackets(char):
            stack.append(char)
        if isCloseBrackets(char):
            if len(stack) == 0:
                return False
            current_char = stack.pop()
            if abs(ord(current_char) - ord(char)) not in [1, 2]:
                return False
    if len(stack) != 0:
        return False

    return True



def isOpenBrackets(s: str) -> bool:
    return s == '(' or s == '[' or s == '{'


def isCloseBrackets(s: str) -> bool:
    return s == ")" or s == "]" or s == "}"


def isValid2(s: str) -> bool:
    stack = []
    mapping_bracket = {')': '(', '}':'{', ']':'['}

    if len(stack) % 2 != 0:
        return False

    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != mapping_bracket[char]:
                return False

    if stack:
        return False
    return True


if __name__ == '__main__':
    print(isValid2("([])"))
