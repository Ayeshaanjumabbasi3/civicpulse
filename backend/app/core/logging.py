import json, logging
from contextvars import ContextVar
request_id_context: ContextVar[str] = ContextVar('request_id', default='-')
def set_request_id(value: str): return request_id_context.set(value)
def reset_request_id(token): request_id_context.reset(token)
class JsonFormatter(logging.Formatter):
    def format(self, record): return json.dumps({"level": record.levelname, "message": record.getMessage(), "request_id": request_id_context.get()})
def configure_logging():
    handler = logging.StreamHandler(); handler.setFormatter(JsonFormatter())
    logging.getLogger().handlers = [handler]; logging.getLogger().setLevel(logging.INFO)
