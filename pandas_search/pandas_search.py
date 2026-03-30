from __future__ import annotations
from collections.abc import Generator
from pathlib import Path
import pandas as pd
import re
from logging import config, getLogger
from pandas_search.lib import Area
import numpy as np

current_filepath = Path(__file__).resolve().parent
config.fileConfig(current_filepath.joinpath("logging.conf"))
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
        self.match_func = self.is_match

    def set_match_function(self, my_func: callable) -> None:
        self.match_func = my_func

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
               rows: tuple[int, int, int] = (None, None, None),
               cols: tuple[int, int, int] = (None, None, None),
               ) -> Generator[tuple[int, int], None, None]:
        """
        this gives the cell position matching to the regular expression
        in the area defined by top_left_cell and bottom_right_cell
        Parameter:
            word(str): key word which we want to find.
                        It is defined by regular expression
            rows(tuple[int, int, int]):
            cols(tuple[int, int, int]):
        retrun:
            Generator: it shows cell position which is matched by regular expression
        """
        logger.info("start search")
        logger.debug(f"{word=}, {rows=}, {cols=}")
        # npdf = self.df.astype(str).to_numpy()
        area = Area(rows, cols)
        searched_df = area.extract(self.df)
        logger.debug(f"{area=}")

        # 1. インデックスを0からの整数に振り直す
        df_ = df.reset_index(drop=True)

        # 2. カラムを0からの整数に振り直す
        df_.columns = range(len(df_.columns))

        # スライスでDataFrameを抽出
        df__ = df_.iloc[0, 3, :] # dfを抽出

        # スライスしたDataFrame上で 条件に合う座標を抽出
        rows, cols = np.where(searched_df.map(self.match_func))

        # 抽出した座標のインデックスとカラムを取得する
        coords = zip(searched_df.index[rows], searched_df.columns[cols])
        
        return coords

    def rsearch(self, word: str,
                rows: list[int, int],
                exact_match: bool = False
               ) -> Generator[tuple[int, int], None, None]:
        """
        this gives the cell position matching to the regular expression
        in the area defined by rows
        """
        yield from self.search(word, (rows[0], 0), (rows[1], -1), exact_match)

    def csearch(self, word: str,
                cols: list[int, int],
                exact_match: bool = False
               ) -> Generator[tuple[int, int], None, None]:
        """
        this gives the cell position matching to the regular expression
        in the area defined by cols
        """
        yield from self.search(word, (0, cols[0]), (-1, cols[1]), exact_match)

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

