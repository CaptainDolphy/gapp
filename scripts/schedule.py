import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://gevo.edookit.net/user/login"

import os.path

##generovani cookies.json file, kdyz neexistuje
if os.path.isfile('cookies.json') == False:
    with sync_playwright() as p:
        ##open browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.wait_for_url("https://gevo.edookit.net/")

        cookies = context.cookies()
        ##delani json filu, tohle tam musi byt jinak to nefunguje
        cookiesJson = {
             "cookies": cookies
        }
        with open("cookies.json", "w") as f:
                json.dump(cookiesJson, f)
        context.close()


def getTimeTable(): 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="cookies.json")
        page = context.new_page()
        page.goto(url)

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

if os.path.isfile('cookies.json'):
    getTimeTable()
