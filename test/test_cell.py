import pytest
from lib import Cell

# Normal Case
cell = Cell(2, 3)
def test_property_val():
    assert cell.val == (2, 3)

def test_property_row():
    assert cell.row == 2

def test_property_col():
    assert cell.col == 3

def test_str():
    assert str(cell) == "(2, 3)"

def test_setter_val():
    cell = Cell(2, 3)
    cell.val = (9, 9)
    assert cell.val == (9, 9)    

def test_setter_row():
    cell = Cell(2, 3)
    cell.row = 100
    assert cell.val == (100, 3) 

def test_setter_col():
    cell = Cell(2, 3)
    cell.col = 101
    assert cell.val == (2, 101)

c0 = Cell(100, 100)
c1 = Cell(50, 100)
c2 = Cell(-30, -40)
t0 = (20, 30)

def test_add01():
    c = c0 + c1
    assert c.val == (150, 200)

def test_add02():
    c = c0 + c2
    assert c.val == (70, 60)

def test_add03():
    c = c0 + c1 + c2
    assert c.val == (120, 160)

def test_add04():
    c = c0 + t0
    assert c.val == (120, 130)

def test_add05():
    c = c0 + t0 + c1
    assert c.val == (170, 230)

# Abnormal Case
def test_decimal():
    with pytest.raises(ValueError):
        Cell(1.2, 4)

def test_str():
    with pytest.raises(ValueError):
        Cell(2, "4")
