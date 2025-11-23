import logging, time, json

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created)),
            "level": record.levelname,
            "msg": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
        }
        return json.dumps(base, ensure_ascii=False)

_logger = logging.getLogger("app")
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(JsonFormatter())
    _logger.setLevel(logging.INFO)
    _logger.addHandler(_handler)

# Public logger reference
logger = _logger

def log_event(event: str, **fields):
    logger.info(json.dumps({"event": event, **fields}, ensure_ascii=False))
