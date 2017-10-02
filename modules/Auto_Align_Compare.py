#!/usr/bin/env python
# Author: Dang Doan
# Date: 2017-09-13

import sys
import os
import csv
# import unicodedata
import difflib

import Aligner
import Compare_Text

def get_list_from_file(fileOfList):
    """fileOfList = './list_pdfs_1.txt"""
    list_path = []

    with open(fileOfList, 'r') as listOfFile:
        for line in listOfFile:
            filePath = line.rstrip('\n')
            list_path.append(filePath)

    return list_path


def auto_align_list(filesSource, filesTarget, lfAlignerSh = '../LF_aligner_3.11.sh', lang1='de', lang2='de'):
    if len(filesSource) != len(filesTarget):
        raise ValueError('Numbers of source and target files are not equal')

    for kk in range(len(filesSource)):
        Aligner.call_lf_aligner_auto(filesSource[kk], filesTarget[kk], lfAlignerSh, lang1, lang2)


def auto_align_list_webcgi(filesSource, filesTarget, lfAlignerSh = './LF_aligner_3.11.sh', lang1='de', lang2='de'):
    """This copy of function is to cope with the web version using cgi-bin
    Note the change of path to LF_aligner
    """
    if len(filesSource) != len(filesTarget):
        raise ValueError('Numbers of source and target files are not equal')

    for kk in range(len(filesSource)):
        Aligner.call_lf_aligner_auto(filesSource[kk], filesTarget[kk], lfAlignerSh, lang1, lang2)


def auto_align_file_list(seriesSource, seriesTarget, lfAlignerSh = '../LF_aligner_3.11.sh', lang1='de', lang2='de'):
    """seriesSource = './list_pdfs_1.txt'
    seriesTarget = './list_pdfs_2.txt'"""
    filesSource = get_list_from_file(seriesSource)
    filesTarget = get_list_from_file(seriesTarget)

    auto_align_list(filesSource, filesTarget, lfAlignerSh, lang1, lang2)


def auto_compare_list(listOfFile):
    """listOfFile is a list of path to files"""
    for filePath in listOfFile:
        table = list(csv.reader(open(filePath, 'rt'), delimiter='\t'))
        table, similarity = Compare_Text.compare_text_columns(table, 0, 1)
        table = Compare_Text.insert_blank_column_table(table, 2)
        table = Compare_Text.insert_column_table(table, 2, similarity)
        exportFile = os.path.join(os.path.dirname(filePath), 'compared_'+os.path.basename(filePath)+'.csv')
        Compare_Text.write_table_csv(exportFile, table)
        print("Data has been written to new file: "+exportFile)


def auto_compare_file_list(seriesFile):
    """seriesFile = './list_aligned.txt'"""
    list_path = get_list_from_file(seriesFile)
    auto_compare_list(list_path)
