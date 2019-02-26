'''
Team 25
'''

import datetime
import copy
import random

class Team25:
    '''
    Main class containing all functions pertaining to the bot
    '''

    def __init__(self):
        self.cell_weight = ((3,2,3) , (2,4,2) , (3,2,3))   #cell_weight as described in stragegy_pdf
        self.small_board_heuristic = {}
        self.big_board_heuristic = {}
        patterns = []

        #rows , columns and diagonals
        for i in xrange(3):
            row_arr = []
            for j in xrange(3):
                row_arr.append((i,j))                            
            patterns.append(tuple(row_arr))

        for i in xrange(3):
            col_arr = []
            for j in xrange(3):
                col_arr.append((j,i))                            
            patterns.append(tuple(col_arr))
            
        diag_arr1 = []
        diag_arr1.append((0,2))
        diag_arr1.append((1,1))
        diag_arr1.append((2,0))
        patterns.append(tuple(diag_arr1))

        diag_arr2 = []
        diag_arr2.append((0,0))
        diag_arr2.append((1,1))
        diag_arr2.append((2,2))
        patterns.append(tuple(diag_arr2))
        
        self.patterns = tuple(patterns)
    

    def opponent_marker(self,flag):
        if flag == 'x':
            return 'o'
        else:
            return 'x'

    def heuristic(self,board):
