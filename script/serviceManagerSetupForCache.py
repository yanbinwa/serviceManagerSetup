import os
import serviceManagerSetupLogAgentConf
import serviceManagerSetupConstants

def setupAnsibleCache(rootPath, caches):
    if caches == None:
        print "The caches map is null. Just return"
        return
    
    feature_info_map = caches[serviceManagerSetupConstants.FEATURES_KEY]
    if feature_info_map == None:
        print "The caches need feature map"
        return
    
    flume_info_map = feature_info_map[serviceManagerSetupConstants.FLUME_INFO_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    cache_ansible_map = {}
    cache_package_path = rootPath + caches[serviceManagerSetupConstants.PACKAGE_KEY]
    cache_template_file = rootPath + caches[serviceManagerSetupConstants.TEMPLATE_KEY]
    cache_install_path = caches[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    cache_log_path = caches[serviceManagerSetupConstants.LOG_PATH_KEY]
    cache_flume_conf_root_path = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TARGET_ROOT_PATH_KEY]
    cache_flume_conf_install_path = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_INSTALL_PATH_KEY]
    cache_flume_conf_file_name = flume_info_map[serviceManagerSetupConstants.FLUME_CONF_FILE_NAME_KEY]
    
    devices = caches[serviceManagerSetupConstants.DEVICE_KEY]
    
    if devices == None:
        print "The cache devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The cache " + deviceKey + " should not be Null"
            continue
        
        cache_ansible_info = {}
        cache_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        cache_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        cache_ansible_info[serviceManagerSetupConstants.START_COMMAND_WORD] = device[serviceManagerSetupConstants.START_COMMAND_KEY]
        cache_ansible_info[serviceManagerSetupConstants.JAR_SRC_WORD] = cache_package_path
        cache_ansible_info[serviceManagerSetupConstants.JAR_INSTALL_WORD] = cache_install_path
        cache_ansible_info[serviceManagerSetupConstants.LOG_DIR_WORD] = cache_log_path
        cache_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        cache_ansible_info[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD] = cache_flume_conf_root_path + '/' + device[serviceManagerSetupConstants.NAME_KEY] + '/' + cache_flume_conf_file_name
        cache_ansible_info[serviceManagerSetupConstants.FLUME_CONF_DES_WORD] = cache_flume_conf_install_path
        
        cache_ansible_map[deviceKey] = cache_ansible_info
    
    buildAnsibleCache(cache_template_file, cache_ansible_map)
    
    flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY] = caches[serviceManagerSetupConstants.LOG_FILES_KEY]
    buildFlumeConf(rootPath, flume_info_map, cache_ansible_map)
        
def buildAnsibleCache(cache_template_file, cache_ansible_map):
    if not os.path.exists(cache_template_file):
        print "cache template file " + cache_template_file + " is not existed"
        return -1
    
    template = open(cache_template_file).read()
    for cacheAnsibleInfoKey in cache_ansible_map.keys():
        cacheAnsibleInfo = cache_ansible_map[cacheAnsibleInfoKey]
        if cacheAnsibleInfo == None:
            print "cache ansible info " + cacheAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_SRC_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_INSTALL_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.START_COMMAND_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_SRC_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.FLUME_CONF_DES_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.LOG_DIR_WORD, cacheAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD])
        
        cacheAnsibleFile = cacheAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        cacheAnsibleFileDir = cacheAnsibleFile[:cacheAnsibleFile.rindex("/")]
    
        if not os.path.exists(cacheAnsibleFileDir):
            os.makedirs(cacheAnsibleFileDir)
        
        if os.path.exists(cacheAnsibleFile):
            os.remove(cacheAnsibleFile)
            
        cacheAnsibleFileScript = os.open(cacheAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(cacheAnsibleFileScript, tempTemplate)
        os.close(cacheAnsibleFileScript)

def buildFlumeConf(rootPath, flume_info_map, cache_ansible_map):
    
    for cacheAnsibleInfoKey in cache_ansible_map.keys():
        cacheAnsibleInfo = cache_ansible_map[cacheAnsibleInfoKey]
        if cacheAnsibleInfo == None:
            print "cache ansible info " + cacheAnsibleInfo + " should not be Null"
            continue
        
        flume_conf_info = {}
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_PARTITION_ID_WORD] = flume_info_map[serviceManagerSetupConstants.FLUME_KAFKA_PARTITION_ID_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'cache'
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_LIST_STRING_KEY] = flume_info_map[serviceManagerSetupConstants.LOG_FILES_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_TEMPLATE_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_SRC_TEMPLATE_KEY] = rootPath + flume_info_map[serviceManagerSetupConstants.FLUME_CONF_SRC_TEMPLATE_KEY]
        
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = cacheAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = cacheAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = cacheAnsibleInfo[serviceManagerSetupConstants.FLUME_CONF_SRC_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_conf_info)