from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")

@app.get("/")
def read_root():
	REQUEST_COUNT.inc()
	return {"message": "Observability Project Running"}

@app.get("/health")
def health_check():
	return{"status": "healthy"}

@app.get("/metrics")
def metrics():
	return Response(generate_latest(), media_type="text/plain")




