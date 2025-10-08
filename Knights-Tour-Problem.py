def is_safe(x, y, board, n):
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1

def print_solution(board, n):
    path = []
    for i in range(n):
        for j in range(n):
            path.append((i, j, board[i][j]))
    path.sort(key=lambda x: x[2])  

    for (x, y, _) in path:
        print(f"{x} {y}")


def solve_knight_tour(n, start_x, start_y):
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    board = [[-1 for _ in range(n)] for _ in range(n)]

    board[start_x][start_y] = 0

    def backtrack(x, y, move_i):
        if move_i == n * n:
            return True

        for i in range(8):
            next_x = x + move_x[i]
            next_y = y + move_y[i]
            if is_safe(next_x, next_y, board, n):
                board[next_x][next_y] = move_i
                if backtrack(next_x, next_y, move_i + 1):
                    return True
                board[next_x][next_y] = -1
        return False

    if not backtrack(start_x, start_y, 1):
        print("Tidak ada solusi.")
    else:
        print_solution(board, n)

if __name__ == "__main__":
    n, m = map(int, input().split())
    start_x, start_y = map(int, input().split())

    print("\nUrutan langkah kuda (Knight's Tour):")
    solve_knight_tour(n, start_x, start_y)
