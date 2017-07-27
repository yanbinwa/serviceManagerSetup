import os
import serviceManagerSetupLogAggConf

DEVICE_KEY = "devices"

LOGGING_TEMPLATE_KEY = "template"
LOGGING_FLUME_INFO_KEY = "flume"

FLUME_CONF_TARGET_ROOT_PATH_KEY = "flumeConfTargetRootPath"
FLUME_CONF_INSTALL_PATH_KEY = "flumeConfInstallPath"
FLUME_CONF_TEMPLATE_KEY = "flumeConfTemplate"
FLUME_CONF_FILE_NAME_KEY = "flumeConfName"
FLUME_KAFKA_BROKER_LIST_KEY = "kafkaBrokerList"
FLUME_KAFKA_LOGGING_TOPIC_KEY = "kafkaTopic"
FLUME_ROOT_PATH_KEY = "logFileRootPath"

LOGGING_NAME_KEY = "name"
LOGGING_USER_KEY = "user"

LOGGING_HOST_NAME_WORD = "$_hostname_"
LOGGING_HOST_USER_WORD = "$_user_"
LOGGING_ROOT_PATH_WORD = "$_loggingRootPath_"
LOGGING_FLUME_CONF_SRC_WORD = "$_loggingFlumeConfSrc_"
LOGGING_FLUME_CONF_DES_WORD = "$_flumeConfPath_"

LOGGING_ANSIBLE_FILE_PATH = "ansibleFile"

def setupAnsibleLogging(rootPath, loggings):
    if loggings == None:
        print "The logging map is null. Just return"
        return
    
    flume_info_map = loggings[LOGGING_FLUME_INFO_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    logging_ansible_map = {}
    logging_template_file = rootPath + loggings[LOGGING_TEMPLATE_KEY]
    logging_root_path = rootPath + flume_info_map[FLUME_ROOT_PATH_KEY];
    logging_flume_conf_root_path = rootPath + flume_info_map[FLUME_CONF_TARGET_ROOT_PATH_KEY]
    logging_flume_conf_install_path = flume_info_map[FLUME_CONF_INSTALL_PATH_KEY]
    logging_flume_conf_file_name = flume_info_map[FLUME_CONF_FILE_NAME_KEY]
    
    devices = loggings[DEVICE_KEY]
    if devices == None:
        print "The loggings devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The logging " + deviceKey + " should not be Null"
            continue
        
        logging_ansible_info = {}
        logging_ansible_info[LOGGING_HOST_NAME_WORD] = device[LOGGING_NAME_KEY]
        logging_ansible_info[LOGGING_HOST_USER_WORD] = device[LOGGING_USER_KEY]
        logging_ansible_info[LOGGING_ROOT_PATH_WORD] = logging_root_path
        logging_ansible_info[LOGGING_FLUME_CONF_SRC_WORD] = logging_flume_conf_root_path + '/' + device[LOGGING_NAME_KEY] + '/' + logging_flume_conf_file_name
        logging_ansible_info[LOGGING_FLUME_CONF_DES_WORD] = logging_flume_conf_install_path
        logging_ansible_info[LOGGING_ANSIBLE_FILE_PATH] = rootPath + device[LOGGING_ANSIBLE_FILE_PATH]
        logging_ansible_map[deviceKey] = logging_ansible_info
        
    buildAnsibleLogging(logging_template_file, logging_ansible_map)
    buildFlumeConf(rootPath, flume_info_map, logging_ansible_map)
    
def buildAnsibleLogging(logging_template_file, logging_ansible_map):
    if not os.path.exists(logging_template_file):
        print "logging template file " + logging_template_file + " is not existed"
        return -1
    
    template = open(logging_template_file).read()
    for loggingAnsibleInfoKey in logging_ansible_map.keys():
        loggingAnsibleInfo = logging_ansible_map[loggingAnsibleInfoKey]
        if loggingAnsibleInfo == None:
            print "logging ansible info " + loggingAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(LOGGING_HOST_NAME_WORD, loggingAnsibleInfo[LOGGING_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(LOGGING_HOST_USER_WORD, loggingAnsibleInfo[LOGGING_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(LOGGING_ROOT_PATH_WORD, loggingAnsibleInfo[LOGGING_ROOT_PATH_WORD])
        tempTemplate = tempTemplate.replace(LOGGING_FLUME_CONF_SRC_WORD, loggingAnsibleInfo[LOGGING_FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(LOGGING_FLUME_CONF_DES_WORD, loggingAnsibleInfo[LOGGING_FLUME_CONF_DES_WORD])
        
        loggingAnsibleFile = loggingAnsibleInfo[LOGGING_ANSIBLE_FILE_PATH]
        loggingAnsibleFileDir = loggingAnsibleFile[:loggingAnsibleFile.rindex("/")]
    
        if not os.path.exists(loggingAnsibleFileDir):
            os.makedirs(loggingAnsibleFileDir)
        
        if os.path.exists(loggingAnsibleFile):
            os.remove(loggingAnsibleFile)
            
        loggingAnsibleFileScript = os.open(loggingAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(loggingAnsibleFileScript, tempTemplate)
        os.close(loggingAnsibleFileScript)
        
def buildFlumeConf(rootPath, flume_info_map, logging_ansible_map):
    
    flume_Conf_Template_file = rootPath + flume_info_map[FLUME_CONF_TEMPLATE_KEY]
        
    for loggingAnsibleInfoKey in logging_ansible_map.keys():
        loggingAnsibleInfo = logging_ansible_map[loggingAnsibleInfoKey]
        if loggingAnsibleInfo == None:
            print "logging ansible info " + loggingAnsibleInfoKey + " should not be Null"
            continue
                
        flume_conf_info = {}
        flume_conf_info[serviceManagerSetupLogAggConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAggConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAggConf.FLUME_CONF_TARGET_PATH_KEY] = loggingAnsibleInfo[LOGGING_FLUME_CONF_SRC_WORD]
        flume_conf_info[serviceManagerSetupLogAggConf.LOG_FILE_ROOT_PATH_WORD] = flume_info_map[FLUME_ROOT_PATH_KEY]
        
        serviceManagerSetupLogAggConf.buildFlumeLogAggConf(flume_Conf_Template_file, flume_conf_info)
        