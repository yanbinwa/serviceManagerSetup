import os

FLUME_NAME_KEY = "name"
FLUME_USER_KEY = "user"

FLUME_INSTALL_KEY = "preStep"
FLUME_START_KEY = "postStep"
FLUME_ANSIBLE_FILE_KEY = "ansibleFile"

FLUME_HOST_NAME_WORD = "$_hostname_"
FLUME_HOST_USER_WORD = "$_user_"

FLUME_INSTALL_PACKAGE_KEY = "package"
FLUME_INSTALL_INSTALL_PATH_KEY = "setup_dir"
FLUME_INSTALL_TEMPLATE_KEY = "template"
FLUME_INSTALL_ANSIBLE_FILE_KEY = "ansibleFile"

FLUME_INSTALL_PACKAGE_WORD = "$_flumePackage_"
FLUME_INSTALL_INSTALL_PATH_WORD = "$_flumePackageInstallPath_"

FLUME_START_TEMPATE_KEY = "template"
FLUME_START_ANSIBLE_FILE_KEY = "ansibleFile"
FLUME_START_SERVICE_SCRIPT_KEY = "serverScript"
FLUME_START_CONF_PATH_KEY = "confDir"
FLUME_START_CONF_NAME_KEY = "confName"

FLUME_START_SERVICE_SCRIPT_WORD = "$_flumeScript_"
FLUME_START_CONF_PATH_WORD = "$_flumeConfDir_"
FLUME_START_CONF_NAME_WORD = "$_flumeConfName_"

def setupAnsibleFlume(rootPath, flume):
    if flume == None:
        print "Flume should not be empty"
        return -1
    
    flume_install = flume[FLUME_INSTALL_KEY]
    if flume_install == None:
        print "flume_install should not be empty"
        return -1
    
    flume_start = flume[FLUME_START_KEY]
    if flume_start == None:
        print "flume_start should not be empty"
        return -1
    
    flume_common_info = {}
    flume_common_info[FLUME_HOST_NAME_WORD] = flume[FLUME_NAME_KEY]
    flume_common_info[FLUME_HOST_USER_WORD] = flume[FLUME_USER_KEY]
    
    setupAnsibleFlumeInstall(rootPath, flume_common_info, flume_install)
    setupAnsibleFlumeStart(rootPath, flume_common_info, flume_start)
    
def setupAnsibleFlumeInstall(rootPath, flume_common_info, flume_install): 
    flume_install_info = {}
    flume_install_info[FLUME_HOST_NAME_WORD] = flume_common_info[FLUME_HOST_NAME_WORD]
    flume_install_info[FLUME_HOST_USER_WORD] = flume_common_info[FLUME_HOST_USER_WORD]
    flume_install_info[FLUME_INSTALL_PACKAGE_WORD] = rootPath + flume_install[FLUME_INSTALL_PACKAGE_KEY]
    flume_install_info[FLUME_INSTALL_INSTALL_PATH_WORD] = flume_install[FLUME_INSTALL_INSTALL_PATH_KEY]
    flume_install_template_file = rootPath + flume_install[FLUME_INSTALL_TEMPLATE_KEY] 
    flume_install_ansible_file = rootPath + flume_install[FLUME_INSTALL_ANSIBLE_FILE_KEY]
    
    buildAnsibleFlume(flume_install_template_file, flume_install_ansible_file, flume_install_info)
    
def setupAnsibleFlumeStart(rootPath, flume_common_info, flume_start):
    flume_start_info = {}
    flume_start_info[FLUME_HOST_NAME_WORD] = flume_common_info[FLUME_HOST_NAME_WORD]
    flume_start_info[FLUME_HOST_USER_WORD] = flume_common_info[FLUME_HOST_USER_WORD]
    flume_start_info[FLUME_START_SERVICE_SCRIPT_WORD] = flume_start[FLUME_START_SERVICE_SCRIPT_KEY]
    flume_start_info[FLUME_START_CONF_PATH_WORD] = flume_start[FLUME_START_CONF_PATH_KEY]
    flume_start_info[FLUME_START_CONF_NAME_WORD] = flume_start[FLUME_START_CONF_NAME_KEY]
    flume_start_template_file = rootPath + flume_start[FLUME_INSTALL_TEMPLATE_KEY] 
    flume_start_ansible_file = rootPath + flume_start[FLUME_START_ANSIBLE_FILE_KEY]
    buildAnsibleFlume(flume_start_template_file, flume_start_ansible_file, flume_start_info)
    
    buildAnsibleFlume(flume_start_template_file, flume_start_ansible_file, flume_start_info)
    
def buildAnsibleFlume(flume_template_path, flume_ansible_path, flume_info_map):
    if not os.path.exists(flume_template_path):
        print "flume template file " + flume_template_path + " is not existed"
        return -1
    
    template = open(flume_template_path).read()
    for flumeInfoKey in flume_info_map.keys():
        template = template.replace(flumeInfoKey, flume_info_map[flumeInfoKey])
    
    flume_ansible_dir = flume_ansible_path[:flume_ansible_path.rindex("/")]
    
    if not os.path.exists(flume_ansible_dir):
        os.makedirs(flume_ansible_dir)
    
    if os.path.exists(flume_ansible_path):
        os.remove(flume_ansible_path)
        
    flumeAnsibleFile = os.open(flume_ansible_path, os.O_CREAT|os.O_RDWR)
    os.write(flumeAnsibleFile, template)
    os.close(flumeAnsibleFile)