import os
import serviceManagerSetupLogAgentConf
import serviceManagerSetupConstants

def setupAnsibleCollection(rootPath, collections):
    if collections == None:
        print "The collections map is null. Just return"
        return
    
    feature_info_map = collections[serviceManagerSetupConstants.FEATURES_KEY]
    if feature_info_map == None:
        print "The collections need feature map"
        return
    
    flume_info_map = feature_info_map[serviceManagerSetupConstants.FLUME_INFO_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    collection_ansible_map = {}
    collection_package_path = rootPath + collections[serviceManagerSetupConstants.PACKAGE_KEY]
    collection_template_file = rootPath + collections[serviceManagerSetupConstants.TEMPLATE_KEY]
    collection_install_path = collections[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    collection_log_dir = collections[serviceManagerSetupConstants.LOG_PATH_KEY]
    collection_flume_conf_root_path = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TARGET_ROOT_PATH_KEY]
    collection_flume_conf_install_path = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_INSTALL_PATH_KEY]
    collection_flume_conf_file_name = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_FILE_NAME_KEY]
    
    devices = collections[serviceManagerSetupConstants.DEVICE_KEY]
    
    if devices == None:
        print "The collection devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The collection " + deviceKey + " should not be Null"
            continue
        
        collection_ansible_info = {}
        collection_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        collection_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        collection_ansible_info[serviceManagerSetupConstants.START_COMMAND_WORD] = device[serviceManagerSetupConstants.START_COMMAND_KEY]
        collection_ansible_info[serviceManagerSetupConstants.JAR_SRC_WORD] = collection_package_path
        collection_ansible_info[serviceManagerSetupConstants.JAR_INSTALL_WORD] = collection_install_path
        collection_ansible_info[serviceManagerSetupConstants.LOG_DIR_WORD] = collection_log_dir
        collection_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        collection_ansible_info[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD] = collection_flume_conf_root_path + '/' + device[serviceManagerSetupConstants.NAME_KEY] + '/' + collection_flume_conf_file_name
        collection_ansible_info[serviceManagerSetupConstants.FLUME_CONF_DES_WORD] = collection_flume_conf_install_path
        collection_ansible_map[deviceKey] = collection_ansible_info
    
    buildAnsibleCollection(collection_template_file, collection_ansible_map)
    flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY] = collections[serviceManagerSetupConstants.LOG_FILES_KEY]
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
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_SRC_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_INSTALL_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.START_COMMAND_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_SRC_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_DES_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.LOG_DIR_WORD, collectionAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD])
        
        collectionAnsibleFile = collectionAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        collectionAnsibleFileDir = collectionAnsibleFile[:collectionAnsibleFile.rindex("/")]
    
        if not os.path.exists(collectionAnsibleFileDir):
            os.makedirs(collectionAnsibleFileDir)
        
        if os.path.exists(collectionAnsibleFile):
            os.remove(collectionAnsibleFile)
            
        collectionAnsibleFileScript = os.open(collectionAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(collectionAnsibleFileScript, tempTemplate)
        os.close(collectionAnsibleFileScript)
        
def buildFlumeConf(rootPath, flume_info_map, collection_ansible_map):
    
    for collectionAnsibleInfoKey in collection_ansible_map.keys():
        collectionAnsibleInfo = collection_ansible_map[collectionAnsibleInfoKey]
        if collectionAnsibleInfo == None:
            print "collection ansible info " + collectionAnsibleInfo + " should not be Null"
            continue
        
        flume_conf_info = {}
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_PARTITION_ID_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_PARTITION_ID_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'collection'
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_LIST_STRING_KEY] = flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TEMPLATE_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_SRC_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_SRC_TEMPLATE_KEY]
        
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = collectionAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = collectionAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = collectionAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_conf_info)