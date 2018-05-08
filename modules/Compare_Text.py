#!/usr/bin/env python
import sys
import os
import csv
import difflib
import re

def compare_text_columns(table, column1Position, column2Position):
    similarity = list()
    for i in range(len(table)):
        sourceSentence = table[i][column1Position]
        targetSentence = table[i][column2Position]
        # Remove hyphen due to line break in German
        sourceSentence = re.sub(r'[A-Za-z]\- +(?!und |oder |bzw\. )[a-z]', r'\1\2', sourceSentence)
        table[i][column1Position] = sourceSentence
        targetSentence = re.sub(r'[A-Za-z]\- +(?!und |oder |bzw\. )[a-z]', r'\1\2', targetSentence)
        table[i][column2Position] = targetSentence
        similarity += [difflib.SequenceMatcher(None, sourceSentence, targetSentence).ratio()]
    return table, similarity


def insert_column_table(table, position, newColumn):
    # Insert newColumn as a list to table as a 2-dimension list, before column #position
    for i in range(len(table)):
        table[i].insert(position, newColumn[i])
    return table


def insert_blank_column_table(table, position):
    # Insert a blank column to table as a 2-dimension list, before column #position
    for i in range(len(table)):
        table[i].insert(position, '')
    return table


def write_table_csv(exportFile, table):
    with open(exportFile, 'wt') as csvfile:
        textWriter = csv.writer(csvfile, delimiter='\t')
        for i in range(len(table)):
            textWriter.writerow(table[i])
