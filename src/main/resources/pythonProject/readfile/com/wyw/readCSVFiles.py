from typing import Any , Union
from copy import copy
import win32com
from win32com.client import Dispatch,constants
import pandas as pd


def open_excel(path , open_password , write_password):
    # 载入Excel
    xlApp = win32com.client.Dispatch("Excel.Application")
    xlApp.Visible = True
    xlApp.DisplayAlerts = False

    # 打开Excel
    xlwb = xlApp.Workbooks.Open(Filename=path, UpdateLinks=0,
                                ReadOnly=False, Format=None, Password=open_password, WriteResPassword=write_password)
    # 获取某个Sheet页数据（页数从1开始）
    sheet_data = xlwb.Worksheets(1)
    excelFile = r'E:\自动化脚本（python）\data.csv'
    df = pd.DataFrame(pd.read_csv(excelFile, header=None))

    for i in range(df.shape[0]):
        update_excel(sheet_data, df, i)
        write_excel(xlwb, i + 1)

    # 保存excel
    xlwb.Save()
    # 关闭Excel
    xlwb.Close()
    xlApp.Quit()


# 写入excel
def write_excel(xlwb, i):
    # sheet_data.Name = 'sheet0'
    ws = xlwb.Worksheets.Add()
    print(i)
    ws.Name = 'sheet{d1}'.format(d1=i+1)
    print(ws.Name)
    xlwb.Worksheets("sheet0").Range("A1:AI100").Copy(ws.Range("A1:AI100"))


# 每张表的update
def update_excel(sheet_data, df, i):

    print(df.shape[0])
    for j in sheet_data.UsedRange.Value:
        print(j, '\t')

        # 项目名称
        sheet_data.Cells(2, 2).Value = "{d1}KV{d2}式{d3}接地箱".format(d1=df[0][i], d2=df[1][i], d3=df[2][i])

        # 电流测试
        sheet_data.Cells(5, 6).Value = " 1:{d1}".format(d1=df[3][i])
        sheet_data.Cells(5, 7).Value = " 2:{d1}".format(d1=df[4][i])
        sheet_data.Cells(5, 8).Value = " 3:{d1}".format(d1=df[5][i])

        sheet_data.Cells(6, 6).Value = " 1:{d1}".format(d1=df[6][i])
        sheet_data.Cells(6, 7).Value = " 2:{d1}".format(d1=df[7][i])
        sheet_data.Cells(6, 8).Value = " 3:{d1}".format(d1=df[8][i])

        sheet_data.Cells(7, 6).Value = " 1:{d1}".format(d1=df[9][i])
        sheet_data.Cells(7, 7).Value = " 2:{d1}".format(d1=df[10][i])
        sheet_data.Cells(7, 8).Value = " 3:{d1}".format(d1=df[11][i])

        # 供电方式
        if df[12][i] == '取电':
            sheet_data.Cells(8, 2).Value = "{d1}取电 {d2}内部电池 {d3}开关电源 {d4}太阳能 {d5}锂电池组".format(d1="☑", d2="□", d3="□", d4="□", d5="□")
        elif df[12][i] == '内部电池':
            sheet_data.Cells(8, 2).Value = "{d1}取电 {d2}内部电池 {d3}开关电源 {d4}太阳能 {d5}锂电池组".format(d1="□", d2="☑", d3="□", d4="□", d5="□")
        elif df[12][i] == '开关电源':
            sheet_data.Cells(8, 2).Value = "{d1}取电 {d2}内部电池 {d3}开关电源 {d4}太阳能 {d5}锂电池组".format(d1="□", d2="", d3="☑", d4="□", d5="□")
        elif df[12][i] == '太阳能':
            sheet_data.Cells(8, 2).Value = "{d1}取电 {d2}内部电池 {d3}开关电源 {d4}太阳能 {d5}锂电池组".format(d1="□", d2="□", d3="□", d4="☑", d5="□")
        else:
            sheet_data.Cells(8, 2).Value = "{d1}取电 {d2}内部电池 {d3}开关电源 {d4}太阳能 {d5}锂电池组".format(d1="□", d2="□", d3="□", d4="□", d5="☑")

        # 供电电压

        sheet_data.Cells(8, 6).Value = "内部电池：{d1}V 外部供电：{d2}V".format(d1=df[13][i],d2=df[14][i])

        # 通讯方式
        if df[15][i] == '有线':
            sheet_data.Cells(9, 2).Value = "{d1}有线 {d2}无线".format(d1="☑",d2="□")
        else:
            sheet_data.Cells(9, 2).Value = "□有线 ☑无线".format(d1="□",d2="☑")

        # 通讯媒介
        if df[16][i] == '内部GPRS模块':
            sheet_data.Cells(9, 5).Value = "{d1}内部GPRS模块 {d2}485 {d3}485转GPRS(卓兰模块)".format(d1="☑", d2="□", d3="□")
        elif df[16][i] == '485':
            sheet_data.Cells(9, 5).Value = "{d1}内部GPRS模块 {d2}485 {d3}485转GPRS(卓兰模块)".format(d1="□", d2="☑", d3="□")
        else:
            sheet_data.Cells(9, 5).Value = "{d1}内部GPRS模块 {d2}485 {d3}485转GPRS(卓兰模块)".format(d1="□" , d2="□", d3="☑")

        # 终端参数
        sheet_data.Cells(10, 3).Value = "{d1}".format(d1=df[17][i])
        sheet_data.Cells(10, 4).Value = "hex地址:{d1}".format(d1=df[18][i])
        if df[19][i] == 'OK':
            sheet_data.Cells(10, 8).Value = "终端复位:{d1}OK{d2}Error".format(d1="☑", d2="□")
        else:
            sheet_data.Cells(10, 8).Value = "终端复位:{d1}OK{d2}Error".format(d1="□", d2="☑")

        # 传输状态


open_excel("E:\自动化脚本（python）\智能接地箱监测终端.xls", 1, 1)
