from __future__ import annotations
from collections.abc import Generator
import pandas as pd
import re

from lib import Area, Cell

class PandasSearch:
    """
    this class gives functions to get data from pandas dataframe
    using by regular expression  
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.nr, self.nc = df.shape

    def is_match(self, value: str, expression: str) -> bool:
        """
        can_match shows if the value matches to the given expression
        parameter:
            value(str): searched word
            expression(str): regular expression to search
        retrun:
            boolean
        """
        
        try:
            m = re.search(expression, value)
        except re.error:
           raise re.error(f"regular expression must be proper: {expression}")
        if m is None:
            return False
        else:
            return True
        
    def search(self, word: str,
               top_left_cell: tuple[int, int] = (0, 0),
               bottom_right_cell: tuple[int, int] = (-1, -1),
               exact_match: bool = False
               ) -> Generator[tuple[int, int], None, None]:
        """
        this gives the cell position matching to the regular expression
        in the area defined by top_left_cell and bottom_right_cell
        Parameter:
            word(str): key word which we want to find.
                        It is defined by regular expression
            top_left_cell(tuple[int, int]):
                top left cell position in any area within the target dataframe
            bottom_right_cell(tuple[int, int]):
                bottom right cell position in any area within the target dataframe
            exact_match(bool): default is Fault. this shows matching type
                if you want to search word by exact match, this is set by True
        retrun:
            Generator: it shows cell position which is matched by regular expression
        """
        if exact_match:
            word = f"^{word}$"
        npdf = self.df.astype(str).to_numpy()
        area = Area(self.df, top_left_cell, bottom_right_cell)

        for ir in range(area.top_left_cell.row, area.bottom_right_cell.row + 1):
            for ic in range(area.top_left_cell.col, area.bottom_right_cell.col + 1):
                cell_val = npdf[ir, ic]
                if self.is_match(cell_val, word):
                    yield (ir, ic)

    def peek(self,
              searched_cells: Generator,
              shift: tuple[int, int] = (0, 0),
              target_size: tuple[int, int] = (1,1)) -> list:
        """
        this gives the data at the area which is based on the searched word
        the area is far from discance which is defined by 'shift'
        and size is defined by 'target_size'
        Parameter:
            shift(tuple[int, int]):
                this shows a vector which means distance and direction
                from the searched word 
            target_size(typle[int, int]):
                this shows the size of target area shown by row and column
        Return:
            (pd.DataFrame)
        """
        target_dfs = []
        for cell in searched_cells:
            searched_cell = Cell(*cell)

            top_left_cell = searched_cell + shift
            bottom_right_cell = self.calc_bottom_right_cell(top_left_cell,
                                                            target_size)
            print(f"top_left_cell:{top_left_cell}, bottom_right_cell:{bottom_right_cell}")

            target_dfs.append(self.df.iloc[top_left_cell.row:bottom_right_cell.row,
                                           top_left_cell.col:bottom_right_cell.col])


        return target_dfs

    def calc_bottom_right_cell(self, top_left_cell: Cell,
                               size: tuple[int, int]) -> Cell:
        """
        """
        size_row, size_col = size
        if size_row < 0:
            row = self.nr + size_row - top_left_cell.row + 1
        else:
            row = top_left_cell.row + size_row
        if size_col < 0:
            col = self.nc + size_col - top_left_cell.col + 1
        else:
            col = top_left_cell.col + size_col

        return Cell(row, col)