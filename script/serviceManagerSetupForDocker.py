import os

DEVICE_KEY = "devices"
DOCKER_CONTAINER_NAME_KEY = 'name'
DOCKER_CONTAINER_IP_KEY = 'ip'
DOCKER_CONTAINER_PORT_KEY = 'port'
DOCKER_CONTAINER_IMAGE_KEY = "dockerImage"
DOCKER_CONTAINER_NET_KEY = "dockerNet"

def setupDockerContainer(dockerContainerFile, components):
    if components == None:
        print "The components map should not be Null"
        return -1
    
    docker_container_map = {}
    for componentKey in components.keys():
        component = components[componentKey]
        if component == None:
            print "The component " + componentKey + " should not be Null"
            continue
        
        devices = component[DEVICE_KEY]
        if devices == None:
            print "The device " + componentKey + " should not be Null"
            continue
        
        for hostKey in devices.keys():
            host = devices[hostKey]
            if host == None:
                print "The host " + hostKey + " should not be Null"
                continue
            
            host_info = {}
            host_info[DOCKER_CONTAINER_NAME_KEY] = host[DOCKER_CONTAINER_NAME_KEY]
            host_info[DOCKER_CONTAINER_IP_KEY] = host[DOCKER_CONTAINER_IP_KEY]
            host_info[DOCKER_CONTAINER_PORT_KEY] = host[DOCKER_CONTAINER_PORT_KEY]
            host_info[DOCKER_CONTAINER_IMAGE_KEY] = host[DOCKER_CONTAINER_IMAGE_KEY]
            host_info[DOCKER_CONTAINER_NET_KEY] = host[DOCKER_CONTAINER_NET_KEY]
            docker_container_map[hostKey] = host_info
    
    buildDockerContainerScript(dockerContainerFile, docker_container_map)
    
    
def buildDockerContainerScript(dockerContainerFile, docker_container_map):
    
    dockerContainerFileDir = dockerContainerFile[:dockerContainerFile.rindex("/")]
    
    if not os.path.exists(dockerContainerFileDir):
        os.makedirs(dockerContainerFileDir)
    
    if os.path.exists(dockerContainerFile):
        os.remove(dockerContainerFile)
    
    dockerContainerScriptFile = os.open(dockerContainerFile, os.O_CREAT|os.O_RDWR)
    os.write(dockerContainerScriptFile, "#!/bin/sh\n")
    for dockerContainerKey in docker_container_map.keys():
        dockerContainer = docker_container_map[dockerContainerKey]
        command = "docker run -i -t -d --net " + dockerContainer[DOCKER_CONTAINER_NET_KEY] + \
                          " -p " + str(dockerContainer[DOCKER_CONTAINER_PORT_KEY]) + ":" + str(dockerContainer[DOCKER_CONTAINER_PORT_KEY]) + \
                          " --ip " + dockerContainer[DOCKER_CONTAINER_IP_KEY] + \
                          " --name " + dockerContainer[DOCKER_CONTAINER_NAME_KEY] + \
                          " " + dockerContainer[DOCKER_CONTAINER_IMAGE_KEY] + " /bin/bash\n"
        os.write(dockerContainerScriptFile, command)
        
    os.close(dockerContainerScriptFile)    