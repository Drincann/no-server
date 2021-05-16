'''
directions:传入年和月以及查询的中心经纬度以及范围，画出相对应的图。
功能1:只输入年份，月份输入0或者不传这个参数，实现画12个月折线图+全年分布图的功能。
功能2:输入年份和月份，输出该月份下的分布图。
@param Central_Longitude: 查询的中心经度
@param Central_Latitude: 查询的中心纬度
@param kmScale: 想查询附近多大范围的，单位为km
@param year: 想查询的年份，YYYY
@param month: 想查询的月份，可以不传参，默认为0
@return:
'''
import getopt
from logging import error

import HLWP1_calAve

import sys


def argvParser():
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "",
            ["minlat=", "maxlat=", "minlon=", 'maxlon=', 'year=', 'month=']
        )
    except getopt.GetoptError:
        print(
            """
{
  "code": 1,
  "message": "参数解析失败"
}
        """
        )
        sys.exit(0)
    argMap = {}
    for opt, val in options:
        argMap[opt] = val
    return argMap


argMap = argvParser()
assert (
    '--minlat' in argMap
    and '--maxlat' in argMap
    and '--minlon' in argMap
    and '--maxlon' in argMap
    and '--year' in argMap
    and '--month' in argMap
)
try:
    imgBase64 = HLWP1_calAve.query(
        float(argMap['--minlat']), float(argMap['--maxlat']),
        float(argMap['--minlon']), float(argMap['--maxlon']),
        int(argMap['--year']), int(argMap['--month'])
    )
except BaseException as e:
    print(
        """
    {{
      "code": 1,
      "message": "{message}"
    }}
  """.format(message=str(e))
    )
else:
    print(
        """
      {{
        "code": 0,
        "imgBase64": "{imgBase64}"
      }}
      """.format(imgBase64=imgBase64)
    )
