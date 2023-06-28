import random

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, length, bow, direction):
        self.length = length
        self.bow = bow
        self.direction = direction
        self.hits = set()

    def dots(self):
        ship_dots = []
        if self.direction == "H":
            for i in range(self.length):
                dot = Dot(self.bow.x + i, self.bow.y)
                ship_dots.append(dot)
        elif self.direction == "V":
            for i in range(self.length):
                dot = Dot(self.bow.x, self.bow.y + i)
                ship_dots.append(dot)
        return ship_dots

class Board:
    def __init__(self):
        self.board = [["O"] * 6 for _ in range(6)]
        self.ships = []

    def show(self, hide_ships=False):
        print("  1 2 3 4 5 6")
        for i, row in enumerate(self.board):
            row_str = " ".join(row) if hide_ships else " ".join([c if c != "■" else "O" for c in row])
            print(i + 1, row_str)

    def add_ship(self, ship):
        for dot in ship.dots():
            x = dot.x - 1
            y = dot.y - 1
            self.board[y][x] = "■"
        self.ships.append(ship)

    def out_of_range(self, dot):
        return dot.x < 1 or dot.x > 6 or dot.y < 1 or dot.y > 6

    def overlapping(self, ship):
        for added_ship in self.ships:
            for dot in ship.dots():
                if dot in added_ship.dots():
                    return True
        return False

    def can_place(self, ship):
        for dot in ship.dots():
            if self.out_of_range(dot) or self.overlapping(ship):
                return False
        return True

    def random_place(self, length):
        while True:
            x = random.randint(1, 6)
            y = random.randint(1, 6)
            direction = random.choice(["H", "V"])
            ship = Ship(length, Dot(x, y), direction)
            if self.can_place(ship):
                self.add_ship(ship)
                break

    def check_hit(self, target):
        for ship in self.ships:
            if target in ship.dots():
                ship.hits.add(target)
                if len(ship.hits) == ship.length:
                    return "sunk"
                return "hit"
        return "miss"

    def update(self, target, result):
        x = target.x - 1
        y = target.y - 1
        if result == "sunk":
            self.board[y][x] = "X"
        elif result == "hit":
            self.board[y][x] = "X"
        else:
            self.board[y][x] = "T"

    def all_ships_sunk(self):
        for ship in self.ships:
            if len(ship.hits) != ship.length:
                return False
        return True

class Player:
    def __init__(self):
        self.board = Board()

    def place_ships(self):
        ship_lengths = [3, 3, 2, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            self.board.random_place(length)

    def get_target(self):
        while True:
            coords = input("Введите координаты выстрела (например, 11): ")
            if len(coords) != 2 or not coords.isdigit():
                print("Некорректные координаты! Попробуйте снова.")
                continue
            x = int(coords[0])
            y = int(coords[1])
            if x < 1 or x > 6 or y < 1 or y > 6:
                print("Некорректные координаты! Попробуйте снова.")
                continue
            return Dot(x, y)

class Computer:
    def __init__(self):
        self.board = Board()

    def place_ships(self):
        ship_lengths = [3, 3, 2, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            self.board.random_place(length)

    def get_target(self):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        print("Компьютер выстрелил в точку:", x, y)
        return Dot(x, y)

class Game:
    def __init__(self):
        self.player = Player()
        self.computer = Computer()

    def start(self):
        print("Расстановка кораблей игрока:")
        self.player.place_ships()
        print("Расстановка кораблей компьютера:")
        self.computer.place_ships()

        print("Поле игрока:")
        self.player.board.show(hide_ships=True)

        print("Поле компьютера:")
        self.computer.board.show(hide_ships=True)
        # self.computer.board.show()

        while True:
            # Ход игрока
            print("Ваш ход:")
            target = self.player.get_target()
            result = self.computer.board.check_hit(target)
            self.player.board.update(target, result)
            # self.player.board.show()
            self.player.board.show(hide_ships=True)
            if result == "sunk":
                print("Вы потопили корабль соперника!")
            elif result == "hit":
                print("Вы попали по кораблю соперника!")
            elif result == "miss":
                print("Вы промахнулись!")
            if self.computer.board.all_ships_sunk():
                print("Вы победили!")
                break

            # Ход компьютера
            print("Ход компьютера:")
            target = self.computer.get_target()
            result = self.player.board.check_hit(target)
            self.computer.board.update(target, result)
            self.computer.board.show(hide_ships=True)
            if result == "sunk":
                print("Корабль компьютера потоплен!")
            elif result == "hit":
                print("Компьютер попал по вашему кораблю!")
            elif result == "miss":
                print("Компьютер промахнулся!")
            if self.player.board.all_ships_sunk():
                print("Компьютер победил!")
                break

if __name__ == "__main__":
    game = Game()
    game.start()