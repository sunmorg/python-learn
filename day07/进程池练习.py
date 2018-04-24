from concurrent.futures import ThreadPoolExecutor
import requests
import time

def get(url):
    response = requests.get(url)
    time.sleep(3)
    return {'url':url,'content':response.text}

def pase(res):
    res = res.result()
    print('%s parse res is %s'%(res['url'],len(res['content'])))


if __name__ == "__main__":
    urls = [
        'http://www.cnblogs.com/linhaifeng',
        'http://www.cnblogs.com',
        'http://www.python.org',
    ]

    pool = ThreadPoolExecutor(2)

    for url in urls:
        pool.submit(get,url).add_done_callback(pase)