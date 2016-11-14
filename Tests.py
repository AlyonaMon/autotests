# coding=utf-8
import json
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', filename="msg.log",
                    format='%(asctime)s  %(name)-20s %(levelname)-8s %(message)s', filemode='w')
from xml.etree import ElementTree
import xml.etree.ElementTree as etree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
import csv
global response, test_dic_for_case, name_testsuite, name_testcase
def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# def XML_FILE(name_testsuite, name_testcase, m):
#     # print name_testcase, name_testsuite
#     top = Element('testsuites', name=str(name_testsuite))
#     parent = SubElement(top, 'testsuite', name=str(name_testcase))
#     # children = [Element('testsuite', name=str(Tests(response)))]
#
#     top.extend(parent)
#     return prettify(top)

def STATUS_CODE(response):
    # print response.status_code

    if response.status_code == 200 or response.status_code == 201:
        text = "Response code is 200 or 201"
        result = True
    else:
        text = "Response code is " + str(response.status_code)
        result = False
    text = text + ": " + str(result)
    # print result
    return text

def STATUS_CODE_NAME(response):
    if response.reason == 'OK':
        text = "Status code name has string '" + str(response.reason) + "'"
        result = True
    else:
        text = "Status code name '" + str(response.reason) + "'"
        result = False
    text = text + ": " + str(result)
    return text

def RESPONSE_TIME(response):
    # if response.elapsed >
    time = response.elapsed.total_seconds()
    if time < 0.5:
        text = "Response time is less than 0.5ms"
        result = time
    else:
        text = "Response time is more than 0.5ms"
        result = "False, time is " + str(time)
    text = text + ": " + str(result) + "ms"
    return text

def CONTENT_TYPE_IS_PRESENT(response):
    if response.content != "":
        text = "Content type is present"
        result = True
    else:
        text = "Content type is not present"
        result = False
    text = text + ": " + str(result)
    return text

def RESPONSE_HAS_ACCKEY(r):
    text = "Access Key present in response "
    if "access_key" in r:
        result = r["access_key"]
        logger.info('Authentication is successful')
        logger.info('Access Key present in response: %s', str(result))
        text = text + ": " + str(True)
    elif "Message" in r:
        logger.setLevel(logging.ERROR)
        logger.error('Access Key absent in response: %s', str(r))
        text = text + ": " + str(False)
    else:
        logger.setLevel(logging.ERROR)
        logger.error('Fails for an paar App key - Access Key')
        text = text + ": " + str(False)
    # print text
    return text


#
# def _is_empty(text):
#     return not text or text.isspace()

"""def indent(elem, level=0, tab='  '):
    i = '\n' + level * tab
    j = i + tab  # j = i_n+1
    indent_parent = False

    if len(elem):
        if _is_empty(elem.text):
            # Indent before element.
            elem.text = j
        if _is_empty(elem.tail):
            # Indent after element.
            elem.tail = i

        prev = None
        for child in elem:
            indent_block = indent(child, level + 1, tab)
            if indent_block or len(child) > 1:
                # This child or some lower child block should be super-indented.
                if len(elem) == 1:
                    # Pass indentation up because this level only has one child.
                    indent_parent = True
                else:
                    # Surround this block with newlines for emphasis.
                    if prev is not None and _is_empty(prev.tail):
                        prev.tail = '\n' + j
                    if _is_empty(child.tail):
                        child.tail = '\n' + j
            prev = child
        if _is_empty(child.tail):
            # Last child element determines closing tag tab level.
            child.tail = i
    else:
        if level and _is_empty(elem.tail):
            elem.tail = i

    return indent_parent"""

def Tests(response, test_dic_for_case, name_testcase, top):

    parent = SubElement(top, 'testsuite', name=str(name_testcase))
    if "STATUS_CODE" in test_dic_for_case:
        m = STATUS_CODE(response)
        children = SubElement(parent, 'testcase', name=str(m))
        if "False" in m:
            children_1 = SubElement(children, 'failure', type="AssertionFailure")
            children_2 = SubElement(children_1, 'failed')
            children_2.text = "![CDATA[Failed]]"
            children_1.extend(children_2)
        else:
            parent.extend(children)

    if "STATUS_CODE_NAME" in test_dic_for_case:
        m = STATUS_CODE_NAME(response)
        children = SubElement(parent, 'testcase', name=str(m))
        if "False" in m:
            children_1 = SubElement(children, 'failure', type="AssertionFailure")
            children_2 = SubElement(children_1, 'failed')
            children_2.text = "![CDATA[Failed]]"
            children_1.extend(children_2)
        else:
            parent.extend(children)

    if "RESPONSE_TIME" in test_dic_for_case:
        m = RESPONSE_TIME(response)
        children = SubElement(parent, 'testcase', name=str(m))
        if 'False' in m:
            children_1 = SubElement(children, 'failure', type="AssertionFailure")
            children_2 = SubElement(children_1, 'failed')
            children_2.text = "![CDATA[Failed]]"
            children_1.extend(children_2)
        else:
            parent.extend(children)

    if "CONTENT_TYPE_IS_PRESENT" in test_dic_for_case:
        m = CONTENT_TYPE_IS_PRESENT(response)
        children = SubElement(parent, 'testcase', name=str(m))
        if 'False' in m:
            children_1 = SubElement(children, 'failure', type="AssertionFailure")
            children_2 = SubElement(children_1, 'failed')
            children_2.text = "![CDATA[Failed]]"
            children_1.extend(children_2)
        else:
            parent.extend(children)

    if "RESPONSE_HAS_ACCKEY" in test_dic_for_case:
        dict_response = response.__dict__["_content"]
        r = json.loads(dict_response)
        m = RESPONSE_HAS_ACCKEY(r)
        # print m
        children = SubElement(parent, 'testcase', name=str(m))
        if 'False' in m:
            children_1 = SubElement(children, 'failure', type="AssertionFailure")
            children_2 = SubElement(children_1, 'failed')
            children_2.text = "![CDATA[Failed]]"
            children_1.extend(children_2)
        else:
            parent.extend(children)








