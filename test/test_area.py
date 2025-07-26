from ..lib import Area
import pandas as pd
import pytest

df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]])    
def test_area_val():
    area = Area(df, (0, 0), (1,2))
    assert area.val == ((0, 0), (1, 2))

def test_area_val2():
    area = Area(df, (-2, -2), (-1, -2))
    assert area.val == ((1, 1), (2, 1))
    
def test_str_area():
    area = Area(df, (0, 0), (1, 2))
    assert str(area) == "((0, 0), (1, 2))"

def test_area_boundary():
    area = Area(df, (0, 0), (-1, -1))
    assert area.val == ((0, 0), (2, 2))

def test_area_boundary2():
    with pytest.raises(ValueError):
        Area(df, (1,1), (3, 3))

def test_area_boundary3():
    with pytest.raises(ValueError):
        Area(df, (2,2), (1,2))

def test_area_boundary4():
    with pytest.raises(ValueError):
        Area(df, (2,2), (-2,2))
