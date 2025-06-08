import pandas as pd

class Area:
    """
    Area class shows rectangle area which is defined 
    by top_left cell and bottom_right cell
    """
    def __int__(self,
                df: pd.DataFrame,
                area: tuple[tuple[int, int], tuple[int, int]]):
        self.df = df
        self.nr, self.nc = df.shape
        self.start_position, self.end_position = area
        self.sp_r, self.sp.c = self.start_position
        self.ep_r, self.ep.c = self.end_position

    def conv_end(self) -> tuple[tuple, tuple]:
        if self.ep_r < 0:
            self.ep_r = self.nr - 1
        if self.ep_c < 0:
            self.ep_c = self.nc - 1
        
        return ((self.sp_r, self.sp_c), (self.ep_r, self.ep_c)) 
