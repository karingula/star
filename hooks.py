from apistar.server.components import ReturnValue
from apistar import http
import json


class SampleHook:
    def on_request(self) -> str:
        self.request_message = "Welcome to the playground"
        print(self.request_message)
        return "sleep with fishes"
    def on_response(self, ret:ReturnValue) -> http.Response:
        self.response_message = "Bye- Bye to the playground!"
        ret = json.loads(ret.content)
        # sanitizing the response
        ret['message'] = 'King is Back!'
        return http.Response(json.dumps(ret))
        
