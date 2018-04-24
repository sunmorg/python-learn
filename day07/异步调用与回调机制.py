from concurrent.futures import ThreadPoolExecutor
import time,random


def la(name):
    print('%s is laing' %name)
    time.sleep(random.randint(3,5))
    res = random.randint(7,13)*'#'
    return {'name':name,'res':res}
    # weight({'name': name, 'res': res})

def weight(shit):
    shit = shit.result()
    name = shit['name']
    size = len(shit['res'])
    print('%s la %s kg'%(name,size))

if __name__ == "__main__":
    pool = ThreadPoolExecutor(13)

    pool.submit(la, 'alex').add_done_callback(weight)
    pool.submit(la, 'wupq').add_done_callback(weight)
    pool.submit(la, 'dsgs').add_done_callback(weight)