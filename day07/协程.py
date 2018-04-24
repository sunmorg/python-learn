def producer():
    g = consumer()
    next(g)
    for i in range(10000):
        g.send(i)

def consumer():
    while True:
        res = yield

producer()