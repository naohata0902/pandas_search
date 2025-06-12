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
    def v(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        this gives the area coordinates which is converted and checked
        """
        return (tuple(self.top_left), tuple(self.bottom_right))

    def conv(self):
        if self.top_left_cell.r < 0:
            self.top_left_cell.r = self.nr - 1
        if self.top_left_cell.c < 0:
            self.top_left_cell.c = self.nc - 1
        self.top_left =(self.top_left_cell.r,
                        self.top_left_cell.c)

        if self.bottom_right_cell.r < 0:
            self.bottom_right_cell.r = self.nr - 1
        if self.bottom_right_cell.c < 0:
            self.bottom_right_cell.c = self.nc - 1
        self.bottom_right = (self.bottom_right_cell.r,
                             self.bottom_right_cell.c)

    def check(self):
        """
        check the rule of area
        - end_position is lager than start_position
        - positon must be within max of dataframe
        """
        self.check_rc_order()
        self.check_rc_max(self.top_left_cell.v)
        self.check_rc_max(self.bottom_right_cell.v)

    def check_rc_order(self) -> None:
        """
        check end_position is larger than start_position 
        """
        if (self.top_left_cell.r > self.bottom_right_cell.r
            or self.top_left_cell.c > self.bottom_right_cell.c):
            raise ValueError("end cell must be " +
                             "larger than start row" +
                             f": {self.top_left_cell.v} - {self.bottom_right_cell.v}")

    def check_rc_max(self, position: tuple[int, int]) -> None:
        """
        check the position is within the max of row and column
        """
        r, c = position
        if r > self.nr or c > self.nc:
            raise ValueError(f"coordinate {position} must be within " +
                             f"max ({self.nr - 1}, {self.nc - 1})")
    
    def __str__(self):
        return str((tuple(self.top_left), tuple(self.bottom_right)))

if __name__ == "__main__":

    df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]])
    print(df)

    c0 = Cell(0,3)
    print(f"{c0.v}")
    c0.r = 2
    print(f"{c0.v}")
    
    area = Area(df, (0, 0), (3,3))
    print(area)
    print(area.v)

    c1 = Cell(5, 1)

    c3 = c0 + c1
    print(c3)