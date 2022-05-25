class Puzzle:

    def __init__(self, nums):

        # nums --> {QLineEdit object: [i-coord (starting at 3), j-coord (starting at 2)]}
        self.numbers = {i for i in range(1, 10)}
        self.modified = set()
        self.tracker = []
        self.boxes = nums
        self.puzzle = {}
        self.zeros = 81

        i = 0
        j = 0
        for n in self.boxes:
            if i == 9:
                i = 0
            if j == 9:
                i += 1
                j = 0

            try:
                val = int(n.text())
                self.zeros -= (1 if val != 0 else 0)
            except ValueError:
                val = 0

            self.puzzle[(i, j)] = val

            j += 1

    def id_box(self, i, j):
        while i % 3 != 0:
            i -= 1

        while j % 3 != 0:
            j -= 1

        return [i, j]

    def solve_box(self, i, j):
        if self.puzzle[(i, j)] != 0:
            return self.puzzle[(i, j)]

        row, col = self.id_box(i, j)

        visited = []
        summation = 0

        for r in range(row, row + 3):
            for c in range(col, col + 3):
                if not (r == i and c == j) and self.puzzle[(r, c)] != 0:
                    visited.append(self.puzzle[(r, c)])
                    summation += self.puzzle[(r, c)]

        if len(visited) == 8:
            diff = 45 - summation
            self.zeros -= 1
            self.modified.add((i, j))
            return diff

        return 0

    def solve_number(self, i, j):
        if self.puzzle[(i, j)] != 0:
            return self.puzzle[(i, j)]

        row_nums = set()
        for num in range(9):
            if self.puzzle[(i, num)] != 0:
                row_nums.add(self.puzzle[(i, num)])

        col_nums = set()
        for num in range(9):
            if self.puzzle[(num, j)] != 0:
                col_nums.add(self.puzzle[(num, j)])

        row, col = self.id_box(i, j)
        box_nums = set()
        for r in range(row, row + 3):
            for c in range(col, col + 3):
                if self.puzzle[(r, c)] != 0:
                    box_nums.add(self.puzzle[(r, c)])

        possible_nums = self.numbers.difference(row_nums)
        possible_nums = possible_nums.difference(col_nums)
        possible_nums = possible_nums.difference(box_nums)

        if len(possible_nums) == 1:
            self.zeros -= 1
            self.modified.add((i, j))
            return possible_nums.pop()
        else:
            return 0

    def solve_puzzle(self):

        self.tracker.append(self.zeros)

        for i in range(9):
            for j in range(9):
                self.puzzle[(i, j)] = self.solve_number(i, j)

        i = 0
        j = 0
        for n in self.boxes:
            if i == 9:
                i = 0
            if j == 9:
                i += 1
                j = 0

            n.setText(str(self.puzzle[(i, j)]))
            if (i, j) in self.modified:
                n.setStyleSheet("color:#62e322")
            elif self.puzzle[(i, j)] == 0:
                n.setStyleSheet("color:red")

            j += 1

        if self.zeros == 0:
            pass
        elif self.zeros == self.tracker.pop():
            pass
        else:
            self.solve_puzzle()
