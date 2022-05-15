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
    # get current s3 buckets and append them to a file
    s3 = boto3.resource('s3')
    s3_buckets = []
    for bucket in s3.buckets.all():
        s3_buckets.append(bucket.name)
    return s3_buckets


def create_file(filename: str) -> None:
    file = filename
    logger1.debug('FILE LOCATION: {}'.format(file))

    # create file if NOT exist
    if not os.path.isfile(file):
        logger1.info('FILE DOES NOT EXIST, CREATING...')
        with open(file, 'a') as f:
            for i in s3_pull():
                f.write(i + '\n')
        logger1.info('WRITE(S) COMPLETE.')


if __name__ == '__main__':
    create_file(str(input("enter file name here: ")))
