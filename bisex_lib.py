from bs4 import BeautifulSoup
from bs4 import re
import requests
import webbrowser
import time

#BiSEx Library - Biva Secure Extractor (Ɔ) Copyleft André Almeida 2016

#setting the http headers to simulate an user using Chrome on Mac OS
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept":"text/html,application/xhtlm+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

class Proprosal:
    def __init__(self, index, name, link, value, percentage):
        self.index = index
        self.name = name
        self.link = link
        self.value = value
        self.percentage = percentage

def connectTo(url, headers, cookie):
    session = requests.Session()
    print("Tentando conectar em " + url + "...")
    req = session.get(url, headers = headers, cookies = cookie)
    if req.status_code != 200:
        print("Conexão falhou: erro " + str(req.status_code))
        exit(0)
    print("Conexão bem sucedida!")
    print("---------")
    return req

def getCookie(request):
    return request.cookies

def getToken(request):
    bs_token = BeautifulSoup(request.text, "html.parser")
    return bs_token.input.next.attrs['value']

def setUser_data(email, password, request):
    return {
        'utf8' : '✓',
        'authenticity_token' : getToken(request),
        'user[email]' : email,
        'user[password]' : password,
        'user[remember_me]' : '0',
        'commit' : 'Entrar'
    }

def logIn(url, headers, user_data, cookie):
    print("Logando em Biva como " + user_data['user[email]'] + "...")
    request = requests.post(url, headers = headers,
                         data = user_data, cookies = cookie)
    bs_post = BeautifulSoup(request.text, "html.parser")
    if bs_post.find("h4") == None:
        print("Login falhou, verifique email e senha.")
        exit(0)
    print(bs_post.find("h4").text+"!")
    print("---------")
    return request

def getOpenOffers(props):
    i = 0
    for p in props:
        if p.percentage != "100":
            i = i + 1
            link = p.link
            print("Proposta aberta! Valor: " + str(p.value) +
              " ("+str(p.percentage)+"% financiado)\n" +
              "Link: " + p.link)
            webbrowser.open(p.link,new=2)
    if i == 0:
        print("Nenhuma proposta aberta disponível.")
    else:
        print(str(i) + " proposta(s) abertas!")

def getHours():
    hours = str(time.localtime().tm_hour)
    mints = time.localtime().tm_min
    if mints < 10:
        mints = "0" + str(mints)
    else:
        mints = str(mints)
    return '['+ hours + ':' + mints + ']'

def getProposals(bs, props, last):
    print("Procurando propostas da home page... " + getHours())

    props = []
    url_base = "https://biva.com.br"
    i = 0
    first = bs.find("h4", {"class" : "proposal-title"}).a.attrs['href']

    if last == None:
        last = first
    elif last == first:
        print("Nenhuma proposta nova encontrada...")
        return last

    prop_names = bs.findAll("h4", {"class" : "proposal-title"})
    for p in prop_names:
        name_prop = p.a.text
        link_prop = url_base + p.a.attrs['href']
        props.append(Proprosal(i, name_prop, link_prop, 0, 0))
        i = i + 1

    i = 0
    prop_values = bs.findAll("div", {"class" : "proposal-footer"})
    for p in prop_values:
        value_prop = p.span.strong.text
        percentage_prop = p.div.div.attrs['data-progress']
        props[i] = Proprosal(i, props[i].name, props[i].link,
                             value_prop, percentage_prop)
        i = i + 1

    print("Propostas obtidas: " + str(len(props)) + '\n')

    print("Imprimindo propostas:")
    for p in props:
        print('['+str(p.index)+'] '+ p.name + "\n" +
              'Valor: ' + str(p.value) +
                " ("+str(p.percentage)+"% financiado)")

    print("")
    getOpenOffers(props)
    return last
