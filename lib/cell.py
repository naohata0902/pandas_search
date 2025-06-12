class Cell:
    def __init__(self, r: int, c: int):
        self.__row= r
        self.__col = c

    @property
    def r(self):
        return self.__row
    
    @property
    def c(self):
        return self.__col

    @property
    def v(self):
        return (self.__row, self.__col)
    
    @r.setter
    def r(self, val: int):
        self.__row = val

    @c.setter
    def c(self, val: int):
        self.__col = val

    @v.setter
    def v(self, val: tuple):
        self.__row, self.__col = val

    def __add__(self, other: "Cell") -> "Cell":
        return Cell(self.r + other.r, self.c + other.c)
    
    def __str__(self):
        return str(self.v)


if __name__ == "__main__":

    c0 = Cell(0,3)
    print(c0)
    c0.r = 2
    print(c0)

    c1 = Cell(5, 1)
    print(c1+ c0)
