#!/usr/bin/python3

import os
import logging
import sys


logging.basicConfig(
    handlers = [logging.FileHandler('nfte.log'), logging.StreamHandler()],
    level = logging.INFO,
    format = '%(asctime)s  -  %(levelname)s:%(funcName)s \n%(message)s')

try:
    TABLO_IP = os.environ['TABLO_IP']
    if os.environ['DELETE_AFTER_EXPORT'].lower() in ['true', 'yes']:
        DELETE_AFTER_EXPORT = True
    else:
        DELETE_AFTER_EXPORT = False
except:
    logging.exception('Errors loading environment variables.')
    sys.exit(1)

MOVIES_EXPORT_PATH = '/nofrills_tablo_export/export/movies'
SERIES_EXPORT_PATH = '/nofrills_tablo_export/export/tv'
SPORTS_EXPORT_PATH = '/nofrills_tablo_export/export/sports'
INCOMPLETE_EXPORT_PATH = '/nofrills_tablo_export/export/incomplete'
FFMPEG_EXE_PATH = '/usr/bin/ffmpeg'
INCOMPLETE_PAD_SECONDS = 60         # how many seconds lost from the end of a video before it is considered incomplete
