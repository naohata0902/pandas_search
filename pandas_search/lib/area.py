import pandas as pd
# from .cell import Cell

class Area:
    """
    Area class shows rectangle area which is defined 
    by top_left cell and bottom_right cell
    """

    def __init__(self,
                 rows: tuple[int, int, int] = (None, None, None),
                 cols: tuple[int, int, int] = (None, None, None),
                 ): 
        self.rows = rows
        self.cols = cols

    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        """
        slice_rows = slice(*self.rows)
        slice_cols = slice(*self.cols)
        return df.iloc[slice_rows, slice_cols]

    def __str__(self):
        return str((self.rows, self.cols))

if __name__ == "__main__":

    df = pd.DataFrame([[1,2,3,4],[4,5,6,3],[7,8,9,22]])
    print(df)
    
    area = Area((0, None),(None, None, -1))
    print(area)

    df_ = area.extract(df)

    print(df_)