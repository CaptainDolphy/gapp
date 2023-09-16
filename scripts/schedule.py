import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://gevo.edookit.net/user/login"

import os.path

##generovani cookies.json file, kdyz neexistuje
def createCookiesJson():
    with sync_playwright() as p:
        ##open browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.get_by_text("Přihlásit přes").click() 
        page.get_by_role("button", name="Google").click()
        page.wait_for_url("https://gevo.edookit.net/", timeout=900000)

        cookies = context.cookies()
        ##delani json filu, tohle tam musi byt jinak to nefunguje
        cookiesJson = {
             "cookies": cookies
        }
        with open("cookies.json", "w") as f:
                json.dump(cookiesJson, f)

        scrapeTimetable(page, False)
        context.close()


def getTimeTable(): 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="cookies.json")
        page = context.new_page()
        page.goto(url)

        scrapeTimetable(page, True)



def scrapeTimetable(page, checkForExpired):
    expiredEdookit = False
    
    if (page.get_by_text("Přihlásit přes").is_visible()) and checkForExpired:
        page.get_by_text("Přihlásit přes").click()
        ## musi byt kvuli edge case kde to redirectne rovnou
        if (page.get_by_role("button", name="Google").is_visible()):
            page.get_by_role("button", name="Google").click()
        expiredEdookit = True

    ## tohle taky nekdy to throwne error 500 (zustane to na random strance)
    if page.url != "https://gevo.edookit.net/":
        os.remove("cookies.json")
        createCookiesJson()
    
    html = page.inner_html('#prints-timetable')
    soup = BeautifulSoup(html, 'html.parser')
    
    classes = soup.find_all('div', {'class':'hoverLesson'})
    data = []

    for i in range(classes.__len__()):

        class_ = classes[i].text.replace('\xa0',' ').split('\n')
        class_info = list(filter(None,[s.lstrip() for s in class_]))
    
        schedule_json = {
            f"Class {i+1} " : {
                "Subject": class_info[0],
                "Teacher": class_info[1],
                "Room": class_info[2],
                "Day": class_info[3],
                "Time": class_info[4]
            }
        }
        
        data.append(schedule_json)

        with open("schedule.json", "w") as f:
            json.dump(data, f)

    if expiredEdookit:
        os.remove("cookies.json") 

        

if os.path.isfile('cookies.json') == False:
    createCookiesJson()
else:
    getTimeTable()
