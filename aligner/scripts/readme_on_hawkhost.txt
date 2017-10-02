Execute this command to set the library path to this local folder:
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/minhdang/public_html/align_compare/aligner/scripts
or set the environment in Python cgi-bin script:
import os
os.environ['LD_LIBRARY_PATH'] = '/home/minhdang/public_html/align_compare/aligner/scripts'
Reason: some libraries linked from LF_aligner are missing on Hawkhost server,
so Dang has collected those libraries in this folder (actually, they are needed by hunalign).
