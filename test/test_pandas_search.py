import pytest
import pandas as pd
from pandas_search import PandasSearch

# Normal Case
df = pd.DataFrame([["taro", 23, "male"],
                   ["rin", 18, "male"],
                   ["hana", 33, "female"]] )
ps = PandasSearch(df)

def test_df_shape():
    assert (ps.nr, ps.nc) == (3, 3)

def test_df_info_0():
    assert ps.df.iloc[0, 0] == "taro"

def test_df_info_1():
    assert ps.df.iloc[1, 1] == 18

def test_df_info_2():
    assert ps.df.iloc[2, 2] == "female"

def test_search():
    s = ps.search("rin")
    assert list(s) == [(1, 0)]

def test_peek():
    s = ps.search("rin")
    assert ps.peek(s)[0].iloc[0, 0] == "rin"

def test_peek_size_1():
    s = ps.search("rin")
    assert ps.peek(s, target_size=(1, 3))[0].values.tolist() == [["rin", 18, "male"]]

def test_peek_size_2():
    s = ps.search("rin")
    assert ps.peek(s, target_size=(2, 1))[0].values.tolist() == [["rin"], ["hana"]]

def test_peek_size_3():
    s = ps.search("rin")
    assert ps.peek(s, target_size=(1, -1))[0].values.tolist() == [["rin", 18, "male"],]

def test_peek_size_4():
    s = ps.search("rin")
    assert ps.peek(s, target_size=(1, -2))[0].values.tolist() == [["rin", 18]]

def test_peek_shift():
    s = ps.search("rin")
    assert ps.peek(s, shift=(1, 0))[0].values.tolist() == [["hana"]]
# Abnormal Case
