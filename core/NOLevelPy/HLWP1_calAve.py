from netCDF4 import Dataset
from numba import jit
import numpy as np
import os
import matplotlib.pyplot as plt
import HLWP1_Drawing
from os import path


def resolvePath(relativePath):
    from pathlib import Path as path
    return str(path(__file__).parent.absolute().joinpath(relativePath))


@jit(nopython=True)
def binary_search(arr, x):
    """二分查找， 非递归"""
    n = len(arr)
    first = 0
    last = n - 1
    while last - first > 2:
        mid = (first + last) // 2
        # if x < arr[mid] and arr[mid]-x>arr[mid]-arr[mid-1]:
        #     last = mid-1
        # elif x < arr[mid] and arr[mid]-x<=arr[mid]-arr[mid-1]:
        #     first=mid-1
        # elif x >= arr[mid] and x-arr[mid]<=arr[mid+1]-arr[mid]:
        #     last = mid+1
        # else:
        #     first = mid+1
        # 下方代码是对上方代码的简化，减少了一些运算，会节省一点时间。
        if x < arr[mid]:
            if arr[mid] - x > arr[mid] - arr[mid - 1]:  # 在外部
                last = mid - 1
            else:  # 在内部
                first = mid - 1
                last = mid
        else:
            if x - arr[mid] > arr[mid + 1] - arr[mid]:  # 在外部
                first = mid + 1
            else:  # 在内部
                last = mid + 1
                first = mid
    mid = (first + last) // 2
    if x - arr[first] < arr[mid] - x:
        return first
    elif arr[last] - x < x - arr[mid]:
        return last
    else:
        return mid


def calAve(minlon, maxlon, minlat, maxlat):
    # path = "F:/06 steam/shuju/step3/uv_output/"+str(year)
    path = resolvePath("./data")
    files = os.listdir(path)
    files.sort()
    lat = []
    lon = []
    E = []
    for i in range(len(files)):
        filename = path+'/'+files[i]
        E_fh = Dataset(filename)
        # E_fh=Dataset("./MEIC/all_MEIC_ind_add_pow.nc")
        lat = E_fh.variables['lat'][:]
        lon = E_fh.variables['lon'][:]
        E_average = E_fh.variables['v_average'][:]
        E.append(E_average)
        E_fh.close()

    # 读取进来经纬度范围、时间。
    # 如果月份==0，则代表只输了年份：每个月区域都需要算。（也就是这个代码来实现折线图的预备处理）
    # 否则：只需作出分布图来
    posminLat = binary_search(lat, minlat)
    posmaxLat = binary_search(lat, maxlat)
    posminLon = binary_search(lon, minlon)
    posmaxLon = binary_search(lon, maxlon)
    ave = []
    # 用切片亦可
    for k in range(len(files)):
        cnt = 0
        avetmp = 0
        for i in range(posminLat, posmaxLat+1):
            for j in range(posminLon, posmaxLon+1):
                if np.isnan(E[k][i][j]):
                    continue
                cnt += 1
                avetmp += E[k][i][j]
        avetmp /= cnt
        ave.append(avetmp)
    return ave


def plotMonthE(y_axis_data, savepath, year):
    x_axis_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    plt.figure(figsize=(2.8565354, 2.7791732))
    # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，线的宽度和标签
    plt.plot(x_axis_data, y_axis_data, 'x-', color='#000000', linewidth=1)
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(x_axis_data)  # 设置横坐标刻度为给定的月份
    plt.ylim([0, 40])  # 设置纵坐标轴范围
    plt.savefig(savepath + '/' + str(year) + '.jpg', dpi=1200)  # 保存该图片
    plt.clf()


def query(minlat, maxlat, minlon, maxlon, year, month=0):
    # Central_Longitude,Central_Latitude,kmScale,year=120.9,37.5,100,2019
    # # month=0
    if minlon < 70 or maxlon > 140 or minlat < 15 or maxlat > 55:
        print('范围有误')
        quit()

    if month == 0:
        # 调用全年求平均的函数
        ave = calAve(minlon, maxlon, minlat, maxlat)
        # ave=[15,17,25,2,22,14,5,20,39,11,33,16]
        # 调用画折线图的函数
        savepath = resolvePath('./output')
        plotMonthE(ave, savepath, year)

        # 调用画年分布图的函数
        # 调用一年整个的nc文件，自己改路径吧，文件名YYYY.nc
        filename = resolvePath('./data/' + str(year)+'.nc')
        dataName = 'v_average'
        # cbarticks = [-10, -5, 0, 5]
        cbarticks = [0, 0.5, 1, 1.5, 2]
        savePath = resolvePath('./output/' + str(year)+'.png')
        return HLWP1_Drawing.DrawingMini(
            filename, dataName, minlon, maxlon, minlat, maxlat, cbarticks, savePath)

    else:
        # 调用画某月份图分布图的函数
        # 调用某个月的nc文件，自己改路径吧。文件名YYYYMM.nc
        # filename = 'F:/06 steam/shuju/step3/uv_output/' + str(year) + '/' + str(year)+str(month).zfill(2)+'.nc'
        filename = resolvePath('./data/' + str(year) +
                               str(month).zfill(2) + '.nc')
        dataName = 'v_average'
        # dataName = 'no2'
        # barticks = [-10, -5, 0, 5]
        cbarticks = [0, 0.5, 1, 1.5, 2]
        savePath = resolvePath('./output/' + str(year) +
                               str(month).zfill(2)+'.png')
        return HLWP1_Drawing.DrawingMini(
            filename, dataName, minlon, maxlon, minlat, maxlat, cbarticks, savePath)
