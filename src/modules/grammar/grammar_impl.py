import random
from typing import List, Tuple


class Grammar:
    def __init__(self, vn: List[str], vt: List[str], p: List[Tuple[str, str, str]]) -> None:
        self._vn: List[str] = vn
        self._vt: List[str] = vt
        self._p: List[Tuple[str, str, str]] = p

    def get_type(self, string: str) -> str:
        types: List[bool] = [False, False, False, False]
        types[3] = True  # Type 3


        return "Type 3"




    def generate_string(self, string: str) -> str:
        flag: bool = True
        while flag:
            flag = False
            for i in range(len(string)):
                if self.is_non_terminal(string[i]):
                    choices: List[int] = self.get_indices(string[i])
                    rule_index: int = random.choice(choices)
                    r: str = self.get_rule(rule_index)

                    string = string[:i] + r + string[i + 1:]
                    flag = True
        return string[:-1]

    def get_indices(self, string: str) -> List[int]:
        result: List[int] = []
        for tran in self._p:
            if string == tran[0]:
                result.append(self._p.index(tran))
        return result

    def is_terminal(self, string: str) -> bool:
        return string in self._vt

    def is_non_terminal(self, string: str) -> bool:
        return string in self._vn

    def get_rule(self, index: int) -> str:
        return self._p[index][1] + self._p[index][2]
