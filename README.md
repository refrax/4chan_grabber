4chan_grabber
=============

Downloading of files using 4chan's read-only JSON API

Written for Python 3

Run the script from the commandline, passing it two arguments, the first being the board on 
4chan you want to search, and the second being the searchterm.

i.e. <4chan.py b reaction> or <4chan.py wg landscape>

The config.ini.example file is how you set the directory to download to. Rename the file to 
config.ini and replace the saveto variable to whatever directory you want the files saved to. 
Be sure to include a trailing slash at the end of the directory.

The directory structure would be as follows:
  saveto directory>
    boardname>
      searchterm #1>
      searchterm #2>
      searchterm #3>
