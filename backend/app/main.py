from fastapi import FastAPI

app = FastAPI(
    title="OnboardIQ API",
    description="AI-powered employee onboarding and organizational knowledge assistant",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
