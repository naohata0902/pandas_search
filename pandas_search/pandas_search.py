from __future__ import annotations
from collections.abc import Generator
import pandas as pd
import re
from logging import config, getLogger
from lib import Area, Cell

config.fileConfig("logging.conf")
logger = getLogger()


class PandasSearch:
    """
    this class gives functions to get data from pandas dataframe
    using by regular expression  
    """
    def __init__(self, df: pd.DataFrame):
        logger.info("create an instance of PandasSearch")
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
        logger.info("start is_match")
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
        logger.info("start search")
        logger.debug(f"{word=}, {top_left_cell=}, {bottom_right_cell=}, {exact_match=}")
        if exact_match:
            word = f"^{word}$"
        npdf = self.df.astype(str).to_numpy()
        area = Area(self.df, top_left_cell, bottom_right_cell)
        logger.debug(f"{area=}")

        for ir in range(area.top_left_cell.row, area.bottom_right_cell.row + 1):
            for ic in range(area.top_left_cell.col, area.bottom_right_cell.col + 1):
                cell_val = npdf[ir, ic]
                if self.is_match(cell_val, word):
                    logger.debug(f"{ir=}, {ic=}")
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
            (pd.DataFrame): 
        """
        logger.info("start peek")
        target_dfs = []
        for cell in searched_cells:
            logger.debug(f"{cell=}")
            searched_cell = Cell(*cell)

            top_left_cell = searched_cell + shift
            bottom_right_cell = self.calc_bottom_right_cell(top_left_cell,
                                                            target_size)
            logger.debug(f"{top_left_cell.val=}, {bottom_right_cell.val=}")

            target_dfs.append(self.df.iloc[top_left_cell.row:bottom_right_cell.row + 1,
                                           top_left_cell.col:bottom_right_cell.col + 1])


        return target_dfs

    def calc_bottom_right_cell(self, top_left_cell: Cell,
                               target_size: tuple[int, int]) -> Cell:
        """
        if target_size is less than zero,
        the value shows the number of cell from the end of row/column
        so calculate bottom right cell position by considering the value
        Parameter:
            top_left_cell(Cell): top left cell position of target area
            target_size(tuple[int, int]): the width and hight of the target_area
        Return:
            (Cell): bottom right cell position
        """
        size_row, size_col = target_size
        row = self.get_bottom_right_cell_value(top_left_cell.row, self.nr - 1, size_row)
        col = self.get_bottom_right_cell_value(top_left_cell.col, self.nc - 1, size_col)
        logger.debug(f"{row=}, {col=}")

        return Cell(row, col)
    
    def get_bottom_right_cell_value(self, start_position: int,
                               max_position: int,size: int) -> int:
        """
        get the value of bottom_right cell's row or column value
        this is used in calc_bottom_right_cell function
        Parameter: 
            start_position(int): number of top_left_cell row of column of target_area
            max_position(int): last row number or last column number
            size(int): given size value
        Return:
            (int): real bottom_right_cell's row or column value
        """
        if size < 0:
            return max_position + size + 1
        elif size > max_position - start_position + 1:
            return max_position
        else:
            return start_position + size - 1

