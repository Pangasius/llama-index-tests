#gui for chatbot
#http://localhost:8080/?prompt=

import time
import requests

from querier import QueryEngine

BOT_FLAG = "A: "
HUMAN_FLAG = "Q: "
QUERIER_FLAG = "R: "
INFO_PROMPT = "At any time, use [HELP] followed by a question in the answer to receive additional information from the search tool named R.\n"
STANDARD_PROMPT = INFO_PROMPT + BOT_FLAG + "Hello, how can I help you?\n"

class Chatbot:
    def __init__(self, endpoint="http://localhost:8080"):
        self.log = [STANDARD_PROMPT]
        
        self.endpoint = endpoint
        
        self.query_engine = QueryEngine()
        
    def prompt(self, prompt):
        self.log.append(HUMAN_FLAG + prompt + "\n")
        
        dialog = self.log[:1][-5:]
        dialog = " ".join(dialog) + BOT_FLAG
        
        response = requests.get(f"{self.endpoint}/?prompt={dialog}")
        
        #truncate to one response, remove any HUMAN_FLAG
        response = response.text.replace(dialog, "").split(HUMAN_FLAG)[0].split(BOT_FLAG)[0].strip()
        
        if response.__contains__("[HELP]") :
            query_prompt = response.split("[HELP]")[1].strip()
            q_response = str(self.query_engine.query(query=query_prompt))
            self.log.append(BOT_FLAG + response + "\n" + QUERIER_FLAG + q_response + "\n")
            
        response = requests.get(f"{self.endpoint}/?prompt={dialog}")
        
        #truncate to one response, remove any HUMAN_FLAG
        response = response.text.replace(dialog, "").split(HUMAN_FLAG)[0].split(BOT_FLAG)[0].strip()
        
        self.log.append(BOT_FLAG + response + "\n")
        
        return response
    
    def start(self):
        time.sleep(1)
        
        while True:
            #prompt with the color light orange
            prompt =  input("\033[93m" + "You: " + "\033[90m") + "\n"
            
            if prompt == "clear\n":
                self.log = [STANDARD_PROMPT]
                #print in red
                print("\033[91m" + "Command [CLEAR]: " + "\033[0m" + "Chat log cleared.")
                continue
            elif prompt == "log\n":
                #print in green
                print("\033[92m" + "Command [LOG]: " + "\033[0m" + "".join(self.log))
                continue
            elif prompt == "help\n":
                #print in yellow
                print("\033[93m" + "Command [HELP]: " + "\033[0m" + "Commands: [CLEAR], [LOG], [HELP]")
                continue
            
            #response with the color light blue
            print("\033[94m" + "Chatbot: " + "\033[0m" + self.prompt(prompt) )
            
            
def run_chatbot(endpoint="http://localhost:8080"):
    Chatbot(endpoint=endpoint).start()

if __name__ == "__main__":
    import concurrent.futures
    from endpoint import ModelEndpoint
    
    print("Initializing model endpoint and chatbot...")
    
    model_endpoint = ModelEndpoint()
    
    print(f"Model endpoint initialized at {model_endpoint.url}")
    
    chatbot = Chatbot(model_endpoint.url)
    
    print("Chatbot initialized.")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("Starting model endpoint and chatbot...")
        
        executor.submit(model_endpoint.start)
        
        print("Model endpoint started.")
        
        executor.submit(chatbot.start)
        
        print("Chatbot started.")
