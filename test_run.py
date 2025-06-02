import pandas as pd 
from pandas_search.pandas_search import PandasSearch

def test_run():
    df = pd.read_excel("./major_results_2020.xlsx")
    ps = PandasSearch(df)

    print(ps.nr, ps.nc)

    ans = ps.can_match("abvccc", "^.bvc")
    print("regex match: ", ans)


if __name__ == "__main__":
    test_run()