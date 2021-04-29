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
    if password =='':
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






# zajęcia 3






from fastapi import Request

# wypisywanie zawartości query params

# @app.get("/request_query_string_discovery/")
# def read_item(request: Request):
#     print(f"{request.query_params=}")
#     return request.query_params

from typing import List
from fastapi import FastAPI, Query

# zwraca wartość parametrów u i q z query params
@app.get("/request_query_string_discovery/")
def read_items(u: str = Query("default"), q: List[str] = Query(None)): #przyjmujemy parametry u i q, które są str. Domyślna wartość u to default, a q to None. q to lista, więc po wpisaniu q=a&q=b otrzymujemy "q":["a","b"]. u nie jest listą, więc przyjmuje tylko jedną wartość - ostatnią podaną. Analogicznie mogą być innymi typami np: int
    query_items = {"q": q, "u": u}
    return query_items



# zwracanie HTML statycznego
from fastapi.responses import HTMLResponse

@app.get("/static", response_class=HTMLResponse) # będziemy zwacać HTML: response_class=HTMLResponse
def index_static():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


# jinja2
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/jinja")
def read_item(request: Request):
    return templates.TemplateResponse("index.html.j2", { # nazwa stworzonej przez nas templatki
        "request": request, "my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]}) # parametry przekazywane do templatki


# routing dynamiczny

@app.get("/simple_path_tmpl/{sample_variable}")
def simple_path_tmpl(sample_variable: str):
    print(f"{sample_variable=}")
    print(type(sample_variable))
    return {"sample_variable": sample_variable} 



# zadania domowe po zajęciach 3

#3.1 
@app.get("/hello")
def hello_html(request: Request):
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d")
    return templates.TemplateResponse("hello.html.j2", {"request": request, "today_date": date})



# 3.2

import secrets
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Cookie

security = HTTPBasic() # do użycia BasicAuth

app.last_login_session = " "
app.last_login_token = " "

@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)): # pobiera user i password za pomocą BasicAuth
    #return {"username": credentials.username, "password": credentials.password} # wydobywanie user i password
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = hashlib.sha256(f"{credentials.username} + {credentials.password}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    app.last_login_session = session_token
    return {"OK"}


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = hashlib.sha256(f"{credentials.username} + {credentials.password}".encode()).hexdigest()
    app.last_login_token = session_token
    return {"token": session_token}
    