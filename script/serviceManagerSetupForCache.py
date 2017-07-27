import os
import serviceManagerSetupLogAgentConf

DEVICE_KEY = "devices"

CACHE_PACKAGE_KEY = "package"
CACHE_TEMPLATE_KEY = "template"
CACHE_INSTALL_PATH_KEY = "setup_dir"
CACHE_LOG_PATH_KEY = "logFilePath"
CACHE_LOG_FILES_KEY = "logFiles"
CACHE_FLUME_INFO_KEY = "flume"

CACHE_NAME_KEY = "name"
CACHE_USER_KEY = "user"
CACHE_START_COMMAND_KEY = "command"

CACHE_ANSIBLE_FILE_PATH = "ansibleFile" 

CACHE_HOST_NAME_WORD = "$_hostname_"
CACHE_HOST_USER_WORD = "$_user_"
CACHE_JAR_SRC_WORD = "$_cacheJarSrc_"
CACHE_JAR_INSTALL_WORD = "$_cacheJarInstallPath_"
CACHE_LOG_DIR_WORD = "$_cacheLogDir_"
CACHE_START_COMMAND_WORD = "$_cacheStartCommand_"
CACHE_FLUME_CONF_SRC_WORD = "$_cacheFlumeConfSrc_"
CACHE_FLUME_CONF_DES_WORD = "$_flumeConfPath_"

FLUME_CONF_TARGET_ROOT_PATH_KEY = "flumeConfTargetRootPath"
FLUME_CONF_INSTALL_PATH_KEY = "flumeConfInstallPath"
FLUME_CONF_FILE_NAME_KEY = "flumeConfName"
FLUME_CONF_TEMPLATE_KEY = "flumeConfTemplate"
FLUME_CONF_SRC_TEMPLATE_KEY = "flumeConfSrcTemplate"
FLUME_KAFKA_BROKER_LIST_KEY = "kafkaBrokerList"
FLUME_KAFKA_LOGGING_TOPIC_KEY = "kafkaTopic"
FLUME_KAFKA_PARTITION_ID_KEY = "kafkaPartitionId"

def setupAnsibleCache(rootPath, caches):
    if caches == None:
        print "The caches map is null. Just return"
        return
    
    flume_info_map = caches[CACHE_FLUME_INFO_KEY]
    if flume_info_map == None:
        print "The flume info map should not be Null"
        return -1
    
    cache_ansible_map = {}
    cache_package_path = rootPath + caches[CACHE_PACKAGE_KEY]
    cache_template_file = rootPath + caches[CACHE_TEMPLATE_KEY]
    cache_install_path = caches[CACHE_INSTALL_PATH_KEY]
    cache_log_path = caches[CACHE_LOG_PATH_KEY]
    cache_flume_conf_root_path = rootPath + flume_info_map[FLUME_CONF_TARGET_ROOT_PATH_KEY]
    cache_flume_conf_install_path = flume_info_map[FLUME_CONF_INSTALL_PATH_KEY]
    cache_flume_conf_file_name = flume_info_map[FLUME_CONF_FILE_NAME_KEY]
    
    devices = caches[DEVICE_KEY]
    
    if devices == None:
        print "The cache devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The cache " + deviceKey + " should not be Null"
            continue
        
        cache_ansible_info = {}
        cache_ansible_info[CACHE_HOST_NAME_WORD] = device[CACHE_NAME_KEY]
        cache_ansible_info[CACHE_HOST_USER_WORD] = device[CACHE_USER_KEY]
        cache_ansible_info[CACHE_START_COMMAND_WORD] = device[CACHE_START_COMMAND_KEY]
        cache_ansible_info[CACHE_JAR_SRC_WORD] = cache_package_path
        cache_ansible_info[CACHE_JAR_INSTALL_WORD] = cache_install_path
        cache_ansible_info[CACHE_LOG_DIR_WORD] = cache_log_path
        cache_ansible_info[CACHE_ANSIBLE_FILE_PATH] = rootPath + device[CACHE_ANSIBLE_FILE_PATH]
        cache_ansible_info[CACHE_FLUME_CONF_SRC_WORD] = cache_flume_conf_root_path + '/' + device[CACHE_NAME_KEY] + '/' + cache_flume_conf_file_name
        cache_ansible_info[CACHE_FLUME_CONF_DES_WORD] = cache_flume_conf_install_path
        
        cache_ansible_map[deviceKey] = cache_ansible_info
    
    buildAnsibleCache(cache_template_file, cache_ansible_map)
    
    flume_info_map[CACHE_LOG_FILES_KEY] = caches[CACHE_LOG_FILES_KEY]
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
        
        tempTemplate = template.replace(CACHE_HOST_NAME_WORD, cacheAnsibleInfo[CACHE_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(CACHE_HOST_USER_WORD, cacheAnsibleInfo[CACHE_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(CACHE_JAR_SRC_WORD, cacheAnsibleInfo[CACHE_JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(CACHE_JAR_INSTALL_WORD, cacheAnsibleInfo[CACHE_JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(CACHE_START_COMMAND_WORD, cacheAnsibleInfo[CACHE_START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(CACHE_FLUME_CONF_SRC_WORD, cacheAnsibleInfo[CACHE_FLUME_CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(CACHE_FLUME_CONF_DES_WORD, cacheAnsibleInfo[CACHE_FLUME_CONF_DES_WORD])
        tempTemplate = tempTemplate.replace(CACHE_LOG_DIR_WORD, cacheAnsibleInfo[CACHE_LOG_DIR_WORD])
        
        cacheAnsibleFile = cacheAnsibleInfo[CACHE_ANSIBLE_FILE_PATH]
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
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_BROKER_LIST_WORD] = flume_info_map[FLUME_KAFKA_BROKER_LIST_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_LOGGING_TOPIC_WORD] = flume_info_map[FLUME_KAFKA_LOGGING_TOPIC_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.KAFKA_PARTITION_ID_WORD] = flume_info_map[FLUME_KAFKA_PARTITION_ID_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_GROUP_NAME_WORD] = 'cache'
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_LIST_STRING_KEY] = flume_info_map[CACHE_LOG_FILES_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TEMPLATE_KEY] = rootPath + flume_info_map[FLUME_CONF_TEMPLATE_KEY]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_SRC_TEMPLATE_KEY] = rootPath + flume_info_map[FLUME_CONF_SRC_TEMPLATE_KEY]
        
        flume_conf_info[serviceManagerSetupLogAgentConf.SERVICE_NAME_WORD] = cacheAnsibleInfo[CACHE_HOST_NAME_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.LOG_FILE_PATH_WORD] = cacheAnsibleInfo[CACHE_LOG_DIR_WORD]
        flume_conf_info[serviceManagerSetupLogAgentConf.FLUME_CONF_TARGET_PATH_KEY] = cacheAnsibleInfo[CACHE_FLUME_CONF_SRC_WORD]
        
        serviceManagerSetupLogAgentConf.buildFlumeLogAgentConf(flume_conf_info)