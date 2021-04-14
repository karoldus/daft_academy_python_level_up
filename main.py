from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.counter = 0

class HelloResp(BaseModel):
    msg: str

@app.get("/") #endpoint pod główną ścieżką. @ to dekorator - widok odpowiedzi na metodę get, ścieżka domyslna
def root():
    return {"message": "Hello world!"}

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


#zajęcia1 - praca domowa z2
@app.get("/method")
def method_get():
    return {"method": "GET"}

@app.post("/method", status_code=201)
def method_post():
    return {"method": "POST"}

@app.delete("/method")
def method_delete():
    return {"method": "DELETE"}

@app.put("/method")
def method_put():
    return {"method": "PUT"}

@app.options("/method")
def method_options():
    return {"method": "OPTIONS"}