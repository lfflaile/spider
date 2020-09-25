import requests
import useragenttool
import proxytool
import lxml.html
import re
import random
import time
import xlwt
import os
class OfferSpider(object):
    def __init__(self):
       self.offer_index_url ="https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&add"
       self.offer_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&add"
       self.offer_list = []
    def get_offer_pages(self):
        "动态获取页面数"
        offer_page_response = requests.get(self.offer_index_url,
                     headers=useragenttool.get_header(),
                     proxies=proxytool.get_proxy())
        #获取网页源码
        page_html_content = offer_page_response.content.decode("gbk")
        #解析数据
        metree = lxml.html.etree
        page_parser = metree.HTML(page_html_content)
        #获得内容值
        pages_content = page_parser.xpath("//div[@class='dw_page']//span[@class='td']/text()")[0]
        #获得682的值
        pages = int(re.search(r"共(\d+)页",pages_content)[1])
        return pages

    def get_offer_url_list(self,num):
        #拼接所有页面的url
        url_list=[]
        for page_index in range(1,num+1):
            temp_url = self.offer_url.format(page_index)
            #添加到列表
            url_list.append(temp_url)
        return url_list
    def parse_offer_url(self,temp_url):
        offer_response = requests.get(temp_url,headers=useragenttool.get_header(),proxies=proxytool.get_proxy())
        offer_html_content=offer_response.content.decode("gbk")
        return offer_html_content

    def catch_work_info(self, temp_url):
        "提取工作职责"
        try:
            work_response = requests.get(temp_url,headers=useragenttool.get_header(),proxies=proxytool.get_proxy())
            work_html_content = work_response.content.decode("gbk")
            #提取数据
            work_parser = lxml.html.etree.HTML(work_html_content)
            work_infos = "".join(work_parser.xpath("//div[@class='bmsg job_msg inbox']//text()")).strip().replace(" ","")
        except Exception:
            work_infos = "暂无数据"
        return work_infos

    def catch_company_info(self, temp_url):
        "提取公司信息"
        try:
            company_response = requests.get(temp_url, headers=useragenttool.get_header(), proxies=proxytool.get_proxy())
            company_html_content = company_response.content.decode("gbk")
            # 提取数据
            company_parser = lxml.html.etree.HTML(company_html_content)
            company_infos = "".join(company_parser.xpath("//div[@class='con_txt']//text()")).strip().replace(" ","")
        except Exception:
            company_infos = "暂无数据"
        return company_infos

    def save_offer_file(self):
        "保存所有数据内容到excel"
        offer_path = "./lastoffer"
        if not os.path.exists(offer_path):
            os.mkdir(offer_path)
        #获得book工作簿
        book = xlwt.Workbook(encoding="utf-8")
        #创建一个表格标题
        offer_sheet=book.add_sheet("python招聘信息")
        #写入数据
        row_index=0
        while row_index<len(self.offer_list):
            col_index=0
            while col_index<len(self.offer_list[row_index]):
                offer_sheet.write(row_index,col_index,self.offer_list[row_index][col_index])
                col_index+=1
            row_index+=1
        book.save(offer_path+"/招聘python岗位信息表.xls")
        #保存结果
        print("所有数据已保存成功")

    def catch_offers_list(self, html_content):
        # 提取岗位
        metree = lxml.html.etree
        # 处理
        offer_parser = metree.HTML(html_content)
        div_list = offer_parser.xpath("//div[@id='resultList']/div[@class='el']")
        for div_element in div_list:
            # 工作岗位
            offer_item =[]
            # 提取职位名,职位链接,公司名,公司链接,工作地点,薪资,发布时间
            # 职位名
            position = div_element.xpath("./p/span/a/text()")[0]
            # print("职位名:",position.strip())
            offer_item.append(position.strip())
            # 职位链接
            position_url = div_element.xpath("./p//a/@href")[0]
            # print(position_url)
            offer_item.append(position_url)
            # 公司名
            company = div_element.xpath("./span[@class='t2']/a/@title")[0]
            # print(company)
            offer_item.append(company)
            # 公司链接
            company_url = div_element.xpath("./span[@class='t2']/a/@href")[0]
            # print(company_url)
            offer_item.append(company_url)
            # 工作地点
            work_loc = div_element.xpath("./span[@class='t3']/text()")[0]
            # print(work_loc)
            offer_item.append(work_loc)
            # 薪资
            salary_value = div_element.xpath("./span[@class='t4']/text()")
            salary = salary_value[0] if len(salary_value) > 0 else "4-6千/月"
            #处理薪资
            #千/月,提取-前数值 .*1000
            salary_result = 8000
            if "千/月" in salary:
                salary_result = int(float(salary.split("-")[0])*1000)
            elif "万/月" in salary:
                salary_result = int(float(salary.split("-")[0])*10000)
            elif "万/年" in salary:
                salary_result = int(float(salary.split("-")[0])/12 * 10000)
            # print(salary)
            offer_item.append(salary_result)
            # 发布时间
            public_time = div_element.xpath("./span[@class='t5']/text()")[0]
            offer_item.append(public_time)
            #工作内容
            work_information = self.catch_work_info(position_url)
            offer_item.append(work_information)
            #公司简介
            company_information=self.catch_company_info(company_url)
            offer_item.append(company_information)
            self.offer_list.append(offer_item)

    def run(self):
        #添加表头
        excel_titles=["职位名","职位链接","公司名","公司链接","工作地点","薪资","发布时间","工作职责","公司简介"]
        self.offer_list.append(excel_titles)
        #page_sum = self.get_offer_pages()
        page_sum=10
        #拼接url
        offer_url_datas=self.get_offer_url_list(page_sum)

        index = 1
        #遍历所有url列表
        for http_url in offer_url_datas:
            print("------->正在爬取第%d页的数据内容,请稍后!!"%index)
            offer_html_data = self.parse_offer_url(http_url)
            #print("输出内容",offer_html_data)
            #提取数据
            self.catch_offers_list(offer_html_data)
            wait_time=random.randint(0,10)
            print("所有岗位信息", self.offer_list)
            print("动态限制访问频率,%ds秒后继续爬去数据...."% wait_time)
            time.sleep(wait_time)
            index+=1
        self.save_offer_file()



def main():
    spider = OfferSpider()
    spider.run()


if __name__ == '__main__':
    main()