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
        # cell_weight as described in stragegy_pdf
        self.cell_weight = ((3, 2, 3), (2, 4, 2), (3, 2, 3))
        self.small_board_heuristic = {}
        self.big_board_heuristic = {}
        patterns = []

        #rows , columns and diagonals
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
        if old_move == (-1, -1, -1):
            # return move directly
            # add to hash
            print 1
        else:
            # if previous move belonged to opponent, add it to hash
            print 0

        self.turn = flag
        max_depth = 4
        start_time = time.time()

        valid_moves = board.find_valid_move_cells(old_move)
        best_move = valid_moves[0]

        try:
            while time.time() - start_time > 10:
                print time.time() - start_time
                board_copy = copy.deepcopy(board)
                best_move = self.minimax(board_copy, float("-inf"), float("inf"), flag, 0, max_depth, old_move)[1]
                max_depth += 1
                del board_copy
        except Exception as e:
            pass

        return best_move

    def minimax(self, board, alpha, beta, flag, current_depth, max_depth, old_move):
        valid_moves = board.find_valid_move_cells(old_move)

        if current_depth == max_depth:
            return rand(30), -2
        
        if flag == self.who:
            max_utility = float("-inf")
            move_ind = 0
            num_moves = len(valid_moves)

            for i in xrange(num_moves):
                current_move = valid_moves[i]
                board.update(old_move, current_move, flag)

                node_val = self.minimax(board, alpha, beta, opponent_marker(flag), current_depth+1, max_depth, current_move)

                if node_val > max_utility:
                    max_utility = node_val
                    move_ind = i
                else:
                    alpha = max_utility

                board.big_boards_status[current_move[0]][current_move[1]][current_move[2]] = '-'
                board.small_boards_status[current_move[0]][current_move[1]/3][current_move[2]/3] = '-'
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

                node_val = self.minimax(board, alpha, beta, opponent_marker(flag), current_depth+1, max_depth, current_move)

                if node_val < min_utility:
                    min_utility = node_val
                    move_ind = i
                else:
                    beta = min_utility
                if beta <= alpha:
                    break
            return min_utility, valid_moves[move_ind]
