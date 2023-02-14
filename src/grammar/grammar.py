import random
from typing import List


class Grammar:
    _vn: List[str] = []
    _vt: List[str] = []
    _p: List[List[str]] = []

    def __init__(self, vn: List[str], vt: List[str], p: List[List[str]]) -> None:
        self._vn = vn
        self._vt = vt
        self._p = p

    def get_indices(self, string: str) -> List[int]:
        result: List[int] = []
        for pr in self._p:
            print(pr, string)
            if string == pr[0]:
                result.append(self._p.index(pr))
        return result

    def generate_string(self, string: str) -> None:
        flag: bool = True

        while flag:
            flag = False
            for i in range(len(string)):
                if self.is_non_terminal(string[i]):
                    choices: List[int] = self.get_indices(string[i])
                    rule_index: int = random.choice(choices)
                    r = self.get_rule(rule_index)

                    string = string[:i] + r + string[i + 1:]
                    flag = True

        print(string)

    def is_terminal(self, string: str) -> bool:
        return string in self._vt

    def is_non_terminal(self, string: str) -> bool:
        return string in self._vn

    def get_rule(self, index: int) -> str:
        return self._p[index][1]
