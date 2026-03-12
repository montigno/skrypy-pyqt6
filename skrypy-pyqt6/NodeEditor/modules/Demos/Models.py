class AllTypes():

    def __init__(self,
                 inInt=0, inFloat=0.0, inString='', inBool=True,
                 inPath='path', listInt=[0], listFloat=[0.0],
                 listString=[''], listBool=[False], listPath=['path'],
                 arrayInt=[[0]], arrayFloat=[[0.0]], arrayString=[['']],
                 arrayBool=[[False]], arrayPath=[['path']],
                 inDict={}, inTuple=('',), inTuple2=(32,)):

        self.inInt = inInt
        self.inFloat = inFloat
        self.inString = inString
        self.inBool = inBool
        self.inPath = inPath

        self.listInt = listInt
        self.listFloat = listFloat
        self.listString = listString
        self.listBool = listBool
        self.listPath = listPath

        self.arrayInt = arrayInt
        self.arrayFloat = arrayFloat
        self.arrayString = arrayString
        self.arrayBool = arrayBool
        self.arrayPath = arrayPath

        self.dict = inDict
        self.tup = inTuple
        self.tup2 = inTuple2

    def outInt(self) -> int:
        return self.inInt

    def outFloat(self) -> float:
        return self.inFloat

    def outString(self) -> str:
        return self.inString

    def outBool(self) -> bool:
        return self.inBool

    def outPath(self) -> None:
        return self.inPath

    def listInt(self) -> list[int]:
        return self.listInt

    def listFloat(self) -> list[float]:
        return self.listFloat

    def listString(self) -> list[str]:
        return self.listString

    def listBool(self) -> list[bool]:
        return self.listBool

    def listPath(self) -> list[None]:
        return self.listPath

    def arrayInt(self) -> list[list[int]]:
        return self.arrayInt

    def arrayFloat(self) -> list[list[float]]:
        return self.arrayFloat

    def arrayString(self) -> list[list[str]]:
        return self.arrayString

    def arrayBool(self) -> list[list[bool]]:
        return self.arrayBool

    def arrayPath(self) -> list[list[None]]:
        return self.arrayPath

    def dictionary(self) -> dict:
        return self.dict

    def tuple(self) -> tuple:
        return self.tup

    def tuple2(self) -> tuple:
        return self.tup2

#############################################################################


class only_options:
    def __init__(self, **options):
        print(options)

#############################################################################


class Fibonacci:

    def __init__(self, n=0):
        a = 0
        b = 1
        if n < 0:
            print("Incorrect input")
            self.res = 0
        elif n == 0:
            self.res = a
            self.res1 = a
        elif n == 1:
            self.res = b
            self.res1 = b
        else:
            for i in range(2, n):
                c = a + b
                a = b
                b = c
            self.res = b
            self.res1 = a

    def n_out(self) -> float:
        return self.res

    def n_1_out(self) -> float:
        return self.res1

#############################################################################


class comboBox_example:
    def __init__(self, input1="enumerate(('Item1', 'Item2', 'Item3'))", input2="enumerate(('Gauss', 'Laplace', 'Sobel'))", **options):
        self.resp1 = input1
        self.resp2 = input2
        self.resp3 = None
        if options:
            self.resp3 = options['input3']

    def out1(self) -> str:
        return self.resp1

    def out2(self) -> str:
        return self.resp2

    def out3(self) -> str:
        return self.resp3
