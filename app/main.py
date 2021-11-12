from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"App": "Welcome to my Simple Authentication app"} 