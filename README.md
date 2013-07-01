# Kiehinen 

_finnish for feather stick_

Can be used to manage the Amazon Kindle. Still in pre-beta -stage.

Developed on 'new' 3G (v 3.0.1) - but should work with 2.x as well.

Written in Python 2.7 and !PyQt4 / PySide - libraries are Python 3.x compliant

## Features
 * Can display and manage collections and books.
 * Can parse .mobi (BOOKMOBI) and .prc (TEXtREAd) files to extract relevant data
 * Can add/remove books to/from collections in GUI

## TODO
 * Try to understand .mbp (BPARMOBI)
 * Add support for .pdf
 * Epub to mobi conversion
 * Drag & drop to add books to Kindle

## Documentation

1. Check out the source
1. edit `kiehinen.conf` so that `kindle_path` points to the kindle root directory, `/media/Kindle` on most modern linuxes
1. run the program `./kiehinen &> kiehinen.log`
1. when the program crashes, send `kiehinen.log` to `k+kindle@77.fi`

In order to run *kiehinen*, you need to have Qt4, BeautifulSoup and simplejson for Python installed. If you are running a debian you can get them by doing `sudo apt-get install python-simplejson python-qt4 python-beautifulsoup`

