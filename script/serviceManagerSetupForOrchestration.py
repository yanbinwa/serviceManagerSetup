import os

DEVICE_KEY = "devices"

ORCHESTRATION_PACKAGE_KEY = "package"
ORCHESTRATION_TEMPLATE_KEY = "template"
ORCHESTRATION_INSTALL_PATH_KEY = "setup_dir"

ORCHESTRATION_NAME_KEY = "name"
ORCHESTRATION_USER_KEY = "user"
ORCHESTRATION_START_COMMAND_KEY = "command"

ORCHESTRATION_ANSIBLE_FILE_PATH = "ansibleFile" 

ORCHESTRATION_HOST_NAME_WORD = "$_hostname_"
ORCHESTRATION_HOST_USER_WORD = "$_user_"
ORCHESTRATION_JAR_SRC_WORD = "$_orchestrationJarSrc_"
ORCHESTRATION_JAR_INSTALL_WORD = "$_orchestrationJarInstallPath_"
ORCHESTRATION_START_COMMAND_WORD = "$_orchestrationStartCommand_"

def setupAnsibleOrchestration(rootPath, orchestrations):
    if orchestrations == None:
        print "The orchestrations map should not be Null"
        return -1
    
    orchestration_ansible_map = {}
    orchestration_package_path = rootPath + orchestrations[ORCHESTRATION_PACKAGE_KEY]
    orchestration_template_file = rootPath + orchestrations[ORCHESTRATION_TEMPLATE_KEY]
    orchestration_install_path = orchestrations[ORCHESTRATION_INSTALL_PATH_KEY]
    
    devices = orchestrations[DEVICE_KEY]
    if devices == None:
        print "The orchestration devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The orchestration " + deviceKey + " should not be Null"
            continue
        
        orchestration_ansible_info = {}
        orchestration_ansible_info[ORCHESTRATION_HOST_NAME_WORD] = device[ORCHESTRATION_NAME_KEY]
        orchestration_ansible_info[ORCHESTRATION_HOST_USER_WORD] = device[ORCHESTRATION_USER_KEY]
        orchestration_ansible_info[ORCHESTRATION_START_COMMAND_WORD] = device[ORCHESTRATION_START_COMMAND_KEY]
        orchestration_ansible_info[ORCHESTRATION_JAR_SRC_WORD] = orchestration_package_path
        orchestration_ansible_info[ORCHESTRATION_JAR_INSTALL_WORD] = orchestration_install_path
        orchestration_ansible_info[ORCHESTRATION_ANSIBLE_FILE_PATH] = rootPath + device[ORCHESTRATION_ANSIBLE_FILE_PATH]
        orchestration_ansible_map[deviceKey] = orchestration_ansible_info
        
    buildAnsibleOrchestration(orchestration_template_file, orchestration_ansible_map)
        
def buildAnsibleOrchestration(orchestration_template_file, orchestration_ansible_map):
    if not os.path.exists(orchestration_template_file):
        print "orchestration template file " + orchestration_template_file + " is not existed"
        return -1
    
    template = open(orchestration_template_file).read()
    for orchestrationAnsibleInfoKey in orchestration_ansible_map.keys():
        orchestrationAnsibleInfo = orchestration_ansible_map[orchestrationAnsibleInfoKey]
        if orchestrationAnsibleInfo == None:
            print "orchestration ansible info " + orchestrationAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(ORCHESTRATION_HOST_NAME_WORD, orchestrationAnsibleInfo[ORCHESTRATION_HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_HOST_USER_WORD, orchestrationAnsibleInfo[ORCHESTRATION_HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_JAR_SRC_WORD, orchestrationAnsibleInfo[ORCHESTRATION_JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_JAR_INSTALL_WORD, orchestrationAnsibleInfo[ORCHESTRATION_JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(ORCHESTRATION_START_COMMAND_WORD, orchestrationAnsibleInfo[ORCHESTRATION_START_COMMAND_WORD])
        
        orchestrationAnsibleFile = orchestrationAnsibleInfo[ORCHESTRATION_ANSIBLE_FILE_PATH]
        if os.path.exists(orchestrationAnsibleFile):
            os.remove(orchestrationAnsibleFile)
            
        orchestrationAnsibleFileScript = os.open(orchestrationAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(orchestrationAnsibleFileScript, tempTemplate)