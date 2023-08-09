#gui for chatbot
#http://localhost:8080/?prompt=

import time
from llama_index.prompts.chat_prompts import CHAT_REFINE_PROMPT
from llama_index.response.schema import Response
from model import ModelLLM

from colorful import rainbow, random

from querier import QueryEngine

BOT_FLAG = "A: "
HUMAN_FLAG = "Q: "
STANDARD_PROMPT = BOT_FLAG + "Hello. I am a powerful chatbot capable of writing code in many languages and communicate on various topics. How can I help you?\n"

class Chatbot:
    def __init__(self, endpoint="http://localhost:8080"):
        self.log = [STANDARD_PROMPT]
        
        self.query_engine = QueryEngine()
        
    def prompt(self, prompt):
        self.log.append(HUMAN_FLAG + prompt)
        
        dialog = self.log
        dialog = "".join(dialog)
        
        #print in light blue
        print(random("Querying search engine... ") + "\033[0m")
        
        context_msg = self.query_engine.query(query=prompt)
        
        if isinstance(context_msg, Response):
            context = context_msg.response or BOT_FLAG + "Could not find a response."
        else :
            context = context_msg.response_txt or BOT_FLAG + "Could not find a response."
        
        sources = context_msg.get_formatted_sources()
        context = "".join(self.log) + context.strip() + "\n" + sources
        
        print("Done.")
        print(random("Answering without query...") + "\033[0m")
        
        existing_answer = BOT_FLAG + ModelLLM()._call(prompt="".join(self.log) + "\n" + BOT_FLAG).split("A: ")[0]
        
        print("Done.")
        print(random("Refining answer with query...") + "\033[0m")
        
        new_attempt = ModelLLM()._call(prompt=CHAT_REFINE_PROMPT.format(context_msg=context, query_str=prompt,existing_answer=existing_answer) + "\n" + BOT_FLAG).split("A: ")[0]
        
        print("Done.\n")
        
        self.log.append(new_attempt)
        
        #truncate to one response, remove any HUMAN_FLAG
        final_response = new_attempt + "\n" + sources
        
        return final_response
    
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
            
            
if __name__ == "__main__":
    import concurrent.futures
    from endpoint import ModelEndpoint
    
    chatbot = Chatbot()
    
    print("Chatbot initialized.")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("Starting chatbot...")

        executor.submit(chatbot.start)
        
        print("Chatbot started.")
