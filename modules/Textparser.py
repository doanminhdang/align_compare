#!/usr/bin/env python
# Author: Dang Doan
# Date: 2017-09-25

def parse_series(numberSeries):
    """Parsing a string like '1, 2, 3 - 4' to a series of numbers
    All letters [], () and spaces will be removed
    """
    import re
    # no_space_text = numberSeries.replace(' ','')
    # no_space_text = no_space_text.replace('[','')
    # no_space_text = no_space_text.replace(']','')
    # no_space_text = no_space_text.replace('(','')
    # no_space_text = no_space_text.replace(')','')

    no_space_text = re.sub(r'[^0-9,\-]', '',numberSeries)

    text_list = no_space_text.split(',')

    return text_list
