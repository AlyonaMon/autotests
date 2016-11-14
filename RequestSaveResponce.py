# coding=utf-8
import requests
import json
import Tests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', filename="msg.log",
                    format='%(asctime)s  %(name)-20s %(levelname)-8s %(message)s', filemode='w')


def Get_Product(url, test_dic_for_case, name_testcase, top):
    response = requests.request("GET", url, data="")
    Tests.Tests(response, test_dic_for_case, name_testcase, top)
    return response


def Auth_for_supereditor(application_key, url, test_dic_for_case, name_testcase, top):
    # print "-------------------"
    logger.setLevel(logging.INFO)
    response = requests.request("POST", url, data=application_key)
    dict_response = response.__dict__["_content"]
    r = json.loads(dict_response)
    if "access_key" in r:
        result = r["access_key"]
        Tests.Tests(response, test_dic_for_case, name_testcase, top)
        logger.info('Authentication is successful')
        logger.info('Access Key present in response: %s', str(result))
    elif "Message" in r:
        logger.setLevel(logging.ERROR)
        logger.error('Access Key absent in response: %s', str(r))
        result = False
    else:
        logger.setLevel(logging.ERROR)
        logger.error('Fails for an paar App key - Access Key')
        result = False
    # result = access_key or False
    return result
