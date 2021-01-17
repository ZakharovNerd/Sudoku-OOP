
from random import randint
from random import choice


class Field:
    def possible(self, x, y):
        res = [i for i in range(1, 10)]
        for i in range(9):
            if res.count(self.field[i * 9 + x]) > 0:
                res.remove(self.field[i * 9 + x])
            if res.count(self.field[y * 9 + i]) > 0:
                res.remove(self.field[y * 9 + i])
        x //= 3
        y //= 3
        for sx in range(3):
            for sy in range(3):
                if res.count(self.field[(y * 3 + sy) * 9 + x * 3 + sx]) > 0:
                    res.remove(self.field[(y * 3 + sy) * 9 + x * 3 + sx])
        return res


    def __init__(self, nums : int):
        self.field = [0 for x in range(81)]
        for _ in range(nums):
            x = randint(0, 80)
            while self.field[x] > 0:
                x = randint(0, 80)
            self.field[x] = choice(self.possible(x % 9, x // 9))

    def print(self):
        for y in range(9):
            if y % 3 == 0:
                print("+-------+-------+-------+")
            for x in range(9):
                if x % 3 == 0:
                    print("| ", end="")

                if self.field[y * 9 + x] > 0:
                    print(self.field[y * 9 + x], end=" ")
                else:
                    print("  ", end="")
            print("|")
        print("+-------+-------+-------+")

    def save(self, path):
        file = open(path, "w")
        for x in range(81):
            file.write(f"{self.field[x]} ")
        file.close()

    def load(self, path):
        file = open(path, "r")
        line = file.readline().split()
        for x in range(81):
            self.field[x] = int(line[x])

    def check(self):
        for i in range(9):
            nums = []
            for j in range(9):
                if nums.count(self.field[i * 9 + j]) > 0:
                    return False
                else:
                    nums.append(self.field[i * 9 + j])
            nums = []
            for j in range(9):
                if nums.count(self.field[j * 9 + i]) > 0:
                    return False
                else:
                    nums.append(self.field[j * 9 + i])

        for bx in range(3):
            for by in range(3):
                nums = []
                for sx in range(3):
                    for sy in range(3):
                        v = self.field[(by * 3 + sy) * 9 + bx * 3 + sx]
                        if v < 1 or nums.count(v) > 0:
                            return False
                        else:
                            nums.append(v)
        return True

    def place(self, x, y, v):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return
        self.field[y * 9 + x] = v

    def at(self, x, y):
        return self.field[y * 9 + x]

    def solve(self):
        empty = -1
        for i in range(81):
            if self.field[i] < 1:
                empty = i
                break

        if empty < 0:
            return True

        x = empty % 9
        y = empty // 9

        for v in self.possible(x, y):
            print(f"x: {x}  y: {y}  value: {v}")
            self.place(x, y, v)
            self.print()
            if self.solve():
                return True
            self.place(x, y, 0)
        return False


field = None
running = True
while running:
    if field != None:
        field.print()
        if field.check():
            print("You win.")
            break

    action = input("Enter action: ")
    if action == "start":
        nums = int(input("Enter numbers count: "))
        field = Field(nums)
    elif action == "save":
        field.save("game.pkl")
    elif action == "load":
        field = Field(0)
        field.load("game.pkl")
    elif action == "exit":
        running = False
    elif action == "solve":
        if field.solve():
            print("Successfully solved.")
        else:
            print("Can not be solved.")
    else:
        vals = action.split()
        field.place(int(vals[0]), int(vals[1]), int(vals[2]))

