from fastapi.responses import StreamingResponse



class batch:
    def __init__(self):
        self.batchQueue = []

    def addQueue(self, request: dict):
        self.batchQueue.append(request)

    def buildComponent(self, question: str, context: str, userid: str, streamObject: StreamingResponse):
        component = {
            "Question": question,
            "Context": context,
            "id": userid,
            "streamObject": streamObject
        }
        return component

    class executorBatch:
        def __init__(self, outer_instance):
            self.outer = outer_instance
            self.runQueue = []


        

        def execute_runQueue(self):
            maxlength = min(3, len(self.outer.batchQueue))
            
            if len(self.outer.batchQueue) == 0:
                
                return
            
            def response(modelname:str):
                return 

            # Select up to 'maxlength' items from outer batchQueue
            while True:
                self.runQueue = self.outer.batchQueue[:maxlength]
                self.outer.batchQueue=self.outer.batchQueue[maxlength:]
                response(self.runQueue)
                

            


