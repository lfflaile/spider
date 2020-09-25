import json
import requests
import useragenttool

def read_proxy_file_by_json():
    proxy_file = open("./ipfile/proxydata.json","r",encoding="utf-8")
    proxy_result = json.load(proxy_file)
    return proxy_result

def main():
    sohu_url = "https://www.sohu.com/"
    value_proxy_list=[]
    proxy_ip_data = read_proxy_file_by_json()
    #遍历IP
    for proxy in proxy_ip_data:
        try:
            proxy_result = requests.get(sohu_url,useragenttool.get_header(),proxies=proxy)
            if proxy_result.status_code == 200:
                value_proxy_list.append(proxy)
                json.dump(value_proxy_list,
                          open("./ipfile/proxypool.json","w",encoding="utf-8"),
                          ensure_ascii=False,
                          indent=2)
        except Exception:
            print("该代理通讯异常,IP代理值为",proxy)


if __name__ == '__main__':
    main()