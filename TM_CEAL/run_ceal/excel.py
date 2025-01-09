# coding=utf-8
import xlrd

Excel = xlrd.open_workbook(filename="../TM.xls")
table=Excel.sheet_by_name('Patient classes')
rows = table.nrows
cols=table.ncols


with open("label.txt","w") as f:

    for i in range(len(table.col_values(0))):
        if i == 0:
            continue
        patient=table.cell_value(i,0)
        label=table.cell_value(i,6)
        f.write(str(patient) + ' ' + str(int(label)))
        f.write('\n')
