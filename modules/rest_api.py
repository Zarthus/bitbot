import http.server, json, threading, uuid, urllib.parse
import flask
from src import utils

_bot = None
_events = None
class Handler(http.server.BaseHTTPRequestHandler):
    timeout = 10
    def do_GET(self):
        _bot.lock.acquire()
        try:
            parsed = urllib.parse.urlparse(self.path)
            query = parsed.query
            get_params = urllib.parse.parse_qs(query)

            _, _, endpoint = parsed.path[1:].partition("/")
            endpoint, _, args = endpoint.partition("/")
            args = list(filter(None, args.split("/")))

            response = ""
            code = 404

            hooks = _events.on("api").on(endpoint).get_hooks()
            if hooks:
                hook = hooks[0]
                authenticated = hook.get_kwarg("authenticated", True)
                key = get_params.get("key", None)
                print(key)
                if authenticated and (
                        not key or
                        not _bot.get_setting("api-key-%s" % key[0], False)):
                    code = 401
                else:
                    if parsed.path.startswith("/api/"):
                        response = _events.on("api").on(endpoint
                            ).call_for_result(params=get_params, path=args)

                        if response:
                            response = json.dumps(response, sort_keys=True,
                                indent=4)
                            code = 200

            self.send_response(code)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode("utf8"))
        except:
            pass
        finally:
            _bot.lock.release()

@utils.export("botset", {"setting": "rest-api",
    "help": "Enable/disable REST API",
    "validate": utils.bool_or_none})
class Module(object):
    def __init__(self, bot, events, exports):
        self.bot = bot
        global _bot
        _bot = bot

        self.events = events
        global _events
        _events = events

        if bot.get_setting("rest-api", False):
            self.httpd = http.server.HTTPServer(("", 5000), Handler)
            self.thread = threading.Thread(target=self.httpd.serve_forever)
            self.thread.daemon = True
            self.thread.start()

    def unload(self):
        self.httpd.shutdown()

    @utils.hook("received.command.apikey", private_only=True)
    def api_key(self, event):
        """
        :help: Generate a new API key
        :permission: api-key
        :prefix: APIKey
        """
        api_key = str(uuid.uuid4())
        self.bot.set_setting("api-key-%s" % api_key, True)
        event["stdout"].write(api_key)