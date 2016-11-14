# coding=utf-8
import Tests
import json
import os, fnmatch
import RequestSaveResponce
from xml.etree.ElementTree import Element, SubElement, Comment

s = "\""
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', filename="msg.log",
                    format='%(asctime)s  %(name)-20s %(levelname)-8s %(message)s', filemode='w')


directory = 'D:\Practice\LanguageTest\json_files'
mask = '*.json'

def postman_globals(file):
    try:
        post_man_globals = open(file).read()
        parsed_string_globals = json.loads(post_man_globals)
        dict_globals = dict()
        i = 0
        #проверить переменную l
        for l in parsed_string_globals:
            u = {parsed_string_globals[i]['key']: parsed_string_globals[i]['value']}
            dict_globals.update(u)
            i += 1
    except (IOError, OSError) as e:
        dict_globals = -1
        logger.setLevel(logging.ERROR)
        logger.info('Fails for an I/O-related reason, e.g., “file not found” or “disk full”.')
        # sys.exit("Fails for an I/O")
    return dict_globals

def rest_language(file):
    try:
        p_e_rest_language = open(file).read()
        parsed_rest_language = json.loads(p_e_rest_language)
        dict_language = dict()
        r = parsed_rest_language["values"]
        i = 0
        for l in r:
            u = {r[i]['key']: r[i]['value']}
            dict_language.update(u)
            i += 1
        # '''
        # корректировка url, замена access_key и url на значения из глобальных переменных
        # '''
        #
        # PG = postman_globals()
        # path_to_restful = PG["path_to_restful"]
        # try:
        #     full_url = urlparse(str(dict_language["url"]))
        #     acc_key = PG["access_key"]
        #     query = full_url.query
        #     pattern = '(?:=)'
        #     split1 = re.split(pattern, query, 1)
        #     pattern = '(?:&)'
        #     split2 = re.split(pattern, split1[1], 1)
        #     url = str(dict_language["url"])
        #     url = url.replace(str(split2[0]), str(acc_key))
        #     new_url = url.replace(full_url.scheme+"://"+full_url.netloc, path_to_restful)
        # except KeyError:
        #     new_url = str(dict_language["url"])
    except (IOError, OSError) as e:
        dict_language = -1
        logger.setLevel(logging.ERROR)
        logger.info('Fails for an I/O-related reason, e.g., “file not found” or “disk full”.')
        # sys.exit("Fails for an I/O")
    return dict_language

#Функция получения имен
# def name_suite_and_case(file):
#     collection = open(file).read()
#     parsed_string_collection = json.loads(collection)
#     parsed_item = parsed_string_collection["info"]["name"]
#     for i in parsed_item:
#         parsed_item_test_suite = i["item"]
#         name_testcase = parsed_item_test_suite[0]["name"]
#         # print
#     return type(name_testcase)

def msg_in_log(level, msg):
    if level == 'INFO':
        logger.setLevel(logging.INFO)
        logger.info(msg)
    elif level == 'ERROR':
        logger.setLevel(logging.ERROR)
        logger.error(msg)
    elif level == "WARN":
        logger.setLevel(logging.WARN)
        logger.warn(msg)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)
        logger.warning(msg)
    elif level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
        logger.debug(msg)

def STR_DIC(str_test):
    test_dic_for_case = ""
    if "responseTime" in str_test:
        test_dic_for_case = test_dic_for_case + "RESPONSE_TIME, "
    if "responseCode.code" in str_test:
        test_dic_for_case = test_dic_for_case + "STATUS_CODE, "
    if "responseCode.name.has" in str_test:
        test_dic_for_case = test_dic_for_case + "STATUS_CODE_NAME, "
    if "responseBody.has" in str_test:
        test_dic_for_case = test_dic_for_case + "RESPONSE_HAS_ACCKEY, "
    if "responseHeaders.hasOwnProperty" in str_test:
        test_dic_for_case = test_dic_for_case + "CONTENT_TYPE_IS_PRESENT, "
    # print test_dic_for_case
    return test_dic_for_case

# обработка внутренних запросов
def test_siute_rest_language_api(file):
    global name_temp
    try:
        collection = open(file).read()
        parsed_string_collection = json.loads(collection)
        parsed_item = parsed_string_collection["item"]
        name_testsuites = parsed_string_collection["info"]["name"]
        top = Element('testsuites', name=str(name_testsuites))
        for i in parsed_item:
            parsed_item_test_suite = i["item"]

            for j in parsed_item_test_suite:
                for key in j["event"]:
                    if key["listen"] == "test":
                        str_test = str(key["script"]["exec"])
                        # print str_test
                    elif key["listen"] == "prerequest":
                        # if use prerequest..
                        prerequest = "prerequest"
                if j["request"]["method"] == "POST":
                    name_testcase = j["name"]
                    # print name_testcase
                    if j["request"]["body"]["raw"].find("application_key") != -1:
                        application_key = j["request"]["body"]["raw"]
                        url = j["request"]["url"]
                        for file in os.listdir(directory):
                            if fnmatch.fnmatch(file, mask):
                                if "globals" in str(file):
                                    path_to_restful = postman_globals("json_files/" + str(file))
                                    url = url.replace("{{path_to_restful}}", path_to_restful["path_to_restful"])
                                    test_dic_for_case = STR_DIC(str_test)
                                    access_key = RequestSaveResponce.Auth_for_supereditor(application_key,
                                                                        url, test_dic_for_case, name_testcase, top)
                                    # print "POST DONE"
                                    if access_key == False:
                                        msg = "In " + name_testcase + " Access Key absent in response. Perhaps Application key incorrect"
                                        msg_in_log('ERROR', msg)
                                        # raise KeyError
                                        # continue
                    else:
                        msg = "In " + name_testcase + " Application key not found"
                        msg_in_log('ERROR', msg)
                        break
                # Если GET
                elif j["request"]["method"] == "GET":
                    name_testcase = j["name"]
                    # print name_testcase
                    if access_key != "" and access_key != False:
                        url = j["request"]["url"]
                        for file in os.listdir(directory):
                            if fnmatch.fnmatch(file, mask):
                                if "globals" in str(file):
                                    path_to_restful = postman_globals("json_files/" + str(file))
                                    url = url.replace("{{path_to_restful}}",
                                                      path_to_restful["path_to_restful"])
                                    for file in os.listdir(directory):
                                        if fnmatch.fnmatch(file, mask):
                                            if "environment" in str(file):
                                                dict_lang = rest_language("json_files/" + str(file))
                                                url = url.replace("{{rest_v2_language}}",
                                                                  dict_lang["rest_v2_language"])
                                                url = url.replace("{{access_key}}", access_key)
                                                test_dic_for_case = STR_DIC(str_test)
                                                response = RequestSaveResponce.Get_Product(url, test_dic_for_case, name_testcase, top)
                                                # print "GET DONE"
            # print Tests.XML_FILE(name_temp,response)
        msg = "All files read"
        msg_in_log('INFO', msg)
        f = open('tests.xml', 'w')
        f.write(Tests.prettify(top))
        f.close()
        # print Tests.prettify(top)
    except (IOError, KeyError) as e:
        msg = "Fails for an I/O-related or 'App key not found' or 'file not found' or 'Acc key absent'."
        msg_in_log('ERROR', msg)
        return 0

#чтение json коллекции в директории
def read_files_in_dir():
    if len(os.listdir(directory)) != 0:# print "The directory is not empty!"
        logger.setLevel(logging.INFO)
        logger.info("The directory is not empty! Starting read files in dir..")
        for file in os.listdir(directory):
            if fnmatch.fnmatch(file, mask):
                if "collection" in str(file):
                    logger.setLevel(logging.INFO)
                    logger.info("File 'collection' has on dir!")
                    test_siute_rest_language_api("json_files/" + str(file))
                if "globals" in str(file):
                    logger.setLevel(logging.INFO)
                    logger.info("File 'globals' has on dir!")
                if "environment" in str(file):
                    logger.setLevel(logging.INFO)
                    logger.info("File 'environment' has on dir!")
    else:
        logger.setLevel(logging.WARN)
        logger.warn("There is a problem reading files on directory! The directory is empty!")

    return 0


read_files_in_dir()