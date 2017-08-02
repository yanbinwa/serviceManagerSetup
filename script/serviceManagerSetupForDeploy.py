import os
import serviceManagerSetupConstants

def setupAnsibleDeploy(rootPath, deploys):
    if deploys == None:
        print "The deploys map should not be Null"
        return -1
    
    deploy_ansible_map = {}
    deploy_package_path = rootPath + deploys[serviceManagerSetupConstants.PACKAGE_KEY]
    deploy_template_file = rootPath + deploys[serviceManagerSetupConstants.TEMPLATE_KEY]
    deploy_install_path = deploys[serviceManagerSetupConstants.INSTALL_PATH_KEY]
    deploy_log_dir = deploys[serviceManagerSetupConstants.LOG_PATH_KEY]
    
    devices = deploys[serviceManagerSetupConstants.DEVICE_KEY]
    if devices == None:
        print "The deploys devices should not be Null"
        return -1
    
    for deviceKey in devices.keys():
        device = devices[deviceKey]
        if device == None:
            print "The deploy " + deviceKey + " should not be Null"
            continue
        
        deploy_ansible_info = {}
        deploy_ansible_info[serviceManagerSetupConstants.HOST_NAME_WORD] = device[serviceManagerSetupConstants.NAME_KEY]
        deploy_ansible_info[serviceManagerSetupConstants.HOST_USER_WORD] = device[serviceManagerSetupConstants.USER_KEY]
        deploy_ansible_info[serviceManagerSetupConstants.START_COMMAND_WORD] = device[serviceManagerSetupConstants.START_COMMAND_KEY]
        deploy_ansible_info[serviceManagerSetupConstants.JAR_SRC_WORD] = deploy_package_path
        deploy_ansible_info[serviceManagerSetupConstants.JAR_INSTALL_WORD] = deploy_install_path
        deploy_ansible_info[serviceManagerSetupConstants.LOG_DIR_WORD] = deploy_log_dir
        deploy_ansible_info[serviceManagerSetupConstants.ANSIBLE_FILE_PATH] = rootPath + device[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        
        deploy_ansible_map[deviceKey] = deploy_ansible_info
        
    buildAnsibleDeploy(deploy_template_file, deploy_ansible_map)
        
def buildAnsibleDeploy(deploy_template_file, deploy_ansible_map):
    if not os.path.exists(deploy_template_file):
        print "deploy template file " + deploy_template_file + " is not existed"
        return -1
    
    template = open(deploy_template_file).read()
    for deployAnsibleInfoKey in deploy_ansible_map.keys():
        deployAnsibleInfo = deploy_ansible_map[deployAnsibleInfoKey]
        if deployAnsibleInfo == None:
            print "deploy ansible info " + deployAnsibleInfoKey + " should not be Null"
            continue
        
        tempTemplate = template.replace(serviceManagerSetupConstants.HOST_NAME_WORD, deployAnsibleInfo[serviceManagerSetupConstants.HOST_NAME_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.HOST_USER_WORD, deployAnsibleInfo[serviceManagerSetupConstants.HOST_USER_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_SRC_WORD, deployAnsibleInfo[serviceManagerSetupConstants.JAR_SRC_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.JAR_INSTALL_WORD, deployAnsibleInfo[serviceManagerSetupConstants.JAR_INSTALL_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.START_COMMAND_WORD, deployAnsibleInfo[serviceManagerSetupConstants.START_COMMAND_WORD])
        tempTemplate = tempTemplate.replace(serviceManagerSetupConstants.LOG_DIR_WORD, deployAnsibleInfo[serviceManagerSetupConstants.LOG_DIR_WORD])
        
        deployAnsibleFile = deployAnsibleInfo[serviceManagerSetupConstants.ANSIBLE_FILE_PATH]
        deployAnsibleFileDir = deployAnsibleFile[:deployAnsibleFile.rindex("/")]
    
        if not os.path.exists(deployAnsibleFileDir):
            os.makedirs(deployAnsibleFileDir)
        
        if os.path.exists(deployAnsibleFile):
            os.remove(deployAnsibleFile)
            
        deployAnsibleFileScript = os.open(deployAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(deployAnsibleFileScript, tempTemplate)
        os.close(deployAnsibleFileScript)
        