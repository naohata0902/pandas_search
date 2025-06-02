import pandas as pd
import re

class PandasSearch():
    """
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.nr, self.nc = df.shape

    def can_match(self, value: str, expression: str) -> bool:
        """
        this returns boolean whether the value is matched by the regex expression
        parameter:
            value(str): searched word
            expression(str): regular expression to search
        retrun:
            boolean
        """
        m = re.search(expression, value)
        if m is None:
            return False
        else:
            return True
        
    def find(self, word: str, search_area: tuple[tuple, tuple]) -> list:
        pass

    



    