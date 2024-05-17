import heapq
import math

class TicTacToeNode:
    def __init__(self, board, player, move=None):
        self.board = board
        self.player = player
        self.move = move

    def __lt__(self, other):
        return False

    @staticmethod
    def print_board(board):
        for row in board:
            print(" ".join(row))
        print()

    @staticmethod
    def is_winner(board, player):
        for i in range(3):
            if all(cell == player for cell in board[i]) or all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or all(board[i][i - 2] == player for i in range(3)):
            return True
        return False

    @staticmethod
    def is_board_full(board):
        return all(cell != ' ' for row in board for cell in row)

    @staticmethod
    def game_over(board):
        for player in ['X', 'O']:
            if TicTacToeNode.is_winner(board, player):
                return True, player
        if TicTacToeNode.is_board_full(board):
            return True, 'Tie'
        return False, None

    @staticmethod
    def heuristic(board, player):
        score = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == 'O':
                    score += 1
                elif board[i][j] == 'X':
                    score -= 1
        return score

    @staticmethod
    def a_star_search(initial_node):
        open_set = []
        closed_set = set()

        heapq.heappush(open_set, (TicTacToeNode.heuristic(initial_node.board, initial_node.player), initial_node))

        while open_set:
            _, current_node = heapq.heappop(open_set)

            if TicTacToeNode.game_over(current_node.board)[0]:
                return current_node

            closed_set.add(tuple(map(tuple, current_node.board)))

            for i in range(3):
                for j in range(3):
                    if current_node.board[i][j] == ' ':
                        new_board = [row[:] for row in current_node.board]
                        new_board[i][j] = current_node.player
                        new_player = 'X' if current_node.player == 'O' else 'O'
                        child_node = TicTacToeNode(new_board, new_player, move=(i, j))

                        if tuple(map(tuple, child_node.board)) not in closed_set:
                            heapq.heappush(open_set, (TicTacToeNode.heuristic(child_node.board, child_node.player), child_node))
        return None

    def play_tic_tac_toe(self):
        board = [[' ' for _ in range(3)] for _ in range(3)]

        while not self.game_over(board)[0]:
            self.print_board(board)

            row = int(input("Enter row (0, 1, or 2): "))
            col = int(input("Enter column (0, 1, or 2): "))

            if board[row][col] == ' ':
                board[row][col] = 'X'
            else:
                print("Cell already occupied. Try again.")
                continue

            if self.game_over(board)[0]:
                break

            print("AI's Move : ")
            ai_node = self.a_star_search(TicTacToeNode(board, 'O'))
            ai_row, ai_col = ai_node.move
            board[ai_row][ai_col] = 'O'

        self.print_board(board)
        result = self.game_over(board)[1]
        if result == 'Tie':
            print("It's a tie")
        else:
            print(f"{result} wins")

if __name__ == "__main__":
  initial_board = [[' ' for _ in range(3)] for _ in range(3)]
  initial_player = 'X'
  game = TicTacToeNode(initial_board, initial_player)
  game.play_tic_tac_toe()
