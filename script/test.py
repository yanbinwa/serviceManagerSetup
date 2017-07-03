if __name__ == "__main__":

#     path = "/User/yanbinwa/ppm/message.txt"
#     
#     path1 = "/User/yanbinwa/ppm/message.txt"
#     
#     map1 = {}
#     map1['wyb'] = 1
#     print map1.has_key('zcl')

    logFiles = 'message,console'
    logFileList = logFiles.split(',')
    for logFile in logFileList:
        print logFile