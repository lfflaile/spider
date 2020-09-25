import requests
import useragenttool
import proxytool
import lxml.html
import os
import json

class OfferIndexSpider(object):

    def __init__(self):
        #初始化
        self.offer_http = "https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&add"
    def parse_offer_url(self):
        offer_response = requests.get(self.offer_http,headers=useragenttool.get_header(),proxies=proxytool.get_proxy())
        #获取结果
        result = offer_response.content.decode("gbk")
        return result

    def save_offer_file(self,datas):
        offer_path = "./offerfile"
        if not os.path.exists(offer_path):
            os.mkdir(offer_path)
        json.dump(datas,open(offer_path+"/offer.json","w",encoding="utf-8"),
                ensure_ascii=False,
                indent=2)

    def catch_offer_info_list(self,html_content):
        #提取岗位
        metree = lxml.html.etree
        #处理
        offer_parser = metree.HTML(html_content)
        div_list = offer_parser.xpath("//div[@id='resultList']/div[@class='el']")
        offer_list=[]
        for div_element in div_list:
            #工作岗位
            offer_item={}
            #提取职位名,职位链接,公司名,公司链接,工作地点,薪资,发布时间
            #职位名
            position = div_element.xpath("./p/span/a/text()")[0]
           # print("职位名:",position.strip())
            offer_item["position"] = position.strip()
            #职位链接
            position_url = div_element.xpath("./p//a/@href")[0]
            #print(position_url)
            offer_item["position_url"] = position_url
            #公司名
            company = div_element.xpath("./span[@class='t2']/a/@title")[0]
            #print(company)
            offer_item["company"]=company
            #公司链接
            company_url = div_element.xpath("./span[@class='t2']/a/@href")[0]
            #print(company_url)
            offer_item[company_url] = company_url
            #工作地点
            work_loc = div_element.xpath("./span[@class='t3']/text()")[0]
            #print(work_loc)
            offer_item["work_loc"] = work_loc
            #薪资
            salary_value = div_element.xpath("./span[@class='t4']/text()")
            salary = salary_value[0]  if len(salary_value)>0 else "4-6千/月"
            #print(salary)
            offer_item["salary"] = salary
            #发布时间
            public_time = div_element.xpath("./span[@class='t5']/text()")[0]
            offer_item["public_time"] = public_time
            offer_list.append(offer_item)
        return offer_list

    def run(self):
        #发送请求
        offer_datas=self.parse_offer_url()
        offer_info_datas = self.catch_offer_info_list(offer_datas)
        #保存文件
        self.save_offer_file(offer_info_datas)




def main():
    spider=OfferIndexSpider()
    spider.run()

if __name__ == '__main__':
    main()