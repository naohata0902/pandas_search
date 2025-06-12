import pandas as pd
from pandas_search.pandas_search import PandasSearch

def test_run():
    df = pd.read_excel("./major_results_2020.xlsx")
    ps = PandasSearch(df)

    print(ps.nr, ps.nc)

    ans = ps.is_match("abvccc", "^.bvc")
    print("regex match: ", ans)

    cells = ps.search("広島")
    """
    for cell in cells:
        print(f"position : {cell}, val:{df.iloc[*cell]}")
    """

    ans = ps.peek(cells, shift=(0, 0
                                 ))

if __name__ == "__main__":
    test_run()