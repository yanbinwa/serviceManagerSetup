import os
import serviceManagerSetupConstants

REDIS_MAKE_DIR_KEY = "make_dir"

REDIS_MAKE_DIR_WORD = "$_makePath_"

def setupAnsibleRedis(rootPath, rediss):
    if rediss == None:
        print "The rediss map is Null. Just return"
        return
    
    redis_ansible_map = {}
    redis_package_path = rootPath + rediss[serviceManagerSetupConstants.PACKAGE_KEY]
    redis_template_file = rootPath + rediss[serviceManagerSetupConstants.TEMPLATE_KEY]
    redis_install_path = rediss[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    redis_conf_path = rediss[serviceManagerSetupConstants.CONF_PATH_KEY]
    redis_serverScript = rediss[serviceManagerSetupConstants.SERVER_SCRPIT_PATH_KEY]
    redis_make_dir = rediss[REDIS_MAKE_DIR_KEY]
    
    devices = rediss[serviceManagerSetupConstants.DEVICE_KEY]
    if devices == None:
        print "The redis devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The redis " + deviceKey + " should not be Null"
            continue
        
        redis_ansible_info = {}
        redis_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        redis_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        redis_ansible_info[serviceManagerSetupConstants.PACKAGE_SRC_WORD] = redis_package_path
        redis_ansible_info[serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD] = redis_install_path
        redis_ansible_info[serviceManagerSetupConstants.CONF_SRC_WORD] = rootPath + device[serviceManagerSetupConstants.CONF_SRC_KEY]
        redis_ansible_info[serviceManagerSetupConstants.CONF_TARGET_WORD] = redis_conf_path
        redis_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        redis_ansible_info[serviceManagerSetupConstants.SERVER_SCRIPT_WORD] = redis_serverScript
        redis_ansible_info[REDIS_MAKE_DIR_WORD] = redis_make_dir
        redis_ansible_map[deviceKey] = redis_ansible_info
        
    buildAnsibleRedis(redis_template_file, redis_ansible_map)

def buildAnsibleRedis(redis_template_file, redis_ansible_map):
    if not os.path.exists(redis_template_file):
        print "redis template file " + redis_template_file + " is not existed"
        return -1
    
    template = open(redis_template_file).read()
    
    for redisAnsibleInfoKey in redis_ansible_map.keys():
        redisAnsibleInfo = redis_ansible_map[redisAnsibleInfoKey]
        if redisAnsibleInfo == None:
            print "redis ansible info " + redisAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, redisAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, redisAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.PACKAGE_SRC_WORD, redisAnsibleInfo[serviceManagerSetupConstants.PACKAGE_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD, redisAnsibleInfo[serviceManagerSetupConstants.PACKAGE_INSTALL_PATH_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.CONF_SRC_WORD, redisAnsibleInfo[serviceManagerSetupConstants.CONF_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.CONF_TARGET_WORD, redisAnsibleInfo[serviceManagerSetupConstants.CONF_TARGET_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.SERVER_SCRIPT_WORD, redisAnsibleInfo[serviceManagerSetupConstants.SERVER_SCRIPT_WORD])
        tempTemplate = tempTemplate.replace(REDIS_MAKE_DIR_WORD, redisAnsibleInfo[REDIS_MAKE_DIR_WORD])
        
        redisAnsibleFile = redisAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        redisAnsibleFileDir = redisAnsibleFile[:redisAnsibleFile.rindex("/")]
    
        if not os.path.exists(redisAnsibleFileDir):
            os.makedirs(redisAnsibleFileDir)
        
        if os.path.exists(redisAnsibleFile):
            os.remove(redisAnsibleFile)
            
        redisAnsibleFileScript = os.open(redisAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(redisAnsibleFileScript, tempTemplate)
        os.close(redisAnsibleFileScript)