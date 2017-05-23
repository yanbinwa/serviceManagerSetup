import os

DEVICE_KEY = "devices"

COLLECTION_PACKAGE_KEY = "package"
COLLECTION_TEMPLATE_KEY = "template"
COLLECTION_INSTALL_PATH_KEY = "setup_dir"

COLLECTION_NAME_KEY = "name"
COLLECTION_USER_KEY = "user"
COLLECTION_START_COMMAND_KEY = "command"

COLLECTION_ANSIBLE_FILE_PATH = "ansibleFile" 

COLLECTION_HOST_NAME_WORD = "$_hostname_"
COLLECTION_HOST_USER_WORD = "$_user_"
COLLECTION_JAR_SRC_WORD = "$_collectionJarSrc_"
COLLECTION_JAR_INSTALL_WORD = "$_collectionJarInstallPath_"
COLLECTION_START_COMMAND_WORD = "$_collectionStartCommand_"

def setupAnsibleCollection(rootPath, collections):
    if collections == None:
        print "The collections map should not be Null"
        return -1
    
    collection_ansible_map = {}
    collection_package_path = rootPath + collections[COLLECTION_PACKAGE_KEY]
    collection_template_file = rootPath + collections[COLLECTION_TEMPLATE_KEY]
    collection_install_path = collections[COLLECTION_INSTALL_PATH_KEY]
    
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
        collection_ansible_info[COLLECTION_ANSIBLE_FILE_PATH] = rootPath + device[COLLECTION_ANSIBLE_FILE_PATH]
        collection_ansible_map[deviceKey] = collection_ansible_info
    
    buildAnsibleCollection(collection_template_file, collection_ansible_map)
        
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
        
        collectionAnsibleFile = collectionAnsibleInfo[COLLECTION_ANSIBLE_FILE_PATH]
        if os.path.exists(collectionAnsibleFile):
            os.remove(collectionAnsibleFile)
            
        collectionAnsibleFileScript = os.open(collectionAnsibleFile, os.O_CREAT|os.O_RDWR)
        os.write(collectionAnsibleFileScript, tempTemplate)