def print_board(board):
    print("   0   1   2")
    for i, row in enumerate(board):
        print(f"{i}  {' | '.join(row)}")
        if i < 2:
            print("  " + "-" * 11)


def check_winner(board):
    # Проверка строк
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]

    # Проверка столбцов
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]

    # Проверка диагоналей
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)

        # Запрос хода у текущего игрока
        row = int(input("Выберите строку (0-2): "))
        col = int(input("Выберите столбец (0-2): "))

        # Проверка на корректность хода
        if board[row][col] != " ":
            print("Недопустимый ход. Попробуйте снова.")
            continue

        # Запись хода на доску
        board[row][col] = current_player

        # Проверка на победителя или ничью
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Игрок {winner} победил!")
            break
        elif all(board[row][col] != " " for row in range(3) for col in range(3)):
            print_board(board)
            print("Ничья!")
            break

        # Смена игрока
        current_player = "O" if current_player == "X" else "X"

# Запуск игры
play_game()