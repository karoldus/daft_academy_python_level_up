from functools import wraps

#---------------------------- konstrukcja dekoratora ------------------------------------------#

def dekorator(do_udekorowania):         # def nazwa_dekoratora (argument - lokalna nazwa funkcji, która zostanie udekorowana)
    print("Teraz dekoruje!")            # ten poziom wykonuje się tylko raz - w momencie dekorowania
    @wraps(do_udekorowania)             # wraps pozwala zachować pewne informacje o oryginalnej funkcji, wymaga from functools import wraps
    def inner(*args, **kwargs):         # wewnątrz dekoratora możemy utworzyć funkcję
        raw = do_udekorowania(*args, **kwargs) # oraz wywołać oryginalną funkcję, która była udekorowana
        ans = "Hello"
        names = raw.split()
        for name in names:
            ans += ' '
            ans += name.capitalize()
        return ans
    return inner                        # to co jest zwracane przez dekorator, jest wynikiem późniejszego wywołania funkcji po dekorowaniu
    # w tym przypadku dekorator zwraca funkcję (nie wywołaną - bez nawiasów), ale mógłby zwracać też wartość. 
    # Funkcja to wywołuje się w momencie wywołania funkcji udekorowanej. 
    # W takim przypadku inner musi przyjmować takie argumenty jak funkcja dekorowana - jeśli nie wiemy jakie możemy użyć *args i **kwargs

@dekorator
def name_surname():                 # dekorujemy funkcję. W tym miejscu wykona się print("Teraz dekoruje!")
    return "jan nowak"

name_surname()                      # W tym miejscu wykona się dekoracja - zamiast name_surname wykona się tak naprawdę to co zwraca dekorator - w tym przypadku zostanie wywołana funkcja inner



# ---------------- zadanie 2.1 -----------------------------#

def greetings(do_udekorowania):
    @wraps(do_udekorowania)
    def inner(*args):
        raw = do_udekorowania(*args)
        ans = "Hello"
        names = raw.split()
        for name in names:
            ans += ' '
            ans += name.capitalize()
        return ans
    return inner

@greetings
def name_surname():
    return "jan nowak"

assert name_surname() == "Hello Jan Nowak"


# ---------------- zadanie 2.2 -----------------------------#

def is_palindrome(do_udekorowania):
    @wraps(do_udekorowania)
    def inner(*args, **kwargs):
        word = do_udekorowania(*args, **kwargs)
        lst = []
        for char in word:
            if char.isalpha():
                lst.append(char.lower())
            elif char.isnumeric():
                lst.append(char)
        palin = True
        for i in range(len(lst)):
            if lst[i] != lst[len(lst)-i-1]:
                palin = False
        if palin == True:
            word += ' - is palindrome'
        else:
            word += ' - is not palindrome'
        return word
    return inner

@is_palindrome
def sentence():
    return "annA"

assert sentence() == "annA - is palindrome"


# ---------------- zadanie 2.3 -----------------------------#

def format_output(*args):         # ten tylko przechwytuje argumenty dekoratora
    def real_decorator(do_udekorowania):
        def inner(*ar, **kwargs):
            dic = do_udekorowania(*ar, **kwargs)
            ans = {}
            for arg in args:
                if arg.count("__")>0:
                    splitted = arg.split("__")
                    string = ""
                    for a in splitted:
                        if a in dic:
                            if string != "":
                                string += " "
                            string += dic[a]
                        else:
                            raise ValueError("ValueError")
                    ans[arg] = string
                else:
                    if arg in dic:
                        ans[arg] = dic[arg]
                    else:
                        raise ValueError("ValueError")
            print(ans)
            return ans
        return inner
    return real_decorator

import pytest

@format_output("first_name__last_name", "city")
def first_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warszawa",
    }

@format_output("first_name", "age")
def second_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warszawa",
    }

assert first_func() == {'first_name__last_name': 'Jan Kowalski', 'city': 'Warszawa'}

with pytest.raises(ValueError):
    second_func()



# ---------------- zadanie 2.4 -----------------------------#

def add_instance_method(klasa):
    def real_decorator(do_udekorowania):
        @wraps(do_udekorowania)
        def inner(*args, **kwargs):
            return do_udekorowania()
        setattr(klasa, do_udekorowania.__name__, inner)
        return do_udekorowania              # zwraca funkcję, dzięki czemu może ona zostać użyta/udekorowana ponownie
    return real_decorator

def add_class_method(klasa):
    def real_decorator(do_udekorowania):
        @wraps(do_udekorowania)
        def inner(*args, **kwargs):
            return do_udekorowania()
        setattr(klasa, do_udekorowania.__name__, inner)
        return do_udekorowania              # zwraca funkcję, dzięki czemu może ona zostać użyta/udekorowana ponownie
    return real_decorator





class A:
    pass

@add_class_method(A)
def foo():
    return "Hello!"

@add_instance_method(A)
def bar():
    return "Hello again!"

assert A.foo() == "Hello!"
assert A().bar() == "Hello again!"