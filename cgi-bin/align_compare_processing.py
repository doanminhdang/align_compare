#!/usr/bin/env python

# Import modules for CGI handling
import cgi, cgitb
import os, sys
import glob
import shutil

cgitb.enable()

cgi_bin_dir = os.getcwd()
aligner_scripts_dir = cgi_bin_dir.replace('/cgi-bin', '/align_compare/aligner/scripts')
os.environ['LD_LIBRARY_PATH'] = aligner_scripts_dir  # for web. Additional libraries for hunalign are put there.

server_name = os.environ["SERVER_NAME"]
#BASE_URL = 'http://localhost:8000'.rstrip('/')
BASE_URL = 'http://'+server_name+'/align_compare'.rstrip('/')  # for web
TOP_DIR = '../align_compare'.rstrip('/')
ALIGNER_DIR = 'aligner'
MODULE_DIR = 'modules'.rstrip('/')
DATA_DIR = 'data'
UPLOAD_DIR = 'uploads'.rstrip('/')
TEMP_RESULT_DIR = 'results'.rstrip('/')
OUTPUT_DIR = 'downloads'.rstrip('/')
#ABS_TOP_DIR = '/home/dang/Dropbox/Working/Sach_UBTT_Viet_Duc/Dien_dien_tu/Sosanh_C14'.rstrip('/')
ABS_TOP_DIR = '/home/minhdang/public_html/align_compare'.rstrip('/')  # for web
OUTPUT_FILE = 'results.zip'

# Note: running on localhost:8000, the TOP_DIR is '.', because the current directory
# is with the HTML file that calls to this Python script (upper dir)
# While running on web server of Hawkhost, TOP_DIR is '..'

from sys import path
path.append(TOP_DIR+'/'+MODULE_DIR)

import Textparser
import Pdfsplitter
import Auto_Align_Compare
import Csv_Excel

def create_user_dir(base_dir):
    """Create directory for the request, with the structure
    base_dir/YYYY/MM/DD/hour-minute-second, and output the relative path
    """
    from datetime import datetime
    # Create directory

    def generate_parent_dir():
        today = datetime.utcnow()

        relative_path_dir_year = str(today.year)
        relative_path_dir_month = os.path.join(relative_path_dir_year, str(today.month))
        relative_path_dir_day = os.path.join(relative_path_dir_month, str(today.day))
        relative_path_dir_now = os.path.join(relative_path_dir_day, str(today.hour)+'-'+str(today.minute)+'-'+str(today.second))

        path_dir_year = os.path.join(base_dir, relative_path_dir_year)
        path_dir_month = os.path.join(base_dir, relative_path_dir_month)
        path_dir_day = os.path.join(base_dir, relative_path_dir_day)

        if not os.path.exists(path_dir_year):
            os.makedirs(path_dir_year)

        if not os.path.exists(path_dir_month):
            os.makedirs(path_dir_month)

        if not os.path.exists(path_dir_day):
            os.makedirs(path_dir_day)

        return relative_path_dir_now


    relative_path_dir_time = generate_parent_dir()

    while os.path.exists(os.path.join(base_data_dir, relative_path_dir_time)):
        relative_path_dir_time = generate_parent_dir()

    os.makedirs(os.path.join(base_data_dir, relative_path_dir_time))

    return relative_path_dir_time


base_data_dir = os.path.join(TOP_DIR, DATA_DIR)
relative_user_dir = create_user_dir(base_data_dir)

os.makedirs(os.path.join(base_data_dir, relative_user_dir, UPLOAD_DIR))
os.makedirs(os.path.join(base_data_dir, relative_user_dir, TEMP_RESULT_DIR))
os.makedirs(os.path.join(base_data_dir, relative_user_dir, OUTPUT_DIR))

# Create instance of FieldStorage, it can only be initiated once per request
form = cgi.FieldStorage()

# Get data from fields
page_series_1 = form.getvalue('page_series_1')
if not page_series_1:  # set default value
    page_series_1 = '1'
page_series_2  = form.getvalue('page_series_2')
if not page_series_2:  # set default value
    page_series_2 = '1'

delete_data = form.getvalue('delete_data')
if not delete_data:  # set default value
    delete_data = 'yes'
language1 = form.getvalue('language1')
language2 = form.getvalue('language2')


def save_uploaded_file(cgi_form, form_field, upload_dir, whitelist_ext):
    """This saves a file uploaded by an HTML form.
       The form_field is the name of the file input field from the form.
       For example, the following form_field would be "file_1":
           <input name="file_1" type="file">
       The upload_dir is the directory where the file will be written.
       The whitelist_ext is the set of allowed file extensions for uploading.
       If no file was uploaded or if the field does not exist then
       this does nothing.
    """
    if not cgi_form.has_key(form_field): return False
    file_item = cgi_form[form_field]
    if not file_item.file: return False
    # Strip leading path from file name to avoid
    # directory traversal attacks.
    # Replace \ by / to make sure compatibility with Windows path
    filename_base = os.path.basename(file_item.filename.replace("\\", "/"))
    mainname, extname = os.path.splitext(filename_base)  # mainname is '123.php.', extname is '.jpg'
    # Use white list of file type to be uploaded
    if not extname in whitelist_ext: return False
    # Replace . by _ to protect against double extension attacks which can activate PHP scripts
    filename_base = mainname.replace('.', '_') + extname
    file_path = os.path.join(upload_dir, filename_base)
    with open(file_path, 'wb') as outfile:
        shutil.copyfileobj(file_item.file, outfile)
        # outfile.write(file_item.file.read())
        # while 1:
        #     chunk = file_item.file.read(100000)
        #     if not chunk: break
        #     outfile.write (chunk)
    return filename_base


pdf_ext  = set(['.pdf', '.PDF'])
text_ext = set(['.docx', '.DOCX', '.txt', '.TXT', '.doc', '.DOC'])

white_list = set()
white_list = white_list.union(pdf_ext)
white_list = white_list.union(text_ext)

file_input_1 = save_uploaded_file(form, "upload1", os.path.join(TOP_DIR, DATA_DIR, relative_user_dir, UPLOAD_DIR), white_list)
file_input_2 = save_uploaded_file(form, "upload2", os.path.join(TOP_DIR, DATA_DIR, relative_user_dir, UPLOAD_DIR), white_list)

if file_input_1:
    file_1_path = os.path.join(ABS_TOP_DIR, DATA_DIR, relative_user_dir, UPLOAD_DIR, file_input_1)
    url_file_1 = BASE_URL+'/'+DATA_DIR+'/'+relative_user_dir+'/'+UPLOAD_DIR+'/'+file_input_1
    message_file_1 = 'File 1: '+file_input_1+' was uploaded successfully.'
else:
    message_file_1 = 'File 1 is not an accepted file. It was not uploaded.'

if file_input_2:
    file_2_path = os.path.join(ABS_TOP_DIR, DATA_DIR, relative_user_dir, UPLOAD_DIR, file_input_2)
    url_file_2 = BASE_URL+'/'+DATA_DIR+'/'+relative_user_dir+'/'+UPLOAD_DIR+'/'+file_input_2
    message_file_2 = 'File 2: '+file_input_2+' was uploaded successfully.'
else:
    message_file_2 = 'File 2 is not an accepted file. It was not uploaded.'

proceed_flag = file_input_1 and file_input_2 and file_input_1!=file_input_2 and os.path.splitext(file_input_1)[1]==os.path.splitext(file_input_2)[1]

if proceed_flag:
    # Processing PDF files
    if os.path.splitext(file_1_path)[1] in pdf_ext:
        source_pages_list = Pdfsplitter.pdf_split_single_page_series(file_1_path, Textparser.parse_series(page_series_1))
        target_pages_list = Pdfsplitter.pdf_split_single_page_series(file_2_path, Textparser.parse_series(page_series_2))
        Auto_Align_Compare.auto_align_list_webcgi(source_pages_list, target_pages_list, TOP_DIR+'/'+ALIGNER_DIR+'/LF_aligner_3.11.sh', language1, language2)

    # Processing text files
    if os.path.splitext(file_1_path)[1] in text_ext:
        Auto_Align_Compare.auto_align_list_webcgi([file_1_path], [file_2_path], TOP_DIR+'/'+ALIGNER_DIR+'/LF_aligner_3.11.sh', language1, language2)

    # os.system('find ../data/uploads -maxdepth 2 -name aligned* > list_aligned_to_be_compared.txt')
    os.system('find '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+UPLOAD_DIR+' -maxdepth 2 -name aligned* > '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+UPLOAD_DIR+'/list_aligned_to_be_compared.txt')

    Auto_Align_Compare.auto_compare_file_list(TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+UPLOAD_DIR+'/list_aligned_to_be_compared.txt')

    # os.system('find ../data/uploads -maxdepth 2 -name compared* -exec mv {} ../data/results/ \;')
    os.system('find '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+UPLOAD_DIR+' -maxdepth 2 -name compared* -exec mv {} '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+TEMP_RESULT_DIR+'/ \;')

    # csv_paths = glob.glob('../data/results/*.csv')
    csv_paths = glob.glob(TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+TEMP_RESULT_DIR+'/*.csv')
    for csv_file in csv_paths:
        Csv_Excel.csv_to_xls(csv_file, csv_file+'.xls')

    [os.system('rm '+path_to_delete) for path_to_delete in csv_paths]

    # Result file to be given back
    # os.system('rm ../data/results.zip')
    # os.system('rm '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+OUTPUT_DIR+'/'+OUTPUT_FILE)
    # os.system('zip -r ../data/results.zip ../data/results')
    os.system('zip -r -j '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+OUTPUT_DIR+'/'+OUTPUT_FILE+' '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+TEMP_RESULT_DIR)

    url_file_result = BASE_URL+'/'+DATA_DIR+'/'+relative_user_dir+'/'+OUTPUT_DIR+'/'+OUTPUT_FILE


# Clean up
if not delete_data != 'yes':
    # os.system('rm -r ../data/results/*')
    os.system('rm -r '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+TEMP_RESULT_DIR+'/*')
    # os.system('rm -r ../data/uploads/*')
    os.system('rm -r '+TOP_DIR+'/'+DATA_DIR+'/'+relative_user_dir+'/'+UPLOAD_DIR+'/*')

# Output to the web
print "Content-type:text/html"
print ""
print "<html>"
print "<head>"
print "<title>Ket qua so sanh 2 file van ban de ho tro dich thuat</title>"
print "</head>"
print "<body>"
print "<h1>Results of aligner and comparer</h1>"
print "<h2>%s</h2>" % (message_file_1)
if delete_data != 'yes' and file_input_1:
    print "<h2>Link to the uploaded file 1: <a href=\"%s\">%s</a></h2>" % (url_file_1, url_file_1)
print "<h2>%s</h2>" % (message_file_2)
if delete_data != 'yes' and file_input_2:
    print "<h2>Link to the uploaded file 2: <a href=\"%s\">%s</a></h2>" % (url_file_2, url_file_2)
#print "<h3>File 1 path:%s</h3>" % (file_1_path)
#print "<h3>File 2 path:%s</h3>" % (file_2_path)
print "<h2>Series of PDF pages to compare are %s and %s</h2>" % (page_series_1, page_series_2)
if proceed_flag:
    print "<h2>Link to the RESULT file: <a href=\"%s\">%s</a></h2>" % (url_file_result, url_file_result)
if not delete_data != 'yes':
    print "<h2>Data (except the RESULT file) was deleted on the server.</h2>"
print "</body>"
print "</html>"
