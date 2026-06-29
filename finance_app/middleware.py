import uuid
import logging
import threading


class TraceIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        trace_id = str(uuid.uuid4())[:8]
        request.trace_id = trace_id
        threading.current_thread().trace_id = trace_id
        response = self.get_response(request)
        response["X-Trace-Id"] = trace_id
        return response


class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = getattr(threading.current_thread(), "trace_id", "-")
        return True
