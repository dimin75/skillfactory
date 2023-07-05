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
# метод выбора стартовой точки размещения и направления размещения (вертикально или горизонтально)

    def place(self, start_dot, direction):
        self.bow = start_dot
        self.direction = direction
# метод размещения кораблей по клеткам вертикально или горизонтально от стартовой точки по длине
# и ориентации - вертикальной или горизонтальной

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
    def __init__(self, size=6):
        self.size = size
        self.board = [["O"] * size for _ in range(size)]
        self.ships = []

# метод перезагрузки/обнуления содержания массива с расстановкой кораблей
    def reset(self):
        self.ships = []
        self.hits = set()
        self.board = [["O"] * self.size for _ in range(self.size)]

# метод демонстрации поля (hide_ships=True - корабли спрятаны под символом "O")
    def show(self, hide_ships=False):
        print("  1 2 3 4 5 6")
        for i, row in enumerate(self.board):
            row_str = " ".join(row) if not hide_ships else " ".join([c if c != "■" else "O" for c in row])
            print(i + 1, row_str)
# метод выделения потопленного корабля путем обведения по контуру символом "."

    def contour(self, ship):
        for dot in ship.dots():
            x = dot.x - 1
            y = dot.y - 1
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if self.board[ny][nx] != "■" and self.board[ny][nx] != "X":
                            self.board[ny][nx] = "."
# метод добавления корабля на поле

    def add_ship(self, ship):
        for dot in ship.dots():
            x = dot.x - 1
            y = dot.y - 1
            self.board[y][x] = "■"
        self.ships.append(ship)
# метод проверки выхода за границы игрового поля

    def out_of_range(self, dot):
        return dot.x < 1 or dot.x > self.size or dot.y < 1 or dot.y > self.size
# метод проверки наложение нового корабля на уже расставленные

    def overlapping(self, ship):
        for added_ship in self.ships:
            for dot in ship.dots():
                if dot in added_ship.dots():
                    return True
        return False

    # метод проверки расстояния не менее одной клетки до ближайшего корабля
    def cell_touch(self, ship):
        if len(self.ships) == 0:
            return False
        for presented_ship in self.ships:
            for dot in ship.dots():
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        x = dot.x + dx
                        y = dot.y + dy
                        for p_dot in presented_ship.dots():
                            if p_dot.x == x and p_dot.y == y:
                                return True
        return False

# проверка, можно ли поместить корабль в данную позицию
    def can_place(self, ship):
        # проверка расстояния не менее одной клетки до ближайшего корабля
        if self.cell_touch(ship):
            return False
        for dot in ship.dots():
            # проверка выхода за пределы поля и наложения на расставленные корабли
            if self.out_of_range(dot) or self.overlapping(ship):
                return False
        return True
# метод случайного размещения кораблей на игровом поле

    def random_place(self, player, length):
        place_attempts = 0
        ship_placed = 0
        # При случайной расстановке кораблей может возникнуть случай, когда цикл перебора позиций будет бесконечным:
        # Ограничиваем количество попыток рассатановки в 10000 попыток. Если нет результата, начинаем расстановку
        # сначала - используем метод board.reset()
        max_attempts = 10000

        while True:
            x = random.randint(1, self.size)
            y = random.randint(1, self.size)
            direction = random.choice(["H", "V"])
            ship = Ship(length, Dot(x, y), direction)
            place_attempts += 1

            if self.can_place(ship):
                self.add_ship(ship)
                ship_placed += 1
                print("Ship placed:", ship_placed)
                break

            if place_attempts >= max_attempts:
                print("Слишком много попыток расстановки. Пробуем заново...")
                self.reset()  # Reset the board and ships
                if isinstance(player, Computer):
                    player.place_ships()  # Retry ship placement using the Computer instance
                if isinstance(player, Player):
                    player.place_ships()  # Retry ship placement using the Computer instance
                break

            print("Попытка расстановки: ", place_attempts, "Кораблей расставлено: ", ship_placed)

# проверить, попал ли выстрел по кораблю и какие последствия (мимо (miss), попал (hit), утонул (miss))
    def check_hit(self, target):
        for ship in self.ships:
            if target in ship.dots():
                ship.hits.add(target)
                # if len(ship.hits) == len(ship.dots()):
                if len(ship.hits) == ship.length:
                    self.contour(ship)
                    return "sunk"
                return "hit"
        return "miss"
# обновление поля после выстрела

    def update(self, target, result):
        x = target.x - 1
        y = target.y - 1
        if result == "sunk":
            self.board[y][x] = "X"
        elif result == "hit":
            self.board[y][x] = "X"
        else:
            self.board[y][x] = "T"
# событие - все корабли игрока потоплены

    def all_ships_sunk(self):
        for ship in self.ships:
            if len(ship.hits) != ship.length:
                return False
        return True


class Player:
    def __init__(self):
        self.board = Board()
# размещение кораблей

    def place_ships(self):
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            self.board.random_place(self, length)
# пристрелка игрока по полю компьютера

    def get_target(self):
        while True:
            coords = input("Введите координаты выстрела (в формате <столбец ряд> например, 11): ")
            if len(coords) != 2 or not coords.isdigit():
                print("Некорректные координаты! Попробуйте снова.")
                continue
            x = int(coords[0])
            y = int(coords[1])
            if x < 1 or x > self.board.size or y < 1 or y > self.board.size:
                print("Некорректные координаты! Попробуйте снова.")
                continue
            return Dot(x, y)


class Computer:
    def __init__(self):
        self.board = Board()
# размещение кораблей компьютера

    def place_ships(self):
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            self.board.random_place(self, length)
# стрельба компьютера

    def get_target(self):
        x = random.randint(1, self.board.size)
        y = random.randint(1, self.board.size)
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
        self.player.board.show()

        print("Поле компьютера:")
        self.computer.board.show(hide_ships=True)
        # Для теста расстановки кораблей раскомментить строку ниже и закомментить строку выше.
        # self.computer.board.show()

        while True:
            # Ход игрока
            print("Ваш ход:")
            target_player = self.player.get_target()
            result_player = self.computer.board.check_hit(target_player)
            print("Поле игрока:")
            if result_player == "sunk":
                print("Вы потопили корабль соперника!")

            # elif result == "hit":
            elif result_player == "hit":
                print("Вы попали по кораблю соперника!")
            # elif result == "miss":
            elif result_player == "miss":
                print("Вы промахнулись!")
            if self.computer.board.all_ships_sunk():
                print("Game Over!")
                self.player.board.update(target_computer, result_computer)
                self.player.board.show()
                self.computer.board.update(target_player, result_player)
                self.computer.board.show()
                print("Вы победили!")
                break

            # Ход компьютера
            print("Ход компьютера:")
            target_computer = self.computer.get_target()
            result_computer = self.player.board.check_hit(target_computer)
            self.player.board.update(target_computer, result_computer)
            self.player.board.show()
            self.computer.board.update(target_player, result_player)
            print("Поле компьютера:")
            # Рабочий вариант показа доски компьютера
            self.computer.board.show(hide_ships=True)
            # Для теста расстановки кораблей раскомментить строку ниже и закомментить строку выше.
            # self.computer.board.show()
            if result_computer == "sunk":
                print("Корабль компьютера потоплен!")
            # elif result == "hit":
            elif result_computer == "hit":
                print("Компьютер попал по вашему кораблю!")
            # elif result == "miss":
            elif result_computer == "miss":
                print("Компьютер промахнулся!")
            if self.player.board.all_ships_sunk():
                print("Game Over!")
                self.player.board.update(target_computer, result_computer)
                self.player.board.show()
                self.computer.board.update(target_player, result_player)
                self.computer.board.show()
                print("Компьютер победил!")
                break


if __name__ == "__main__":
    game = Game()
    game.start()
