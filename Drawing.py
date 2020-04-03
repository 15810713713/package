import re
import datetime
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
import matplotlib


def Split_file(filename_data_path,path):
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
    else:
        pass
    '''分割文件'''
    total = sum(1 for line in open(filename_data_path))
    if 100000 <= total <= 1000000 :
        split_number = total//10
    elif total>10000000:
        split_number = total//100
    else:
        split_number = total

    rows = pd.read_csv(filename_data_path, chunksize=split_number)
    for i, chuck in enumerate(rows):
        chuck.to_csv(path +'\out{}.csv'.format(i))

def get_data(data,new_data):
    '''对每个文件数据进行转化,同时价格为零时候跳过该行'''
    # 通过with语句读取，以列表类型读取
    with open(data, 'r', encoding='utf8')as fp:
        # 使用列表推导式，将读取到的数据装进列表
        data_list = [i for i in csv.reader(fp)]  # csv.reader 读取到的数据是list类型
        f = open(new_data, 'w', encoding='utf-8')
        # 构建列表头
        csv_writer = csv.writer(f)
        csv_writer.writerow(["时间", "金额", "交易量"])
        for data in data_list:
            # 对每行数据进行处理
            data[1] = datetime.datetime.fromtimestamp(int(data[1]))
            # 写入CSV文件(如果价格为零跳过该行)
            if data[2] == '0':
                continue
            else:
                csv_writer.writerow(["" + str(data[1]) + "", '' + data[2] + '', '' + data[3] + ''])
        # 关闭文件
        f.close()

def File_directory(filename_path,new_filename_path):
    '''文件夹内文件名修改'''
    isExists = os.path.exists(new_filename_path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(new_filename_path)
    else:
        pass
    filename_data = filename_path
    data = [i[2:][0] for i in os.walk(filename_data)]
    for i, data in enumerate(data[0]):
        get_data(data=filename_data + '\\' + data, new_data=new_filename_path + '\\new_data{}.csv'.format(i))

def get_Duplicate_removal(new_data):
    '''重复去重'''
    frame = pd.read_csv(new_data, engine='python')
    data = frame.drop_duplicates(subset=None, keep='first', inplace=False)
    data.to_csv(new_data, encoding='utf8')

def get_Month_Transaction(data,max_year):
    '''通过获取最大交易月份'''
    filename_data = data
    # filename_data_test = 'D:\split_csv\\20200401_csv'
    month = [0,0,0,0,0,0,0,0,0,0,0,0]  #记录月份交易次数
    data = [i[2:][0] for i in os.walk(filename_data)]
    for data in data[0]:
        with open(filename_data + '\\' + data, encoding="utf8") as f:
            data = f.read()
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', data)
            year = [date for date in dates]
            for i in year:
                if i[0:4] == max_year:
                    if '01-' in i[5:9]:
                        month[0] += 1
                    elif '02-' in i[5:9]:
                        month[1] += 1
                    elif '03-' in i[5:9]:
                        month[2] += 1
                    elif '04-' in i[5:9]:
                        month[3] += 1
                    elif '05-' in i[5:9]:
                        month[4] += 1
                    elif '06-' in i[5:9]:
                        month[5] += 1
                    elif '07-' in i[5:9]:
                        month[6] += 1
                    elif '08-' in i[5:9]:
                        month[7] += 1
                    elif '09-' in i[5:9]:
                        month[8] += 1
                    elif '10-' in i[5:9]:
                        month[9] += 1
                    elif '11-' in i[5:9]:
                        month[10] += 1
                    elif '12-' in i[5:9]:
                        month[11] += 1
                else:
                    continue
        f.close()

    return month

def get_Maximum_price(filename_data):
    '''交易量最大年份的价格曲线图'''
    year_2013 = 0
    year_2014 = 0
    year_2015 = 0
    year_2016 = 0
    year_2017 = 0
    year_2018 = 0
    filename_data = filename_data
    data = [i[2:][0] for i in os.walk(filename_data)]
    for data in data[0]:
        with open(filename_data + '\\' + data, encoding="UTF-8") as f:
            data = f.read()
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', data)
            year = [date[0:4] for date in dates]
            for i in year:
                if i == '2013':
                    year_2013 += 1
                elif i == '2014':
                    year_2014 += 1
                elif i == '2015':
                    year_2015 += 1
                elif i == '2016':
                    year_2016 += 1
                elif i == '2017':
                    year_2017 += 1
                elif i == '2018':
                    year_2018 += 1
                else:
                    pass

    year_list_x = [year_2013, year_2014, year_2015, year_2016, year_2017, year_2018]
    b = year_list_x.index(max(year_list_x))  # 最大值的位置
    year = {
        0 :'2013',
        1: '2014',
        2: '2015',
        3: '2016',
        4: '2017',
    }

    #年交易量最大年份
    max_year = year[b]
    return max_year

def graphic_display(max_year,y):
    # 将全局的字体设置为黑体
    matplotlib.rcParams['font.family'] = 'SimHei'

    x = ("1月", "2月", "3月", "4月", "5月", '6月', '7月', '8月', '9月', '10月', '11月', '12月')
    p1 = plt.plot(x,y,color='red',linewidth=1.0,linestyle='-')
    for a, b in zip(x, y):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)

    plt.title(""+ max_year +"年12个月交易量")

    plt.legend()

    # 展示图形
    plt.show()

def main(filename_data_path,split_filename_data_path,split_new_filename_data_path):
    '''start'''
    filename_data_path = filename_data_path
    path = split_filename_data_path
    new_filename_path = split_new_filename_data_path
    Split_file(filename_data_path,path)             #分割
    File_directory(filename_path = path,new_filename_path = new_filename_path)   #原始目录 生成新的文件目录 进行数据清洗
    max_year = get_Maximum_price(filename_data=new_filename_path)                #jmax 年份
    month = get_Month_Transaction(data=new_filename_path, max_year=max_year)     # 返回12个月份的列表
    graphic_display(max_year,y=month)   # 绘图生成结果


if __name__ == '__main__':
    filename_data_path = 'E:\\program_pycharm_python\\AI_Data_analysis\\btctradeCNY_test.csv'    #需要处理的文件
    split_filename_data_path = 'D:\\AI_Data_analysis\\btc'                                       #分割后出输出的目录       (生成的垃圾文件可以根据需求手动删除)
    split_new_filename_data_path = 'D:\\AI_Data_analysis\\btc_csv'                               #分割后文件数据清洗后 放入新的文件夹
    #绘图
    main(filename_data_path=filename_data_path,split_filename_data_path=split_filename_data_path,split_new_filename_data_path=split_new_filename_data_path)
