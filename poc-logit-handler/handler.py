import ctypes
import json
import os
import boto3
import logging

# use python logging module to log to CloudWatch
# http://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
logging.getLogger().setLevel(logging.DEBUG)

################### load R
# must load all shared libraries and set the
# R environment variables before you can import rpy2
# load R shared libraries from lib dir

for file in os.listdir('lib'):
    if os.path.isfile(os.path.join('lib', file)):
        ctypes.cdll.LoadLibrary(os.path.join('lib', file))
 
# # set R environment variables
os.environ["R_HOME"] = os.getcwd()
os.environ["R_LIBS"] = os.path.join(os.getcwd(), 'site-library')

import rpy2
from rpy2 import robjects
from rpy2.robjects import r
################## end of loading R

def pred_admit(data):
    r('library(RJSONIO)')
    r('library(lpSolve)')
    r('library(stringdist)')
    r('library(crowdedDedupeR2)')
    r('library(jsonlite)')    
    r.assign('data', data)
    r('pred <- dedupe_social_func(data)')
    return robjects.r('pred')[0]

def lambda_handler(event, context):
    try:
        data = event["data"]
        print data
        can_be_admitted = pred_admit(data)
        res = {
            "httpStatus": 200,
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : True
            },
            "body": {"result": can_be_admitted}
        }
        return res
    except Exception as e:
        logging.error('Payload: {0}'.format(event))
        logging.error('Error: {0}'.format(e.message))
        err = {
            'errorType': type(e).__name__, 
            'httpStatus': 400,
            'request_id': context.aws_request_id,
            'message': e.message.replace('\n', ' ')
            }
        raise Exception(json.dumps(err))
