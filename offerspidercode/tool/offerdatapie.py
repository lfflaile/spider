from matplotlib import pyplot
import  pandas
def read_offer_data_excel():
    "从excel表格获取数据"
    data_result = pandas.read_excel("./lastoffer/招聘python岗位信息表.xls")
    salary = data_result["薪资"]
    return salary


def main():
    offer_salary = read_offer_data_excel()
    #5k以下,5k-8k,8k-14k,14k以上
    #print(offer_salary[0])
    count_5k=0
    count_8k=0
    count_14k=0
    count_boss=0
    #下标值
    index = 0
    while index<offer_salary.size:
        if offer_salary[index]<5000:
            count_5k+=1
        elif offer_salary[index]<8000:
            count_8k+=1
        elif offer_salary[index]<14000:
            count_14k+=1
        else:
            count_boss+=1
        index+=1
    #绘制分布图
    pyplot.rcParams["font.sans-serif"]=["SimHei"]
    data = [count_5k,count_8k,count_14k,count_boss]
    labels = ["5k以下","5k-8k","8k-14k","14k以上"]
    explore = [0,0,0,0.05]
    pyplot.pie(data,labels=labels,autopct="%2.2f%%",explode=explore)
    pyplot.title("python薪资占比分布图")
    pyplot.legend(loc="upper left")
    pyplot.show()

if __name__ == '__main__':
    main()
