from bs4 import BeautifulSoup
import time
import requests
from bisex_lib import *

print("BiSEx - Biva Secure Extractor 0.8v\n(Ɔ) Copyleft André Almeida 2016\n")

#conecting to the login page and extracting coockie
url_login = "https://biva.com.br/login/"
req_login = connectTo(url_login, headers, None)
coockie_login = getCookie(req_login)

#setting the user_data dict to send by POST
email = "teste@gmail.com"
password = "BaSWUwufrucrafud2cHe"
user_data = setUser_data(email, password, req_login)

#logining into biva.com.br
req_post = logIn(url_login, headers, user_data, coockie_login)
coockie_prop = getCookie(req_post)

#getting proprosals
proposals = []
url_prop = "https://biva.com.br/painel/propostas"
last_proposal = None
print("")
while True:
    req_prop = connectTo(url_prop, headers, coockie_prop)
    bs_prop = BeautifulSoup(req_prop.text, "html.parser")
    last_proposal = getProposals(bs_prop, proposals, last_proposal)
    print("Próxima checagem em 1 minuto...\n")
    time.sleep(60)
