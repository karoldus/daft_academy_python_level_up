from fastapi import FastAPI

app = FastAPI()

@app.get("/") #dekorator - widok odpowiedzi na metoda get, ścieżka domyslna
def root():
    return {"message": "Hello World"}