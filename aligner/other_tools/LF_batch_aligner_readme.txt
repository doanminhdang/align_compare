LF batch aligner version 2.41
by András Farkas


XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
NOTE: THIS BATCH ALIGNER IS DEPRECATED! PLEASE SEE THE NEW BATCH ALIGNMENT MODE IN THE MAIN README.
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX



The batch mode aligner allows you to align several file pairs in one go. It is a mutation of the "normal" LF aligner, so this readme only covers the things that are specific to batch mode.

Using the batch aligner is a better solution than just merging your files into one and aligning them in one go that way, because in batch mode, files are handled separately. I.e. the individual file names are added as a note to each segment to allow you to tell afterwards where a segment came from, and if there is a problem with one file pair (one file much shorter than the other etc.) the issue won't affect the rest of the project.

How it works
The basic idea is that you create a tab separated txt file with a list of file pairs you want to align and then you tell the aligner to align each of them (the list has to contain full file paths). The files can be txt, docx, pdf or html (they all have to be the same type) and they can be anywhere on your computer. The aligner then loops through the file pairs one by one. If something is wrong with a file pair, it is skipped and the aligner moves on to the next file pair. In the scripts folder, you'll find two log files with info on how the alignment went. With the correct settings, the aligner can run unattended, i.e. you can start it, leave your computer and come back when all the files are done. You'll probably want to make (most of) these settings in batch_aligner_setup.txt, or else the batch mode won't offer much of an advantage over just running the normal aligner several times.

Howto
To create the input txt with Total Commander: select all the language 1 files in TCMD, click Commands/Copy full names to clipboard. Paste into Excel. Repeat with language 2, paste into the next column to the right in Excel.
Copy the whole two-column table to a text editor and save in ANSI encoding or in UTF-8 without a BOM.
Then make your settings in the setup file, start the batch aligner, drag&drop the txt and off you go. The output files will be in the folder where the batch file is.