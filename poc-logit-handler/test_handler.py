import unittest
import handler
import rpy2
from rpy2 import robjects
from rpy2.robjects import r

class AdmitHandlerTest(unittest.TestCase):
    def test_admit(self):
        aws_key = '5loXZUThBxyTTlCGcuYvibYO73uTYueD'
        corp_id = '564'
        file_name = '33'
        r('library(RJSONIO)')
        r('library(lpSolve)')
        r('library(stringdist)')
        r('library(crowdedDedupeR2)')		
        r.assign('aws_key', aws_key)
        r.assign('corp_id', corp_id)
        r.assign('file_name', file_name)
        r('pred <- dedupe_social_func(aws_key, corp_id, file_name)')
        return robjects.r('pred')[0]

if __name__ == "__main__":
    unittest.main()
