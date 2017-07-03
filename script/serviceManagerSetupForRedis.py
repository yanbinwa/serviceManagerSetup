import os

DEVICE_KEY = "devices"

REDIS_PACKAGE_KEY = "package"
REDIS_TEMPLATE_KEY = "template"
REDIS_INSTALL_PATH_KEY = "setup_dir"
REDIS_CONF_PATH_KEY = "conf_dir"
REDIS_CONF_FILE_KEY = "conf_file"
REDIS_SERVER_SCRPIT_PATH_KEY = "serverScript"
REDIS_MAKE_DIR_KEY = "make_dir"

REDIS_NAME_KEY = "name"
REDIS_USER_KEY = "user"
REDIS_CONF_SRC_KEY = "conf"
REDIS_ANSIBLE_FILE_PATH = "ansibleFile"

REDIS_HOST_NAME_WORD = "$_hostname_"
REDIS_HOST_USER_WORD = "$_user_"
REDIS_PACKAGE_SRC_WORD = "$_redisPackage_"
REDIS_PACKAGE_INSTALL_WORD = "$_redisPackageInstallPath_"
REDIS_CONFIG_SRC_WORD = "$_redisConfSrc_"
REDIS_CONFIG_TARGET_WORD = "$_redisConfTarget_"
REDIS_CONFIG_TARGET_FILE_WORD = "$_redisConfFile_"
REDIS_SERVER_SCRPIT_WORD = "$_redisServerScript_"
REDIS_MAKE_DIR_WORD = "$_redisMakePath_"

def setupAnsibleRedis(rootPath, rediss):
    if rediss == None:
        print "The rediss map should not be Null"
        return -1
    
    redis_ansible_map = {}
    redis_package_path = rootPath + rediss[REDIS_PACKAGE_KEY]
    redis_template_file = rootPath + rediss[REDIS_TEMPLATE_KEY]
    redis_install_path = rediss[REDIS_INSTALL_PATH_KEY]
    redis_conf_path = rediss[REDIS_CONF_PATH_KEY]
    redis_conf_file = rediss[REDIS_CONF_FILE_KEY]
    redis_serverScript = rediss[REDIS_SERVER_SCRPIT_PATH_KEY]
    redis_make_dir = rediss[REDIS_MAKE_DIR_KEY]
    
    devices = rediss[DEVICE_KEY]
    if devices == None:
        print "The redis devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The redis " + deviceKey + " should not be Null"
            continue
        
        redis_ansible_info = {}
        redis_ansible_info[REDIS_HOST_NAME_WORD] = device[REDIS_NAME_KEY]
        redis_ansible_info[REDIS_HOST_USER_WORD] = device[REDIS_USER_KEY]
        redis_ansible_info[REDIS_PACKAGE_SRC_WORD] = redis_package_path
        redis_ansible_info[REDIS_PACKAGE_INSTALL_WORD] = redis_install_path
        redis_ansible_info[REDIS_CONFIG_SRC_WORD] = rootPath + device[REDIS_CONF_SRC_KEY]
        redis_ansible_info[REDIS_CONFIG_TARGET_WORD] = redis_conf_path
        redis_ansible_info[REDIS_CONFIG_TARGET_FILE_WORD] = redis_conf_file
        redis_ansible_info[REDIS_ANSIBLE_FILE_PATH] = rootPath + device[REDIS_ANSIBLE_FILE_PATH]
        redis_ansible_info[REDIS_SERVER_SCRPIT_WORD] = redis_serverScript
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
        
        tempTemplate = template.replace(REDIS_HOST_NAME_WORD, redisAnsibleInfo[REDIS_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(REDIS_HOST_USER_WORD, redisAnsibleInfo[REDIS_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(REDIS_PACKAGE_SRC_WORD, redisAnsibleInfo[REDIS_PACKAGE_SRC_WORD])
        tempTemplate = tempTemplate.replace(REDIS_PACKAGE_INSTALL_WORD, redisAnsibleInfo[REDIS_PACKAGE_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(REDIS_CONFIG_SRC_WORD, redisAnsibleInfo[REDIS_CONFIG_SRC_WORD])
        tempTemplate = tempTemplate.replace(REDIS_CONFIG_TARGET_WORD, redisAnsibleInfo[REDIS_CONFIG_TARGET_WORD])
        tempTemplate = tempTemplate.replace(REDIS_CONFIG_TARGET_FILE_WORD, redisAnsibleInfo[REDIS_CONFIG_TARGET_FILE_WORD])
        tempTemplate = tempTemplate.replace(REDIS_SERVER_SCRPIT_WORD, redisAnsibleInfo[REDIS_SERVER_SCRPIT_WORD])
        tempTemplate = tempTemplate.replace(REDIS_MAKE_DIR_WORD, redisAnsibleInfo[REDIS_MAKE_DIR_WORD])
        
        redisAnsibleFile = redisAnsibleInfo[REDIS_ANSIBLE_FILE_PATH]
        redisAnsibleFileDir = redisAnsibleFile[:redisAnsibleFile.rindex("/")]
    
        if not os.path.exists(redisAnsibleFileDir):
            os.makedirs(redisAnsibleFileDir)
        
        if os.path.exists(redisAnsibleFile):
            os.remove(redisAnsibleFile)
            
        redisAnsibleFileScript = os.open(redisAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(redisAnsibleFileScript, tempTemplate)
        os.close(redisAnsibleFileScript)