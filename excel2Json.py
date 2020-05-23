import xlrd
from collections import OrderedDict
import json


def excel2json(file):
    wb = xlrd.open_workbook(file)
    convert_list = []
    sh = wb.sheet_by_index(0)
    title = sh.row_values(0)  # get row(0) as json key
    for rownum in range(1, sh.nrows):  # row lines
        rowvalue = sh.row_values(rownum)
        single = OrderedDict()
        for colnum in range(0, len(rowvalue), 2):  # colnum lines
            # print("key:{0}, value:{1}".format(title[colnum], rowvalue[colnum]))
            json_value = rowvalue[colnum]
            if isinstance(json_value, float):
                single[title[colnum]] = str(int(json_value))
            else:
                single[title[colnum]] = rowvalue[colnum]
        convert_list.append(single)

    j = json.dumps(convert_list, indent=4)  # convertjson.dumps into str & line break

    with open(path.split('.')[0]+".json", "w", encoding="utf8") as f:
        f.write(j+"\n")

if __name__ == '__main__':
    path = "D:\\monitor_host\\cubcus.xlsx"
    excel2json(path)
