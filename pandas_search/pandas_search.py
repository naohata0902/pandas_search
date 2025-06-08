import pandas as pd
import re
from typing import Generator

from .area import Area

class PandasSearch():
    """
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
        
    def find(self, regex: str, search_area: tuple[tuple, tuple]
             ) -> Generator[tuple[int, int], None, None]:
        """
        """
        ((sp_r, sp_c), (ep_r, ep_c)) = search_area
        npdf = self.df.astype(str).to_numpy()

        fixed_search_area = Area(self.df, search_area).get()

        for ir in range(sp_r, ep_r + 1):
            for ic in range(sp_c, ep_c + 1):
                cell_val = npdf[ir, ic]
                if not isinstance(cell_val, str):
                    continue
                if self.is_match(cell_val, regex):
                    print(ir, ic)
                    yield (ir, ic)


    
    