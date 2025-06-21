import pandas as pd
from .cell import Cell

class Area:
    """
    Area class shows rectangle area which is defined 
    by top_left cell and bottom_right cell
    """

    def __init__(self,
                df: pd.DataFrame,
                top_left:tuple[int, int],
                bottom_right: tuple[int, int]):
        self.df = df
        self.nr, self.nc = df.shape
        self.top_left_cell = Cell(*top_left)
        self.bottom_right_cell = Cell(*bottom_right)
        self.conv()
        self.check()

    @property
    def val(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        this gives the area coordinates which is converted and checked
        """
        return (self.top_left_cell.val, self.bottom_right_cell.val)

    def conv(self):
        if self.top_left_cell.row < 0:
            self.top_left_cell.row = self.nr + self.top_left_cell.row
        if self.top_left_cell.col < 0:
            self.top_left_cell.col = self.nc + self.top_left_cell.col
        self.top_left =(self.top_left_cell.row,
                        self.top_left_cell.col)

        if self.bottom_right_cell.row < 0:
            self.bottom_right_cell.row = self.nr + self.bottom_right_cell.row
        if self.bottom_right_cell.col < 0:
            self.bottom_right_cell.col = self.nc + self.bottom_right_cell.col
        self.bottom_right = (self.bottom_right_cell.row,
                             self.bottom_right_cell.col)

    def check(self):
        """
        check the rule of area
        - end_position is lager than start_position
        - positon must be within max of dataframe
        """
        self.check_rc_order()
        self.check_rc_max(self.top_left_cell.val)
        self.check_rc_max(self.bottom_right_cell.val)

    def check_rc_order(self) -> None:
        """
        check end_position is larger than start_position 
        """
        if (self.top_left_cell.row > self.bottom_right_cell.row
            or self.top_left_cell.col > self.bottom_right_cell.col):
            raise ValueError("end cell must be " +
                             "larger than start row" +
                             f": {self.top_left_cell.val} - {self.bottom_right_cell.val}")

    def check_rc_max(self, position: tuple[int, int]) -> None:
        """
        check the position is within the max of row and column
        """
        r, c = position
        if r >= self.nr or c >= self.nc:
            raise ValueError(f"coordinate {position} must be within " +
                             f"max ({self.nr - 1}, {self.nc - 1})")
    
    def __str__(self):
        return str((self.top_left_cell.val, self.bottom_right_cell.val))

if __name__ == "__main__":

    df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]])
    print(df)

    c0 = Cell(0,3)
    print(f"{c0.val}")
    c0.row = 2
    print(f"{c0.val}")
    
    area = Area(df, (0, 0), (2,2))
    print(area)
    print(area.val)

    c1 = Cell(5, 1)

    c3 = c0 + c1
    print(c3)