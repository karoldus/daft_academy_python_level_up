from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.counter = 0

class HelloResp(BaseModel):
    msg: str

@app.get("/") #dekorator - widok odpowiedzi na metodę get, ścieżka domyslna
def root():
    return {"message": "Hello World"}

# @app.get("/hello/{name}") # obsługa GET z parametrem
# def hello_name_view(name: str):
#     return f"Hello {name}"

@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter

#7.3 TYPOWANIE
@app.get("/hello/{name}", response_model=HelloResp)
def read_item(name: str):
    return HelloResp(msg=f"Hello {name}")