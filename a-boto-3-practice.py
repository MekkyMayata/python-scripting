#!/usr/bin/env python3

# script: a-boto-3-practice
# fxn: gets list of s3 buckets and writes to desired file
# author: MekkyMayata

# Builtin Python Libraries
import os
import logging

# Third party Libraries
import boto3

# set logging level
# https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
# DEBUG < INFO < WARNING < ERROR < CRITICAL. DEFAULT: WARNING
logging.basicConfig(level=logging.INFO)
logger1 = logging.getLogger('file_logger')


def s3_pull() -> list:
    """
    pulls existing s3 buckets and
    appends result to a list
    :return: list
    """
    s3 = boto3.resource('s3')
    s3_buckets = []
    for bucket in s3.buckets.all():
        s3_buckets.append(bucket.name)
    return s3_buckets


def create_file(filename: str) -> None:
    """
    creates a file and appends
    s3 bucket names
    :param filename: str
    :return: None
    """
    file = filename
    logger1.debug('FILE LOCATION: {}'.format(file))

    # file does NOT exist
    if not os.path.isfile(file):
        logger1.info('FILE DOES NOT EXIST, CREATING...')
        with open(file, 'w') as f:
            for i in s3_pull():
                f.write(i + '\n')
        logger1.info('WRITE(S) COMPLETE.')
    else:
        logger1.info('FILE EXISTS')
        with open(file, 'r+') as f:
            # file is EMPTY
            if os.path.getsize(file) == 0:
                for i in s3_pull():
                    f.write(i + '\n')
            elif list(f)[-1].split('\n')[0] != s3_pull()[-1]:
                for i in s3_pull():
                    f.write(i + '\n')
    logger1.info('WRITE(S) COMPLETE.')


if __name__ == '__main__':
    create_file(str(input("enter file name here: ")))
