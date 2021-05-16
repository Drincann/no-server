import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import shapefile
from cartopy.crs import PlateCarree, LambertConformal
from cartopy._crs import Geodetic
from matplotlib.ticker import MaxNLocator
import matplotlib.colorbar as colorbar
from netCDF4 import Dataset
from matplotlib import ticker, cm
import matplotlib as mpl
import cartopy.io.shapereader as shpreader
import base64
import io


def resolvePath(relativePath):
    from pathlib import Path as path
    return str(path(__file__).parent.absolute().joinpath(relativePath))


# 控制字体大小，不重要。原来是20，适当调小一些似乎显得图片上档次


def DrawingMini(filename, dataName, lonMin, lonMax, latMin, latMax, cbarticks, savePath):
    plt.rcParams.update({'font.size': 15})
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    fh = Dataset(filename, mode='r')
    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    data = fh.variables[dataName][:]
    # data=data*10**3
    # data=data*10**3
    # data = data * (10 ** -16)
    fh.close()
    nx = data.shape[1]
    ny = data.shape[0]
    proj = ccrs.PlateCarree()
    ax = fig.subplots(1, 1, subplot_kw={'projection': proj})

    chinaProvince = shpreader.Reader(
        resolvePath('./Data_ipynb/cn_province.dbf')).geometries()
    # 绘制中国国界省界九段线等等
    ax.add_geometries(chinaProvince, proj, facecolor='none',
                      edgecolor='black', linewidth=2, zorder=1)

    extent = [lonMin, lonMax, latMin, latMax]
    ax.set_extent(extent, proj)

    # gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
    #   linewidth=0.6, color='k', alpha=0.5, linestyle='--')
    # #正常程序
    # gl.xlabels_top = False
    # gl.ylabels_right = False
    # gl.xformatter = LONGITUDE_FORMATTER
    # gl.yformatter = LATITUDE_FORMATTER

    norm = mpl.colors.Normalize(vmin=cbarticks[0], vmax=cbarticks[-1])
    im = ax.pcolormesh(
        lons, lats, data, transform=ccrs.PlateCarree(), cmap=cm.Spectral_r, norm=norm)
    # position=fig.add_axes([0.7, 0.17, 0.15, 0.012])
    # position=fig.add_axes([0.2, 0.05, 0.5, 0.012])
    cb = plt.colorbar(im, aspect=35, shrink=0.8)  # aspect左右缩进，越小越宽
    font = {'size': 16, }
    # cb.set_label('×$\mathregular{10^{16}}$ kg/s', fontdict=font)
    cb.set_ticks(cbarticks)
    cb.ax.tick_params(labelsize=18)

    pic_IObytes = io.BytesIO()
    plt.savefig(savePath, dpi=600, format='jpg')
    plt.savefig(pic_IObytes, dpi=600, format='jpg')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read()).decode('ascii')

    # plt.show()
    return pic_hash
   # print('画图完毕')
