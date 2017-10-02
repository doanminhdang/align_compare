#!/usr/bin/env python
# Author: Dang Doan
# Date: 2017-09-12

#def call_lf_aligner_sh(inFile1, inFile2, lfAlignerSh = './LF_aligner_3.11.sh'):
    #"""Call LF aligner to automatically align two files
    #"""
    #from subprocess import Popen, PIPE
    #import time

    #p = Popen([lfAlignerSh], stdin=PIPE, shell=False)
    #p.stdin.write('\n')  # Default languages = 2
    #p.stdin.write(inFile1+'\n')  # First file
    #p.stdin.write(inFile2+'\n')  # Second file
    #time.sleep(1)
    #p.stdin.write('\n')  # "Pdf to txt conversion done... press enter to skip the review"
    #time.sleep(3)
    #p.stdin.write('\n')  # "Died at ./scripts/LF_aligner_3.11_with_modules.pl line 53384, <STDIN> line 5."
    ## This enter is to exit

def call_lf_aligner_pdf(inFile1, inFile2, lfAlignerSh = './LF_aligner_3.11.sh'):
    """Call LF aligner to automatically align two PDF files
    Example:
    call_lf_aligner_pdf('./pdfs/v27_001.pdf', './pdfs/v30_001.pdf', './LF_aligner_3.11.sh')
    or full path version for sure:
    call_lf_aligner_pdf('/home/dang/software/aligner/v27_001.pdf', '/home/dang/software/aligner/v30_001.pdf', '/home/dang/software/aligner/LF_aligner_3.11.sh')
    """
    import os

    from subprocess import Popen, PIPE
    import time

    # To debug: do not use FNULL, so the full output of LF_aligner is displayed
    # p = Popen([lfAlignerSh], stdin=PIPE, shell=False)

    # To use on web: use FNULL, otherwise output of LF_aligner is displayed on the web page

    FNULL = open(os.devnull, 'w')
    p = Popen([lfAlignerSh], stdin=PIPE, shell=False, stdout=FNULL)
    p.stdin.write('\n')  # Default languages = 2
    p.stdin.write(inFile1+'\n')  # First file
    p.stdin.write(inFile2+'\n')  # Second file
    time.sleep(1)
    p.stdin.write('\n')  # "Pdf to txt conversion done... press enter to skip the review"
    time.sleep(4)
    p.stdin.write('\n')  # "Died at ./scripts/LF_aligner_3.11_with_modules.pl line 53384, <STDIN> line 5."
    # This enter is to exit


def call_lf_aligner_text(inFile1, inFile2, lfAlignerSh = './LF_aligner_3.11.sh'):
    """Call LF aligner to automatically align two text files, eg. DOCX, DOC, TXT
    Note: with two text files, it requires one less enter than PDF files during the interaction
    """
    import os

    from subprocess import Popen, PIPE
    import time

    # To debug: do not use FNULL, so the full output of LF_aligner is displayed
    # p = Popen([lfAlignerSh], stdin=PIPE, shell=False)

    # To use on web: use FNULL, otherwise output of LF_aligner is displayed on the web page

    FNULL = open(os.devnull, 'w')
    p = Popen([lfAlignerSh], stdin=PIPE, shell=False, stdout=FNULL)
    p.stdin.write('\n')  # Default languages = 2
    p.stdin.write(inFile1+'\n')  # First file
    p.stdin.write(inFile2+'\n')  # Second file
    time.sleep(5)  # Wait for processing, no need to press enter during this time
    p.stdin.write('\n')  # "Died at ./scripts/LF_aligner_3.11_with_modules.pl line 53384, <STDIN> line 4."
    # This enter is to exit


def call_lf_aligner_auto(inFile1, inFile2, lfAlignerSh = './LF_aligner_3.11.sh', lang1 = 'de', lang2 = 'de'):
    """Set the right language codes and file type in file LF_aligner_setup.txt,
    then pass parameters to either call_lf_aligner_pdf or call_lf_aligner_text.
    """
    import re

    aligner_dir = lfAlignerSh.replace('/LF_aligner_3.11.sh', '')  # no trailing / in directory
    setup_file = aligner_dir+'/LF_aligner_setup.txt'
    pdf_ext  = set(['.pdf', '.PDF'])
    text_ext = set(['docx', 'DOCX', '.txt', '.TXT', '.doc', '.DOC'])
    # More restriction on the allowed languages, if we want:
    # lang1_set = set(['de', 'en', 'fr', 'vi'])
    # lang2_set = set(['de', 'en', 'fr', 'vi'])
    # if not lang1 in lang1_set: lang1 = 'de'
    # if not lang2 in lang1_set: lang2 = 'de'

    filetype_pattern = r'Filetype default \(t/c/com/epr/w/h/p\): \[.*\]'
    language1_pattern = r'Language 1 default: \[..\]'
    language2_pattern = r'Language 2 default: \[..\]'

    filetype_setup_pdf = 'Filetype default (t/c/com/epr/w/h/p): [p]'
    filetype_setup_text = 'Filetype default (t/c/com/epr/w/h/p): [t]'
    language1_setup_line = 'Language 1 default: ['+lang1+']'
    language2_setup_line = 'Language 2 default: ['+lang2+']'

    with open(setup_file, "rt") as objFile:
        txtFile = objFile.read()
    # Set languages in the setup file
    txtFile = re.sub(language1_pattern, language1_setup_line, txtFile)
    txtFile = re.sub(language2_pattern, language2_setup_line, txtFile)

    if inFile1[-4:] in pdf_ext:
        txtFile = re.sub(filetype_pattern, filetype_setup_pdf, txtFile)
        with open(setup_file, "wt") as objFile:
            objFile.write(txtFile)
        call_lf_aligner_pdf(inFile1, inFile2, lfAlignerSh)
    elif inFile1[-4:] in text_ext:
        txtFile = re.sub(filetype_pattern, filetype_setup_text, txtFile)
        with open(setup_file, "wt") as objFile:
            objFile.write(txtFile)
        call_lf_aligner_text(inFile1, inFile2, lfAlignerSh)
