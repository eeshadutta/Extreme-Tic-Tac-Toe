'''
Team 25
'''

import datetime
import time
import copy
import random


class Team25:
    '''
    Main class containing all functions pertaining to the bot
    '''

    def __init__(self):
        self.cell_weight = ((3, 2, 3), (2, 4, 2), (3, 2, 3))
        self.global_rand_table = [
            [[long(0) for k in xrange(2)] for i in xrange(9)] for j in xrange(9)]
        self.small_board_heuristic = {}
        self.total_board_hash = long(0)
        self.big_board_heuristic = {}
        self.total_heuristic = {}
        self.big_board_hash = [long(0), long(0)]
        self.small_board_hash = ([[long(0) for i in range(3)] for j in range(3)], [
                                 [long(0) for i in range(3)] for j in range(3)])
        self.max_nodes = 1e5 + 5000
        self.nodes_explored = 0
        patterns = []
        self.start_time = 0
        self.time_limit = datetime.timedelta(seconds=20)

        # rows , columns and diagonals
        for i in xrange(3):
            row_arr = []
            for j in xrange(3):
                row_arr.append((i, j))
            patterns.append(tuple(row_arr))

        for i in xrange(3):
            col_arr = []
            for j in xrange(3):
                col_arr.append((j, i))
            patterns.append(tuple(col_arr))

        self.global_hash()

        diag_arr1 = []
        diag_arr1.append((0, 2))
        diag_arr1.append((1, 1))
        diag_arr1.append((2, 0))
        patterns.append(tuple(diag_arr1))

        diag_arr2 = []
        diag_arr2.append((0, 0))
        diag_arr2.append((1, 1))
        diag_arr2.append((2, 2))
        patterns.append(tuple(diag_arr2))

        self.patterns = tuple(patterns)

    def opponent_marker(self, flag):
        if flag == 'x':
            return 'o'
        else:
            return 'x'

    def move(self, board, old_move, flag):
        self.start_time = datetime.datetime.utcnow()
        # self.time_limit = datetime.timedelta(seconds = 22)
        if old_move == (-1, -1, -1):
            self.update_hash((0, 4, 4), 1)
            return (0, 4, 4)
        
        self.turn = flag

        if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.opponent_marker(flag):
            self.update_hash(old_move, 0)


        valid_moves = board.find_valid_move_cells(old_move)
        best_move = valid_moves[0]

        max_depth = 3
        while datetime.datetime.utcnow() - self.start_time < self.time_limit:
            board_copy = copy.deepcopy(board)
            (temp_val, temp_move) = self.minimax(board_copy, float(
                "-inf"), float("inf"), flag, 0, max_depth, old_move)
            if temp_val != -111:
                best_move = temp_move
            max_depth += 1
            print max_depth
            print datetime.datetime.utcnow() - self.start_time
            del board_copy

        self.update_hash(best_move, 1)

        return best_move

    def minimax(self, board, alpha, beta, flag, current_depth, max_depth, old_move):
        if datetime.datetime.utcnow() - self.start_time > self.time_limit:
            return -111, (-1, -1, -1)

        check_goal_state = board.find_terminal_state()

        if check_goal_state[1] == 'WON':
            if check_goal_state[0] == self.turn:
                return float("inf"), -1000
            else:
                return float("-inf"), -1000
        elif check_goal_state[1] == 'DRAW':
            return -100000, -1000

        if current_depth == max_depth:
            if (self.total_board_hash, flag) in self.total_heuristic:
                return self.total_heuristic[(self.total_board_hash, flag)], -2
            return (self.heuristic(board, 0, flag) + self.heuristic(board, 1, flag)), -2

        valid_moves = board.find_valid_move_cells(old_move)
        random.shuffle(valid_moves)

        if flag == self.turn:
            max_utility = float("-inf")
            move_ind = 0
            num_moves = len(valid_moves)

            for i in xrange(num_moves):
                current_move = valid_moves[i]
                board.update(old_move, current_move, flag)
                self.update_hash(current_move, 1)

                node_val = self.minimax(board, alpha, beta, self.opponent_marker(
                    flag), current_depth+1, max_depth, current_move)[0]
                if datetime.datetime.utcnow() - self.start_time > self.time_limit:
                    board.big_boards_status[current_move[0]
                                            ][current_move[1]][current_move[2]] = '-'
                    board.small_boards_status[current_move[0]
                                              ][current_move[1]/3][current_move[2]/3] = '-'
                    self.update_hash(current_move, 1)
                    return -111, (-1, -1, -1)

                if node_val > max_utility:
                    max_utility = node_val
                    move_ind = i
                if max_utility > alpha:
                    alpha = max_utility

                board.big_boards_status[current_move[0]
                                        ][current_move[1]][current_move[2]] = '-'
                board.small_boards_status[current_move[0]
                                          ][current_move[1]/3][current_move[2]/3] = '-'
                self.update_hash(current_move, 1)

                if beta <= alpha:
                    break

            return max_utility, valid_moves[move_ind]
        else:
            min_utility = float("inf")
            move_ind = 0
            num_moves = len(valid_moves)

            for i in xrange(num_moves):
                current_move = valid_moves[i]
                board.update(old_move, current_move, flag)
                self.update_hash(current_move, 0)

                node_val = self.minimax(board, alpha, beta, self.opponent_marker(
                    flag), current_depth+1, max_depth, current_move)[0]
                if datetime.datetime.utcnow() - self.start_time > self.time_limit:
                    board.big_boards_status[current_move[0]
                                            ][current_move[1]][current_move[2]] = '-'
                    board.small_boards_status[current_move[0]
                                              ][current_move[1]/3][current_move[2]/3] = '-'
                    self.update_hash(current_move, 1)
                    return -111, (-1, -1, -1)

                if node_val < min_utility:
                    min_utility = node_val
                    move_ind = i
                if min_utility < beta:
                    beta = min_utility

                board.big_boards_status[current_move[0]
                                        ][current_move[1]][current_move[2]] = '-'
                board.small_boards_status[current_move[0]
                                          ][current_move[1]/3][current_move[2]/3] = '-'
                self.update_hash(current_move, 0)

                if beta <= alpha:
                    break

            return min_utility, valid_moves[move_ind]

    def heuristic(self, board, big_board_num, flag):
        # if that board hash is precomputed, then return else calculate
        if (self.big_board_hash[big_board_num], flag) in self.big_board_heuristic:
            return self.big_board_heuristic[(self.big_board_hash[big_board_num], flag)]

        utility = 0

        # the status of the big board
        decision_board = board.small_boards_status[big_board_num]
        play_board = board.big_boards_status[big_board_num]
        # decision_board_heuristics = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        decision_board_heuristics = [[long(0) for i in xrange(3)] for j in xrange(3)]

        for i in xrange(3):
            for j in xrange(3):
                if decision_board[i][j] == flag:
                    decision_board_heuristics[i][j] = 30
                elif decision_board[i][j] == self.opponent_marker(flag):
                    decision_board_heuristics[i][j] = -1
                elif decision_board[i][j] == 'd':
                    decision_board_heuristics[i][j] = -1
                else:
                    small_play_board = tuple(
                        [tuple(play_board[3*i + x][3*j:3*(j+1)]) for x in xrange(3)])
                    # if that small board hash is precomputed, then return else calculate
                    if (self.small_board_hash[big_board_num][i][j], flag) in self.small_board_heuristic:
                        decision_board_heuristics[i][j] = self.small_board_heuristic[(
                            self.small_board_hash[big_board_num][i][j], flag)]
                    else:
                        decision_board_heuristics[i][j] = self.compute_small_board_heuristic(
                            small_play_board, flag)
                        self.small_board_heuristic[(
                            self.small_board_hash[big_board_num][i][j], flag)] = decision_board_heuristics[i][j]

        for pattern in self.patterns:
            count = self.pattern_checker(decision_board, pattern, flag)

            if count == 2:
                utility += 2 * 60
            if count == 3:
                utility += 100 * 60

        for i in xrange(3):
            for j in xrange(3):
                utility += decision_board_heuristics[i][j] * \
                    self.cell_weight[i][j]

        self.big_board_heuristic[(
            self.big_board_hash[big_board_num], flag)] = utility

        return utility

    def compute_small_board_heuristic(self, small_play_board, flag):
        small_play_board_heuristic = 0

        for i in xrange(3):
            for j in xrange(3):
                if small_play_board[i][j] == flag:
                    small_play_board_heuristic += 0.1 * self.cell_weight[i][j]

        for pattern in self.patterns:
            count = self.pattern_checker(small_play_board, pattern, flag)

            if count == 2:
                small_play_board_heuristic += 10

        return small_play_board_heuristic

    def pattern_checker(self, small_board, pattern, flag):
        count = 0
        
        for pos in pattern:
            x = pos[0]
            y = pos[1]
            if small_board[x][y] == self.opponent_marker(flag):
                return 0
            elif small_board[x][y] == flag:
                count += 1

        return count


    def global_hash(self):
        for i in xrange(9):
            for j in xrange(9):
                for k in xrange(2):
                    self.global_rand_table[i][j][k] = long(
                        random.randint(1, 2**64))

    def update_hash(self, current_move, flag):
        board_num = current_move[0]

        self.total_board_hash ^= self.global_rand_table[current_move[1]][current_move[2]][flag]
        self.big_board_hash[board_num] ^= self.global_rand_table[current_move[1]][current_move[2]][flag]
        self.small_board_hash[board_num][current_move[1]/3][current_move[2] /3] ^= self.global_rand_table[current_move[1]][current_move[2]][flag]
