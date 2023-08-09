import argparse

parser = argparse.ArgumentParser(description="Run")
parser.add_argument('--runnable', '-m', type=str, default="chatbot", help="The file to run.")

args = parser.parse_args()

if args.runnable == "chatbot":
    from runnable.chatbot import run_chatbot
    
    run_chatbot()
    
elif args.runnable == "endpoint":
    from runnable.endpoint import run_model_endpoint
    
    run_model_endpoint()
    
elif args.runnable == "discord_index":
    from runnable.discord_index import run_discord_index
    
    run_discord_index()
    
elif args.runnable == "querier":
    from backend.querier import run_querier
    
    run_querier()
    
else :
    raise Exception("Invalid runnable.")