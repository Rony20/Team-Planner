from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def demo():
    return{"Success":"Server running"}
