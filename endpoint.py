import tornado.ioloop
import tornado.web
from tornado.options import define, options

from model import ModelLLM

class ModelEndpoint:
    def __init__(self, port=8080, host="localhost", base_url=""):
        self.port = port
        self.host = host
        self.base_url = base_url
        
        self.url = f"http://{self.host}:{self.port}{self.base_url}"
        
        self.model = ModelLLM()
        
    def start(self) :
        define("port", default=self.port, help="run on the given port", type=int)
        define("host", default=self.host, help="run on the given host", type=str)
        define("base_url", default=self.base_url, help="base url", type=str)
        
        class ModelHandler(tornado.web.RequestHandler):
            def initialize(self):
                self.application.model = self.settings["model"]
                
            def get(self):
                prompt_text = self.get_argument("prompt", default="hello world")
                self.write(self.application.model.predict(prompt_text))
                
        app = tornado.web.Application([
            (r"/", ModelHandler),
        ], model=self.model, debug=True, autoreload=True)

        app.listen(options.port, options.host)
        
        tornado.ioloop.IOLoop.current().start()
    
def run_model_endpoint(port=8080, host="localhost", base_url=""):
    ModelEndpoint(port=port, host=host, base_url=base_url).start()

if __name__ == "__main__":
    run_model_endpoint()
