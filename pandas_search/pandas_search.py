from __future__ import annotations
from collections.abc import Generator
import pandas as pd
import re

from .area import Area

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
        
    def search(self, regex: str,
               top_left_cell: tuple[int, int] = (0, 0),
               bottom_right_cell: tuple[int, int] = (-1, -1)
               ) -> Generator[tuple[int, int], None, None]:
        """
        this gives the cell position matching to the regular expression
        in the area defined by top_left_cell and bottom_right_cell
        Parameter:
            regex(str): key word which we want to find.
                        It is defined by regular expression
            top_left_cell(tuple[int, int]):
                top left cell position in any area within the target dataframe
            bottom_right_cell(tuple[int, int]):
                bottom right cell position in any area within the target dataframe
        retrun:
            Generator: it shows cell position which is matched by regular expression
        """
        npdf = self.df.astype(str).to_numpy()
        area = Area(self.df, top_left_cell, bottom_right_cell)

        for ir in range(area.top_left_cell.r, area.bottom_right_cell.r + 1):
            for ic in range(area.top_left_cell.c, area.bottom_right_cell.c + 1):
                cell_val = npdf[ir, ic]
                if self.is_match(cell_val, regex):
                    yield (ir, ic)

    def peek(self,
              searched_cells: Generator,
              shift: tuple[int, int] = (0, 0),
              target_size: tuple[int, int] = (1,1)):
        """
        """
        for cell in searched_cells:
            i_r, i_c = cell

            target_cell = self.add_tuple(cell, shift)
            target_cell = self.add_tuple(target_cell, target_size)
            target_cell = self.add_tuple(target_cell, (-1, -1))
            print(f"position : {cell}, val:{self.df.iloc[*target_cell]}")

        return "answer"
    
    def add_tuple(self, cell_a: tuple, cell_b: tuple) -> tuple:
        ar, ac = cell_a
        br, bc = cell_b
        
        return (ar + br, ac + bc)
    
    