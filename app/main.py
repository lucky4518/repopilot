from fastapi import FastAPI

app = FastAPI(title="RepoPilot")


@app.get("/")
def root():
    return {
        "message": "RepoPilot is running"
    }