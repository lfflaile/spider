import pandas
from matplotlib import pyplot
import numpy
def read_offer_data_excel():
    "从excel表格获取数据"
    data_result = pandas.read_excel("./lastoffer/招聘python岗位信息表.xls")
    salary = data_result["薪资"]
    return salary
def main():
    offer_salary=read_offer_data_excel()
    #绘制薪资分布图
    pyplot.figure(figsize=(18,8),dpi=80)
    #处理中文乱码
    pyplot.rcParams["font.sans-serif"]=["SimHei"]
    #x轴
    x=[i for i in range(1,offer_salary.size+1)]
    #绘制
    pyplot.scatter(x,offer_salary,label="薪资")
    #添加标题
    pyplot.title("某招聘网python薪资")
    pyplot.xlabel("岗位个数")
    pyplot.ylabel("薪资(单位:元)")
    #x刻度 每间隔10个则绘制刻度值
    x_tick = [i for i in range(0,offer_salary.size+1,10)]
    pyplot.xticks(x_tick,x_tick,rotation=45)
    #最大最小值
    pyplot.xlim(0,501)
    #y刻度
    y_tick = [i for i in range(0,41000,2500)]
    pyplot.yticks(y_tick)
    pyplot.ylim(0,41000)
    #网格
    pyplot.grid(alpha=0.1)
    #绘制均值线
    average = numpy.mean(offer_salary)
    #处理
    avg_list = [average for i in x]
    #print(avg_list)
    pyplot.plot(x,avg_list,"r",linewidth=2,label="平均薪资")
    #绘制均值
    pyplot.text(0,average+300,"均薪"+str(average),color="green")
    #绘制图例
    pyplot.legend(loc=0)
    #显示
    pyplot.show()

if __name__ == '__main__':
    main()

