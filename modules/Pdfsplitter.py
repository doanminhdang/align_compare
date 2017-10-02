#!/usr/bin/env python
# Author: Dang Doan
# Date: 2017-09-25

def pdf_split(inFile, firstPage, lastPage='', outFile=''):
    """Call Ghostscript to split pages in the PDF inFile to a new PDF file
    Example:
    output = pdf_split('sources/Chuong_14_Dien_Auflage_27.pdf',3)
    pdf_split('sources/Chuong_14_Dien_Auflage_27.pdf',3,30)
    pdf_split('sources/Chuong_14_Dien_Auflage_27.pdf',3,30,'sources/output.pdf')
    output is a string
    """
    import os

    if lastPage == '':
        lastPage = firstPage

    if outFile == '':
        output_file = inFile + '_split.pdf'
    else:
        output_file = outFile

    gs_command_base = ['gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dSAFER -dFirstPage=',\
        ' -dLastPage=', ' -sOutputFile=']
    gs_command_params = [str(firstPage), str(lastPage), output_file + ' ' + inFile]
    gs_command = ''

    for k in range(len(gs_command_base)):
        gs_command += gs_command_base[k] + gs_command_params[k]

    os.system(gs_command)

    return output_file


def pdf_split_page(inFile, pageNumber, outFile=''):
    """Accepts pageNumber as either a page like '2', or a range like '2-4'
    output is a list of strings
    """
    numbers = pageNumber.split('-')

    if outFile == '':
        output_base = inFile + '_split'
    else:
        output_base = outFile
    output_path = output_base + '_p' + str(pageNumber) + '.pdf'

    output = []

    if len(numbers)>1:
        output.append(pdf_split(inFile, numbers[0], numbers[1], output_path))
    else:
        output.append(pdf_split(inFile, numbers[0], '', output_path))

    return output


def pdf_split_page_series(inFile, pageSeries, outFile=''):
    """Split files according to a series of pages
    Example:
    output = pdf_split_page_series('sources/Chuong_14_Dien_Auflage_27.pdf',['1-3', '5', '8-10'])
    output is a list of strings
    """
    output = []
    for page_number in pageSeries:
        output.extend(pdf_split_page(inFile, page_number, outFile))

    return output


def pdf_split_single_page(inFile, pageNumber, outFile=''):
    """Accepts pageNumber as either a page like '2', or a range like '2-4'
    output is a list of strings
    """
    numbers = pageNumber.split('-')

    if outFile == '':
        output_base = inFile + '_split'
    else:
        output_base = outFile

    output = []

    if len(numbers)>1:
        for k in range(int(numbers[0]), int(numbers[1])+1):
            current_path = output_base + '_p' + str(k) + '.pdf'
            output.append(pdf_split(inFile, k, '', current_path))
    else:
        single_path = output_base + '_p' + str(pageNumber) + '.pdf'
        output.append(pdf_split(inFile, numbers[0], '', single_path))

    return output


def pdf_split_single_page_series(inFile, pageSeries, outFile=''):
    """Split files according to a series of pages
    Example:
    pdf_split_single_page_series('sources/Chuong_14_Dien_Auflage_27.pdf',['1-3', '5', '8-10'])
    output is a list of strings
    """
    output = []
    for page_number in pageSeries:
        output.extend(pdf_split_single_page(inFile, page_number, outFile))

    return output
