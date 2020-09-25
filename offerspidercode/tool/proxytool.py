import json
import random


def read_proxy_data():
    proxy_result = json.load(open("./ipfile/proxypool.json","r",encoding="utf-8"))
    return proxy_result


def get_proxy():
    proxy_data = read_proxy_data()
    index = random.randint(0,len(proxy_data))
    return proxy_data[index]


if __name__ == '__main__':
    data = get_proxy()
    print("动态获取的IP地址为:",data)