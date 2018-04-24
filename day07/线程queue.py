import queue

#先进先出 -》队列
# q = queue.Queue(3)
#
# q.put('first')
# q.put('second')
# q.put('third')
#
# print(q.get())
# print(q.get())
# print(q.get())

# print(q.get(block=True,timeout=3))  #q.get_nowatit()

#先进后出 -》 堆栈

# q = queue.LifoQueue(3)
# q.put('first')
# q.put('second')
# q.put('third')
#
# print(q.get())
# print(q.get())
# print(q.get())

#优先级队列
q = queue.PriorityQueue(3)
q.put((10,'first'))
q.put((20,'second'))
q.put((5,'third'))

print(q.get())
print(q.get())
print(q.get())
