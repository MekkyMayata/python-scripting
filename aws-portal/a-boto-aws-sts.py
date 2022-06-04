#!/usr/bin/env python3

# script: a-boto-aws-sts
# author: MekkyMayata

# Builtin Python Libraries
import os
import logging
import configparser

# Third party Libraries
import boto3

# set logging level
# https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
# DEBUG < INFO < WARNING < ERROR < CRITICAL. DEFAULT: WARNING
logging.basicConfig(level=logging.INFO)

# configParser
config_parser = configparser.ConfigParser()


def get_sts_creds(role_arn: str, role_session_name: str, duration_seconds: int = 900) -> dict:
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name,
                                      DurationSeconds=duration_seconds)
    return response


def aws_creds_file(temp_cred_file: str = 'credentials_test') -> None:
    cred_location = '~/.aws/credentials'
    user_home = os.path.expanduser('~')
    file = user_home + '/.aws/' + temp_cred_file
    # prepare the file
    if not os.path.isfile(temp_cred_file):
        logging.info('file does not exist, creating...')
        with open(file, 'w') as f:
            f.write('[default]\n')
            f.write('aws_access_key_id = \n')
            f.write('aws_secret_access_key = \n')
            # leave session token out for now
        logging.info('file created')

    # to get accounts, roles for user - user selects (prompt way) - roleSession based on user/role
    creds = get_sts_creds('arn:aws:iam::xxxxxxxxxxxx:role/Terraform', 'roleSession', 1000)['Credentials']

    # parse the file
    config_parser.read(file)
    if config_parser.has_section('default'):
        with open(file) as f:
            config_parser.read_file(f)
        # Update the in-memory configuration
        config_parser['default']['aws_access_key_id'] += creds['AccessKeyId']
        config_parser['default']['aws_secret_access_key'] += creds['SecretAccessKey']
        config_parser.set('default', 'aws_session_token ', creds['SessionToken'])
        with open(file, 'w+') as f:
            config_parser.write(f)


if __name__ == '__main__':
    aws_creds_file()


