import pandas as pd
from pandas_search.pandas_search import PandasSearch

def test_run():
    df = pd.read_excel("./major_results_2020.xlsx")
    ps = PandasSearch(df)

    print(ps.nr, ps.nc)

    ans = ps.is_match("abvccc", "^.bvc")
    print("regex match: ", ans)

    cells = ps.search("都道府県名", exact_match = True)
    """
    for cell in cells:
        print(f"position : {cell}, val:{df.iloc[*cell]}")
    """
    print("test")

    dfs = ps.peek(cells, shift=(0, 0), target_size=(1, -1))
    for idf in dfs:
        print(idf)
 

if __name__ == "__main__":
    test_run()