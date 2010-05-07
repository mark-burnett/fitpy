import os
import logging
import collections

def getLogger(filename):
    long_name, junk = os.path.splitext(filename)
    begining, end = os.path.split(long_name)
    logger_name = ''
    while not ('fitpy' == end):
        logger_name = '.'+  end + logger_name
        begining, end = os.path.split(begining)
    else:
        logger_name = end + logger_name

    return logging.getLogger(logger_name)

