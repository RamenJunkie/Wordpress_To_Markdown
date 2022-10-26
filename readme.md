# Wordpress to Markdown Files Converter

This isn't perfect, but it takes an exported wordpress XML archive and converts it into a series of single files in the format of YYYY.MM.DD - POST TITLE.md with the contents of the post itself inside.  It does a bit of clean up on the post data as well, but it's not perfect and does not catch everything.  This is mostly for quick "archival purposes" than anything else.  If you wanted to use it for something else you would probably want to manually touch up the files a bit.  

It does not download images but may still embed them as a side effect of the conversion.

## Requirements

Needs a few modules, _bs4_ (Beautiful Soup) for one, probably also _html_ and _lxml_ as well.  

Also you will need to create a folder "output_files" in the same folder where the script and XML file are.

## To Run

Put everything into one folder, run _python ./wp2markdown.py EXPORTFILENAME.py_ and it should output everything to "output_files".

If you want something besides a "." in the date format, you can edit the file and change the value of "sep" on line 15.  