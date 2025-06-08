import pandas as pd

class Area:
    """
    Area class shows rectangle area which is defined 
    by top_left cell and bottom_right cell
    """
    def __init__(self,
                df: pd.DataFrame,
                area: tuple[tuple[int, int], tuple[int, int]]):
        self.df = df
        self.nr, self.nc = df.shape
        self.start_position, self.end_position = area
        self.sp_r, self.sp_c = self.start_position
        self.ep_r, self.ep_c = self.end_position
        self.conv()
        self.check()

    def get(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        this gives the area coordinates which is converted and checked
        """
        return ((self.sp_r, self.sp_c), (self.ep_r, self.ep_c))

    def conv(self):
        if self.sp_r < 0:
            self.sp_r = self.nr - 1
        if self.sp_c < 0:
            self.sp_c = self.nc - 1
        self.start_position = (self.sp_r, self.sp_c)
        if self.ep_r < 0:
            self.ep_r = self.nr - 1
        if self.ep_c < 0:
            self.ep_c = self.nc - 1
        self.end_position = (self.ep_r, self.ep_c)

    def check(self):
        """
        check the rule of area
        - end_position is lager than start_position
        - positon must be within max of dataframe
        """
        self.check_rc_order()
        self.check_rc_max(self.start_position)
        self.check_rc_max(self.end_position)

    def check_rc_order(self) -> None:
        """
        check end_position is larger than start_position 
        """
        if self.sp_r > self.ep_r or self.sp_c > self.ep_c:
            raise ValueError("end cell must be " +
                             "larger than start row" +
                             f": {self.start_position} - {self.end_position}")

    def check_rc_max(self, position: tuple[int, int]) -> None:
        """
        check the position is within the max of row and column
        """
        r, c = position
        if r > self.nr or c > self.nc:
            raise ValueError(f"coordinate {position} must be within " +
                             f"max ({self.nr - 1}, {self.nc - 1})")
        
