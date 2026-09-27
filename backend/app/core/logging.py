import json, logging
class JsonFormatter(logging.Formatter):
    def format(self, record): return json.dumps({"level": record.levelname, "message": record.getMessage()})
def configure_logging():
    handler = logging.StreamHandler(); handler.setFormatter(JsonFormatter())
    logging.getLogger().handlers = [handler]; logging.getLogger().setLevel(logging.INFO)
