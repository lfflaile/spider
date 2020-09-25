import urllib.request
import useragenttool
import lxml.html
import os
import json



def parse_proxy_url(temp_url):
    #Request对象
    request = urllib.request.Request(temp_url,headers=useragenttool.get_header())
    response = urllib.request.urlopen(request)
    result = response.read().decode("utf-8")
    return result


def catch_proxy_value_list(html_content):
    proxy_list = []
    #提取数据内容
    #(1)解析器对象 --用于解析html代码
    metree = lxml.html.etree
    proxy_parser = metree.HTML(html_content)
    #(2)获取所有tr
    tr_list = proxy_parser.xpath("//table[@id='ip_list']/tr")[1:]
    #(3)遍历tr单个元素
    for tr_element in tr_list:
        ip_item={}
        ip = tr_element.xpath("./td[2]/text()")[0]
        port = tr_element.xpath("./td[3]/text()")[0]
        agreement = tr_element.xpath("./td[6]/text()")[0]
        #拼接处理数据
        ip_item[agreement]=agreement.lower()+"://"+ip+":"+port
        proxy_list.append(ip_item)
    return proxy_list


def save_proxy_value(datas):
    ip_path="./ipfile"
    if not os.path.exists(ip_path):
        os.mkdir(ip_path)
    json.dump(datas,
              open(ip_path+"/proxydata.json","w",encoding="utf-8"),
              ensure_ascii=False,
              indent=2)
    print("所有IP数据已保存完毕")

def main():
    proxy_url='https://www.xicidaili.com/nn/'
    proxy_html_data = parse_proxy_url(proxy_url)
    #解析数据
    proxy_value_data=catch_proxy_value_list(proxy_html_data)
    save_proxy_value(proxy_value_data)

if __name__ == '__main__':
    main()
