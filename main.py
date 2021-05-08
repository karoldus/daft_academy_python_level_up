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

# app.last_login_session = ""
# app.last_login_token = ""

# @app.post("/login_session", status_code=201)
# def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)): # pobiera user i password za pomocą BasicAuth
#     #return {"username": credentials.username, "password": credentials.password} # wydobywanie user i password
#     correct_username = secrets.compare_digest(credentials.username, "4dm1n")
#     correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
#     if not(correct_password and correct_username):
#         raise HTTPException(status_code=401)
#     session_token = hashlib.sha256(f"{credentials.username} + {credentials.password}".encode()).hexdigest()
#     response.set_cookie(key="session_token", value=session_token)
#     app.last_login_session = session_token
#     return {"OK"}


# @app.post("/login_token", status_code=201)
# def login_token(credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = secrets.compare_digest(credentials.username, "4dm1n")
#     correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
#     if not(correct_password and correct_username):
#         raise HTTPException(status_code=401)
#     session_token = hashlib.sha256(f"{credentials.username} + {credentials.password}".encode()).hexdigest()
#     app.last_login_token = session_token
#     return {"token": session_token}



# # 3.3
# from fastapi.responses import PlainTextResponse

# @app.get("/welcome_session")
# def welcome_session(format:str = "", session_token: str = Cookie(None)):
#     if session_token != app.last_login_session:
#         raise HTTPException(status_code=401)
#     if format == "json":
#         return {"message": "Welcome!"}
#     elif format == "html":
#         return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
#     else:
#         return PlainTextResponse(content="Welcome!", status_code=200)



# @app.get("/welcome_token")
# def welcome_token(token: str = "", format: str = ""):
#     if (token == "") or (token != app.last_login_token):
#         raise HTTPException(status_code=401)
#     if format == "json":
#         return {"message": "Welcome!"}
#     elif format == "html":
#         return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
#     else:
#         return PlainTextResponse(content="Welcome!", status_code=200)


# # 3.4 - wylogowywanie
# from fastapi.responses import RedirectResponse

# @app.delete("/logout_session")
# def logout_session(format:str = "", session_token: str = Cookie(None)):
#     if session_token != app.last_login_session and session_token != app.last_login_token:
#         raise HTTPException(status_code=401)

#     app.last_login_session = ""
#     url = "/logged_out?format=" + format
#     return RedirectResponse(url=url, status_code=303)



# @app.delete("/logout_token")
# def logout_token(token: str = "", format: str = ""):
#     if (token == "") or (token != app.last_login_token and token != app.last_login_session):
#         raise HTTPException(status_code=401)

#     app.last_login_token = ""
#     url = "/logged_out?format=" + format
#     return RedirectResponse(url=url, status_code=303)


# @app.get("/logged_out", status_code=200)
# def logged_out(format:str = ""):
#     if format == "json":
#         return {"message": "Logged out!"}
#     elif format == "html":
#         return HTMLResponse(content="<h1>Logged out!</h1>", status_code=200)
#     else:
#         return PlainTextResponse(content="Logged out!", status_code=200)



# 3.5

# logowanie

app.last_login_session = []
app.last_login_token = []

import random
random.seed(datetime.datetime.now())

@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)): # pobiera user i password za pomocą BasicAuth
    #return {"username": credentials.username, "password": credentials.password} # wydobywanie user i password
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    secret = str(random.randint(0, 999999))
    session_token = hashlib.sha256(f"{credentials.username}{credentials.password}{secret}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    if len(app.last_login_session) >= 3: 
        app.last_login_session.pop(0)
    app.last_login_session.append(session_token)
    return {"OK"}


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    secret = str(random.randint(0, 999999))
    session_token = hashlib.sha256(f"{credentials.username}{credentials.password}{secret}".encode()).hexdigest()
    if len(app.last_login_token) >= 3: 
        app.last_login_token.pop(0)
    app.last_login_token.append(session_token)
    return {"token": session_token}



# dostęp
from fastapi.responses import PlainTextResponse

@app.get("/welcome_session")
def welcome_session(format:str = "", session_token: str = Cookie(None)):
    if session_token not in app.last_login_session:
        raise HTTPException(status_code=401)
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
    else:
        return PlainTextResponse(content="Welcome!", status_code=200)



@app.get("/welcome_token")
def welcome_token(token: str = "", format: str = ""):
    if (token == "") or (token not in app.last_login_token):
        raise HTTPException(status_code=401)
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
    else:
        return PlainTextResponse(content="Welcome!", status_code=200)


#wylogowywanie
from fastapi.responses import RedirectResponse

@app.delete("/logout_session")
def logout_session(format:str = "", session_token: str = Cookie(None)):
    if session_token not in app.last_login_session:
        raise HTTPException(status_code=401)

    app.last_login_session.remove(session_token)
    url = "/logged_out?format=" + format
    return RedirectResponse(url=url, status_code=303)



@app.delete("/logout_token")
def logout_token(token: str = "", format: str = ""):
    if (token == "") or (token not in app.last_login_token):
        raise HTTPException(status_code=401)

    app.last_login_token.remove(token)
    url = "/logged_out?format=" + format
    return RedirectResponse(url=url, status_code=303)


@app.get("/logged_out", status_code=200)
def logged_out(format:str = ""):
    if format == "json":
        return {"message": "Logged out!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Logged out!</h1>", status_code=200)
    else:
        return PlainTextResponse(content="Logged out!", status_code=200)






#zajęcia 4




import sqlite3

# łączenie się z bazą przy uruchamianiu apki
@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific

# analogicznie rozłączenie
@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

# with sqlite3.connect("northwind.db") as connection:
#     connection.text_factory = lambda b: b.decode(errors="ignore") # northwind specific
#     cursor = connection.cursor() # używamy kursora
#     products = cursor.execute("SELECT ProductName FROM Products").fetchall()
#     print(len(products))
#     print(products[4])

# zamykanie
# conn.close()

# pobieranie danych z bazy bez kursora

# @app.get("/suppliers/{supplier_id}")
# async def single_supplier(supplier_id: int):
#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute(
#         f"SELECT CompanyName, Address FROM Suppliers WHERE SupplierID = {supplier_id}").fetchone()

#     return data

# Lepsze sposoby:

# @app.get("/suppliers/{supplier_id}")
# async def single_supplier(supplier_id: int):
#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute(
#         "SELECT CompanyName, Address FROM Suppliers WHERE SupplierID = ?", (supplier_id, )).fetchone()

#     return data
# @app.get("/suppliers/{supplier_id}")
# async def single_supplier(supplier_id: int):
#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute(
#         "SELECT CompanyName, Address FROM Suppliers WHERE SupplierID = :supplier_id",
#         {'supplier_id': supplier_id}).fetchone()

#     return data


@app.get("/employee_with_region")
async def employee_with_region():
    app.db_connection.row_factory = sqlite3.Row # Dzięki temu dostęp do pól następuje po nazwie shipper[„CompanyName”] zamiast shipper[0]
    data = app.db_connection.execute('''
        SELECT Employees.LastName, Employees.FirstName, Territories.TerritoryDescription 
        FROM Employees JOIN EmployeeTerritories ON Employees.EmployeeID = EmployeeTerritories.EmployeeID
        JOIN Territories ON EmployeeTerritories.TerritoryID = Territories.TerritoryID;
     ''').fetchall()
    return [{"employee": f"{x['FirstName']} {x['LastName']}", "region": x["TerritoryDescription"]} for x in data]




# praca domowa

# 4.1

@app.get("/categories", status_code=200)
async def categores():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
    SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID
    ''').fetchall()
    return {"categories": [{"id": x['CategoryID'], "name": x["CategoryName"]} for x in data]}

@app.get("/customers", status_code=200)
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
    SELECT CustomerID, CompanyName, Address || ' ' || PostalCode || ' ' || City || ' ' || Country AS full_address FROM Customers ORDER BY CustomerID
    ''').fetchall()
    return {"customers": [{"id": f"{x['CustomerID']}", "name": x["CompanyName"], "full_address": (x["full_address"])} for x in data]}


# 4.2

@app.get('/products/{id}', status_code=200)
async def products(id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT ProductName FROM Products WHERE ProductID = ?",(id,)).fetchone()
    if data == None:
        raise HTTPException(status_code=404)
    return {"id": id, "name": data['ProductName']}

#4.3

@app.get('/employees', status_code=200)
async def employees(limit: int = -1, offset: int = 0, order: str = 'id'):
    app.db_connection.row_factory = sqlite3.Row
    columns = {'first_name' : 'FirstName', 'last_name' : 'LastName', 'city' : 'City', 'id' : 'EmployeeID'}
    if order not in columns.keys():
        raise HTTPException(status_code=400) 
    order = columns[order]
    data = app.db_connection.execute(f"SELECT EmployeeID, LastName, FirstName, City FROM Employees ORDER BY {order} LIMIT ? OFFSET ?",(limit, offset, )).fetchall()
    return {"employees": [{"id": x['EmployeeID'],"last_name":x['LastName'],"first_name":x['FirstName'],"city":x['City']} for x in data]}

# 4.4

@app.get('/products_extended', status_code=200)
async def products_extended():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
    SELECT Products.ProductID AS id, Products.ProductName AS name, Categories.CategoryName AS category, Suppliers.CompanyName AS supplier FROM Products 
    JOIN Categories ON Products.CategoryID = Categories.CategoryID JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID ORDER BY Products.ProductID
    ''').fetchall()
    return {"products_extended": [{"id": x['id'], "name": x['name'], "category": x['category'], "supplier": x['supplier']} for x in data]}

# 4.5

@app.get('/products/{id}/orders', status_code=200)
async def products_id_orders(id: int):
    app.db_connection.row_factory = sqlite3.Row # (UnitPrice x Quantity) - (Discount x (UnitPrice x Quantity))
    data = app.db_connection.execute(f'''
    SELECT Products.ProductID AS id, Orders.OrderID, Customers.CompanyName AS customer, [Order Details].Quantity AS quantity, [Order Details].UnitPrice AS unitprice, [Order Details].Discount as discount 
    FROM Products JOIN [Order Details] ON Products.ProductID = [Order Details].ProductID JOIN Orders ON [Order Details].OrderID = Orders.OrderID JOIN Customers ON Orders.CustomerID = Customers.CustomerID WHERE Products.ProductID = {id} ORDER BY Orders.OrderID
    ''').fetchall()
    if data == None:
        raise HTTPException(status_code=404)
    return {"orders": [{"id": x["id"], "customer": x["customer"], "quantity": x["quantity"], "total_price": round(((x['unitprice'] * x['quantity']) - (x['discount'] * (x['unitprice'] * x['quantity']))), 2)} for x in data]}