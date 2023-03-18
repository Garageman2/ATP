import time

from bs4 import BeautifulSoup
import requests
from splinter import Browser

#!Seems to require the request coming from the US

def construct_url(name:str):
    base = "https://www.atptour.com/en/players"
    editname = name.strip().lower().replace(" ","-")
    print(name)
    with Browser() as browser:
        browser.visit(base)
        pSearch = browser.find_by_id("playerInput")
        pSearch.fill(name)
        pSearch.click()
        time.sleep(2.0)
        pDropdown = browser.find_by_id("playerDropdown")
        for link in browser.find_by_tag('a'):
            if link.value == name:
                print(link.value)
                link.click()
                break
        input()

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


