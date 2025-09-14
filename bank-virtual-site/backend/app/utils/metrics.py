from prometheus_client import Counter, Histogram, make_asgi_app

requests_total = Counter('requests_total', 'Total requests')
latency = Histogram('request_latency_seconds', 'Request latency')

def setup_metrics(app):
    app.mount("/metrics", make_asgi_app())