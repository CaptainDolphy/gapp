import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os.path

url = "https://gevo.edookit.net/user/login"

##generovani cookies.json file, kdyz neexistuje

def createCookiesJson(_headless):
    with sync_playwright() as p:
        ##open browser
        browser = p.chromium.launch(headless=_headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        page.wait_for_url("https://gevo.edookit.net/", timeout=900000)

        cookies = context.cookies()
        ##delani json filu, tohle tam musi byt jinak to nefunguje
        cookiesJson = {
             "cookies": cookies
        }
        with open("cookies.json", "w") as f:
                json.dump(cookiesJson, f)
        context.close()

def getTimeTable(_headless): 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=_headless)
        context = browser.new_context(storage_state="cookies.json")
        page = context.new_page()
        page.goto(url)

        ## Expired cookies handling, sometimes we can still log in
        if (page.get_by_text("Přihlásit přes").is_visible()):
            page.get_by_text("Přihlásit přes").click()
            if (page.get_by_role("button", name="Google").is_visible()):
                page.get_by_role("button", name="Google").click()
                
            os.remove('cookies.json')
            if (page.url != url):
                createCookiesJson()

        ## Main TimeTable Getter
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



if os.path.isfile('cookies.json') == False:
    createCookiesJson(_headless=False)

if os.path.isfile('cookies.json'):
    getTimeTable(_headless=True)
