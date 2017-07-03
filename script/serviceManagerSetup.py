import serviceManagerSetupForAnsibleHost
import serviceManagerSetupForAnsibleMainScript
import serviceManagerSetupForDocker
import serviceManagerSetupForZookeeper
import serviceManagerSetupForOrchestration
import serviceManagerSetupForCollection
import serviceManagerSetupForKafka
import serviceManagerSetupForCache
import serviceManagerSetupForLogging
import serviceManagerSetupForRedis
import serviceManagerSetupForCommons

import yaml
import sys

ROOT_TARGET_PATH_KEY = "root_path"
ANSIBLE_HOST_PATH_KEY = "ansible_host"
ANSIBLE_MAIN_PATH_KEY = "ansible_main"
COMPONENT_KEY = "components"
COMMON_KEY = "commons"
DOCKER_CONTAINER_PATH_KEY = "docker_container"

ZOOKEEPER_KEY = "zookeeper"
ORCHESTRATION_KEY = "orchestration"
COLLECTION_KEY = "collection"
KAFKA_KEY = "kafka"
CACHE_KEY = "cache"
LOGGING_KEY = "logging"
REDIS_KEY = "redis"

class serviceManagerSetup:

    def __init__(self):
        
        if len(sys.argv) < 2:
            print "Should input the manifest file path"
            exit(-1)
            
        self.manifestFile = sys.argv[1]        
        self.manifest = yaml.safe_load(open(self.manifestFile))
        
        self.rootPath = self.manifest[ROOT_TARGET_PATH_KEY]
                
        self.ansibleHostPath = self.rootPath + self.manifest[ANSIBLE_HOST_PATH_KEY]
        self.components = self.manifest[COMPONENT_KEY]
        if self.components == None:
            print "The components should not be Null"
            exit(-1)
            
        self.commons = self.manifest[COMMON_KEY]
            
        serviceManagerSetupForAnsibleHost.setupAnsibleHost(self.ansibleHostPath, self.components, self.commons)
        
        self.dockerContainer = self.rootPath + self.manifest[DOCKER_CONTAINER_PATH_KEY]
        serviceManagerSetupForDocker.setupDockerContainer(self.dockerContainer, self.components)
        
        self.ansibleMainPath = self.rootPath + self.manifest[ANSIBLE_MAIN_PATH_KEY]
        serviceManagerSetupForAnsibleMainScript.setupAnsibleMain(self.rootPath, self.ansibleMainPath, self.components, self.commons)
          
        self.zookeepers = self.components[ZOOKEEPER_KEY]
        serviceManagerSetupForZookeeper.setupAnsibleZookeeper(self.rootPath, self.zookeepers)
        
        self.orchestrations = self.components[ORCHESTRATION_KEY]
        serviceManagerSetupForOrchestration.setupAnsibleOrchestration(self.rootPath, self.orchestrations)
        
        self.collections = self.components[COLLECTION_KEY]
        serviceManagerSetupForCollection.setupAnsibleCollection(self.rootPath, self.collections)
        
        self.kafkas = self.components[KAFKA_KEY]
        serviceManagerSetupForKafka.setupAnsibleKafka(self.rootPath, self.kafkas)
        
        self.caches = self.components[CACHE_KEY]
        serviceManagerSetupForCache.setupAnsibleCache(self.rootPath, self.caches)
        
        self.logging = self.components[LOGGING_KEY]
        serviceManagerSetupForLogging.setupAnsibleCache(self.rootPath, self.logging)
        
        self.rediss = self.components[REDIS_KEY]
        serviceManagerSetupForRedis.setupAnsibleRedis(self.rootPath, self.rediss)
        
        serviceManagerSetupForCommons.setupAnsibleCommons(self.rootPath, self.commons)

# Start of the python invocation, the argv is manifest file
if __name__ == "__main__":
    setup = serviceManagerSetup()