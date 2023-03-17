from bs4 import BeautifulSoup
import requests

#!Seems to require the request coming from the US

def construct_url(name:str):
    base = "https://www.atptour.com/en/players"
    name = name.strip().lower().replace(" ","-")
    print(name)

def main():
    link = "https://www.atptour.com/en/players/carlos-alcaraz/a0e2/titles-and-finals"
    req = requests.get(link)
    print(req.status_code)
    content = BeautifulSoup(req.text)
    print(content.prettify())
    construct_url("Jannik Sinner")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


