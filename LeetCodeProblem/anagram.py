from collections import defaultdict


def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    sorted_t = sorted(t)
    sorted_s = sorted(s)
    return ''.join(sorted_s) == ''.join(sorted_t)


def isAnagram2(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    s = s.lower()
    t = t.lower()
    count = [0] * 26
    for c1, c2 in zip(s, t):
        count[ord(c1) - ord('a')] += 1
        count[ord(c2) - ord('a')] -= 1

    return all(x == 0 for x in count)


def isAnagram3(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    freq = defaultdict(int)
    for c1, c2 in zip(s, t):
        freq[ord(c1)] += 1
        freq[ord(c2)] -= 1

    return all(x == 0 for x in freq.values())





if __name__ == '__main__':
    print(isAnagram3("ab_b", "b_ab"))
