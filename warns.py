class Warns:
    def __init__(self) -> None:
        self._computers_warns = {i: 0 for i in range(1, 7)}

    def add_warn(self, computer: int) -> None:
        self._computers_warns[computer] += 1

    def remove_warn(self, computer: int) -> None:
        if self._computers_warns[computer] != 0:
            self._computers_warns[computer] -= 1

    def set_warns(self, computer: int, count: int) -> None:
        self._computers_warns[computer] = count

    def get_warns_for_selected_computer(self, computer: int) -> int:
        return self._computers_warns[computer]

if __name__ == '__main__':
    a = Warns()
    a.add_warn(1)
    print(a.get_warns_for_selected_computer(1))