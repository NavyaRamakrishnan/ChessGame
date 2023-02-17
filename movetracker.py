class MoveTracker:
    
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    # equals function for when comparing two MoveTracker objects together
    def __eq__(self, other):
       return self.start == other.start and self.end == other.end

