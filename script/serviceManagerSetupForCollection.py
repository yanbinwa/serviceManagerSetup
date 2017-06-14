import os
import serviceManagerSetupLogAgentConf

DEVICE_KEY = "devices"

COLLECTION_PACKAGE_KEY = "package"
COLLECTION_TEMPLATE_KEY = "template"
COLLECTION_INSTALL_PATH_KEY = "setup_dir"
COLLECTION_LOG_PATH_KEY = "logFilePath"
COLLECTION_FLUME_INFO_KEY = "flume"

COLLECTION_NAME_KEY = "name"
COLLECTION_USER_KEY = "user"
COLLECTION_START_COMMAND_KEY = "command"

COLLECTION_ANSIBLE_FILE_PATH = "ansibleFile" 

COLLECTION_HOST_NAME_WORD = "$_hostname_"
COLLECTION_HOST_USER_WORD = "$_user_"
COLLECTION_JAR_SRC_WORD = "$_collectionJarSrc_"
COLLECTION_JAR_INSTALL_WORD = "$_collectionJarInstallPath_"
COLLECTION_LOG_DIR_WORD = "$_collectionLogDir_"
COLLECTION_START_COMMAND_WORD = "$_collectionStartCommand_"
COLLECTION_FLUME_CONF_SRC_WORD = "$_collectionFlumeConfSrc_"
COLLECTION_FLUME_CONF_DES_WORD = "$_flumeConfPath_"

FLUME_CONF_TARGET_ROOT_PATH_KEY = "flumeConfTargetRootPath"
FLUME_CONF_INSTALL_PATH_KEY = "flumeConfInstallPath"
FLUME_CONF_FILE_NAME_KEY = "flumeConfName"
FLUME_CONF_TEMPLATE_KEY = "flumeConfTemplate"
FLUME_KAFKA_BROKER_LIST_KEY = "kafkaBrokerList"
FLUME_KAFKA_LOGGING_TOPIC_KEY = "kafkaTopic"

def setupAnsibleCollection(rootPath, collections):
    if collections == None:
        print "The collections map should not be Null"
        return -1
    
    flume_info_map = collections[COLLECTION_FLUME_INFO_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    collection_ansible_map = {}
    collection_package_path = rootPath + collections[COLLECTION_PACKAGE_KEY]
    collection_template_file = rootPath + collections[COLLECTION_TEMPLATE_KEY]
    collection_install_path = collections[COLLECTION_INSTALL_PATH_KEY]
    collection_log_dir = collections[COLLECTION_LOG_PATH_KEY]
    collection_flume_conf_root_path = rootPath + flume_info_map[FLUME_CONF_TARGET_ROOT_PATH_KEY]
    collection_flume_conf_install_path = flume_info_map[FLUME_CONF_INSTALL_PATH_KEY]
    collection_flume_conf_file_name = flume_info_map[FLUME_CONF_FILE_NAME_KEY]
    
    devices = collections[DEVICE_KEY]
    
    if devices == None:
        print "The collection devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The collection " + deviceKey + " should not be Null"
            continue
        
        collection_ansible_info = {}
        collection_ansible_info[COLLECTION_HOST_NAME_WORD] = device[COLLECTION_NAME_KEY]
        collection_ansible_info[COLLECTION_HOST_USER_WORD] = device[COLLECTION_USER_KEY]
        collection_ansible_info[COLLECTION_START_COMMAND_WORD] = device[COLLECTION_START_COMMAND_KEY]
        collection_ansible_info[COLLECTION_JAR_SRC_WORD] = collection_package_path
        collection_ansible_info[COLLECTION_JAR_INSTALL_WORD] = collection_install_path
        collection_ansible_info[COLLECTION_LOG_DIR_WORD] = collection_log_dir
        collection_ansible_info[COLLECTION_ANSIBLE_FILE_PATH] = rootPath + device[COLLECTION_ANSIBLE_FILE_PATH]
        collection_ansible_info[COLLECTION_FLUME_CONF_SRC_WORD] = collection_flume_conf_root_path + '/' + device[COLLECTION_NAME_KEY] + '/' + collection_flume_conf_file_name
        collection_ansible_info[COLLECTION_FLUME_CONF_DES_WORD] = collection_flume_conf_install_path
        collection_ansible_map[deviceKey] = collection_ansible_info
    
    buildAnsibleCollection(collection_template_file, collection_ansible_map)
    buildFlumeConf(rootPath, flume_info_map, collection_ansible_map)
        
def buildAnsibleCollection(collection_template_file, collection_ansible_map):
    if not os.path.exists(collection_template_file):
        print "collection template file " + collection_template_file + " is not existed"
        return -1
    
    template = open(collection_template_file).read()
    for collectionAnsibleInfoKey in collection_ansible_map.keys():
        collectionAnsibleInfo = collection_ansible_map[collectionAnsibleInfoKey]
        if collectionAnsibleInfo == None:
            print "collection ansible info " + collectionAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(COLLECTION_HOST_NAME_WORD, collectionAnsibleInfo[COLLECTION_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(COLLECTION_HOST_USER_WORD, collectionAnsibleInfo[COLLECTION_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(COLLECTION_JAR_SRC_WORD, collectionAnsibleInfo[COLLECTION_JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(COLLECTION_JAR_INSTALL_WORD, collectionAnsibleInfo[COLLECTION_JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(COLLECTION_START_COMMAND_WORD, collectionAnsibleInfo[COLLECTION_START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(COLLECTION_FLUME_CONF_SRC_WORD, collectionAnsibleInfo[COLLECTION_FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(COLLECTION_FLUME_CONF_DES_WORD, collectionAnsibleInfo[COLLECTION_FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(COLLECTION_LOG_DIR_WORD, collectionAnsibleInfo[COLLECTION_LOG_DIR_WORD])
        
        collectionAnsibleFile = collectionAnsibleInfo[COLLECTION_ANSIBLE_FILE_PATH]
        if os.path.exists(collectionAnsibleFile):
            os.remove(collectionAnsibleFile)
            
        collectionAnsibleFileScript = os.open(collectionAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(collectionAnsibleFileScript, tempTemplate)
        os.close(collectionAnsibleFileScript)
        
def buildFlumeConf(rootPath, flume_info_map, collection_ansible_map):
    flume_Conf_Template_file = rootPath + flume_info_map[FLUME_CONF_TEMPLATE_KEY]
    
    for collectionAnsibleInfoKey in collection_ansible_map.keys():
        collectionAnsibleInfo = collection_ansible_map[collectionAnsibleInfoKey]
        if collectionAnsibleInfo == None:
            print "collection ansible info " + collectionAnsibleInfo + " should not be Null"
            continue
        
        flume_conf_info = {}
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'cache'
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = collectionAnsibleInfo[COLLECTION_HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = collectionAnsibleInfo[COLLECTION_FLUME_CONF_SRC_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = collectionAnsibleInfo[COLLECTION_LOG_DIR_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_Conf_Template_file, flume_conf_info)