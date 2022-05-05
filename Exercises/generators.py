
def gen():
    yield 1

def fib(limit):
    a, b = 0, 1
    while a < limit:
        yield a     # generator: saves the number, so we can write after "yield", but we cannot write after return
        a, b = b, a+b

def generators():
    g1 = gen()
    g2 = fib(10000000000000000)
    print(list(g2))


######################################
# SCOPING

x = 3
def fun3():
    print(x)
    x = 1

fun3()

def fun():
    print(x)

    def fun2():
        print(x)
        x = 2
        print(x)

    fun2()
    print(x)

fun()