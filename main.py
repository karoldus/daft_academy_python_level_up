from fastapi import FastAPI, Response, HTTPException, Request
from fastapi.exceptions import RequestValidationError # praca domowa 1.3
from fastapi.responses import PlainTextResponse # praca domowa 1.3
from pydantic import BaseModel
import hashlib #sha512 - praca domowa 1.3
import datetime
import urllib.parse #pd 1.3


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


#zajęcia 1 - praca domowa z3
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=401)

@app.get("/auth", status_code=401)
def auth(password: str, password_hash: str, response: Response, request: Request):
    if ' ' in password or password == Null:
        raise HTTPException(status_code=401, detail="Wrong password")
    h = hashlib.sha512(password.encode())
    if password_hash == h.hexdigest():
        response.status_code = 204
        return password
    raise HTTPException(status_code=401, detail="Wrong password")

#zajęcia 1 - praca domowa z4

def number_of_letters(word):
    ans = 0
    for char in word:
        if char.isalpha():
            ans += 1
    return ans


app.id = 0
app.patients = []
@app.post("/register", status_code=201)
def register(json_data: dict):
    name = json_data["name"]
    surname = json_data["surname"]
    app.id += 1

    date = datetime.datetime.now()
    date_v = date + datetime.timedelta(days=(number_of_letters(name)+number_of_letters(surname)))
    date_v = date_v.strftime("%Y-%m-%d")
    date = date.strftime("%Y-%m-%d")
    new_patient = {
            "id": app.id,
            "name": name,
            "surname": surname,
            "register_date": date,
            "vaccination_date": date_v
            }
    app.patients.append(new_patient)
    return new_patient

#zajęcia 1 - praca domowa z5
@app.get('/patient/{id}', status_code=200)
def patient(id: int, response: Response):
    if id < 1:
        raise HTTPException(status_code=400, detail="ID must be > 0")
    else:
        for p in app.patients:
            if p['id'] == id:
                return p
        
        raise HTTPException(status_code=404, detail="Wrong ID")  # from fastapi import FastAPI, Header, HTTPException

