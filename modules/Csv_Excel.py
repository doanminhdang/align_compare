#!/usr/bin/env python
# Author: Dang Doan
# Date: 2017-09-21
# Note: Compatible to Python 2 only

from sys import path
#path.append('./xlrd-1.1.0')  # Download and untar module xlrd from https://pypi.python.org/pypi/xlrd
#path.append('./xlwt-1.3.0')  # Download and untar module xlrd from https://pypi.python.org/pypi/xlwt
# Note: xlrd-1.1.0 and xlwt-1.3.0 must be put in two places:
#   In the top directory, so that it is called by the cgi-bin script
#   In the directory modules, so that it is called by script running in terminal
path.append('../align_compare/xlrd-1.1.0')  # for web
path.append('../align_compare/xlwt-1.3.0')  # for web


def detect_encoding(fileName):

    import chardet

    with open(fileName, 'rb') as filebyte:
        rawdata = b''.join(filebyte.readlines())
        encoding = chardet.detect(rawdata)['encoding']

    return encoding


def xls_to_csv(xlsFile, csvFile, sheetName = 'Sheet1'):
    """Convert Excel XLS file to CSV file
    Example:
    xls_to_csv('v27_002-v30_002.xls', 'v27_002-v30_002.csv', 'Sheet1')
    """
    import xlrd
    import csv

    work_book = xlrd.open_workbook(xlsFile)
    work_sheet = work_book.sheet_by_name(sheetName)
    with open(csvFile, 'wb') as file_in:
        text_writer = csv.writer(file_in, delimiter='\t', quoting=csv.QUOTE_ALL)
        for rownum in range(work_sheet.nrows):
            text_writer.writerow(
                list(x.encode('utf-8') if type(x) == type(u'') else x
                    for x in work_sheet.row_values(rownum)))


def csv_to_xls(csvFile, xlsFile, sheetName = 'Sheet1'):
    """Convert Csv file to Excel XLS file
    Example:
    csv_to_xls('v27_002-v30_002.csv', 'v27_002-v30_002.xls', 'Sheet1')
    """
    import csv
    import xlwt
    import re

    int_re = re.compile(r'^-?\d+$')
    float_re = re.compile(r'^-?\d+\.\d+$')
    date_re = re.compile(r'^\d+\-\d+\-\d+$')

    style = xlwt.XFStyle()

    work_book = xlwt.Workbook()
    work_sheet = work_book.add_sheet(sheetName)
    with open(csvFile, 'rt') as file_out:
        text_reader = csv.reader(file_out, delimiter='\t')
        for r, row in enumerate(text_reader):
            for c, val in enumerate(row):
                unicode_val = val.decode('utf-8')
                # The following code block specifie the cell format in Excel
                # without this block, all values are entered to the cell as text
                format = 'general'
                if re.match(date_re, unicode_val):
                    format = 'M/D/YY'
                elif re.match(float_re, unicode_val):
                    unicode_val = float(unicode_val)
                    format = '0.0000'
                elif re.match(int_re, unicode_val):
                    unicode_val = float(unicode_val)
                    format = '0'
                style.num_format_str = format
                work_sheet.write(r, c, unicode_val, style)

    work_book.save(xlsFile)
