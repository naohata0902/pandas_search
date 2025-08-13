from logging import getLogger

logger = getLogger()

class Cell:
    def __init__(self, row: int, col: int):
        logger.info("create Cell instance")
        logger.debug(f"{row=}:{col=}")
        if not isinstance(row, int) or not isinstance(col, int):
            raise ValueError("row of column number must be integer !!")
        self.__row = row
        self.__col = col
        logger.debug(f"{self.__row=}:{self.__col=}")

    @property
    def row(self):
        return self.__row
    
    @property
    def col(self):
        return self.__col

    @property
    def val(self):
        return (self.__row, self.__col)
    
    @row.setter
    def row(self, val: int):
        if not isinstance(val, int):
            raise ValueError("row number must be integer !!")
        self.__row = val

    @col.setter
    def col(self, val: int):
        if not isinstance(val, int):
            raise ValueError("column number must be integer !!")
        self.__col = val

    @val.setter
    def val(self, val: tuple):
        if not isinstance(val, tuple):
            raise ValueError("cell must be tuple !!")
        elif len(val) != 2:
            raise ValueError("size of tuple must be two")
        elif not isinstance(val[0], int):
            raise ValueError("element of cell is int !!")
        elif not isinstance(val[1], int):
            raise ValueError("element of cell is int !!")
        self.__row, self.__col = val

    def __add__(self, other: "Cell|tuple[int, int]") -> "Cell":
        if isinstance(other, tuple):
            return Cell(self.row + other[0], self.col + other[1])
        else:
            return Cell(self.row + other.row, self.col + other.col)
    
    def __str__(self):
        return str(self.val)

if __name__ == "__main__":
    """
    simple performance test
    """
    c0 = Cell(0,3)
    print("c0 =", c0)
    c0.r = 2
    print("c0 = ", c0)

    c1 = Cell(5, 1)
    t1 = (2, 4)
    print("c0 = ", c0, " : c1 = ", c1, " : t1 = ", t1)
    print("c1 + c0 = ", c1 + c0)
    print("c1 + t1 = ", c1 + t1)
    print("c1 + t1 + c0 = ", c1 + t1 + c0)
    c = Cell(100, 200)
    c.val = (1.2, 3)
    print(c)