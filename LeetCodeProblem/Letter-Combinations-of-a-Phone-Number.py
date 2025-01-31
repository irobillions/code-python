from itertools import product


def letterCombinations(digits: str) -> list[str]:
    res = []

    if not digits:
        return []

    keypad_mapping = {
        "2": ["a", "b", "c"],
        "3": ["d", "e", "f"],
        "4": ["g", "h", "i"],
        "5": ["j", "k", "l"],
        "6": ["m", "n", "o"],
        "7": ["p", "q", "r", "s"],
        "8": ["t", "u", "v"],
        "9": ["w", "x", "y", "z"]
    }

    def combineStr(index: int, current_combinaisons: list[str]):
        if index == len(digits):
            res.append("".join(current_combinaisons))
            return

        current_digits = digits[index]
        currents_letter_lists = keypad_mapping[current_digits]

        for letter in currents_letter_lists:
            current_combinaisons.append(letter)
            combineStr(index + 1, current_combinaisons)
            current_combinaisons.pop()

    combineStr(0, [])
    return res


def letterCombinationsNaiveSol(digits: str) -> list[str]:
    if not digits:
        return []
    keypad_mapping = {
        "2": ["a", "b", "c"], "3": ["d", "e", "f"],
        "4": ["g", "h", "i"], "5": ["j", "k", "l"],
        "6": ["m", "n", "o"], "7": ["p", "q", "r", "s"],
        "8": ["t", "u", "v"], "9": ["w", "x", "y", "z"]
    }

    combinaisons = [""]
    for current_letter in digits:
        current_letter_list = keypad_mapping[current_letter]
        new_combinaisons = []

        for comb in combinaisons:
            for letter in current_letter_list:
                new_combinaisons.append(comb + letter)
        combinaisons = new_combinaisons

    return combinaisons


if __name__ == '__main__':
    letters = '2395'
    print(letterCombinationsNaiveSol(letters))
