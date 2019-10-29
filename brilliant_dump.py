import os
import time
import json
import pickle
import urllib
import requests
import platform
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from pathlib import Path, PureWindowsPath
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

#Open a Chrome windows controlled by selenium
def InitializeChrome_Linux():
    global driver
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

def main():
    if platform.system() == 'Windows':
        InitializeChrome_Windows()
    if platform.system() == 'Linux':
        InitializeChrome_Linux()
    if platform.system() == 'Darwin':
        InitializeChrome_MacOS()
    time.sleep(10)
    goToBrilliantWebsite()
    input("Please go to a course you want to dump. Warning: this will erase all the progress you've made in this course.\nPress any key to continue...")
    dumpCourse()

def InitializeChrome_Windows():
    global driver
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    username_windows = input("Please enter your username the way it's written in C:/Users/ - it's needed to locate your Chrome user data.\nUsername:")
    user_data_path = Path('C:/Users/' + str(username_windows) + '/AppData/Local/Google/Chrome/User Data')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument(f'--user-data-dir={user_data_path}')
    path_to_chromedriver = str(Path("./binaries/chromedriver.exe").absolute())
    driver = webdriver.Chrome(path_to_chromedriver, options = chrome_options)
    print('initialized Chrome window!')

def InitializeChrome_MacOS():
    pass

def goToBrilliantWebsite():
    driver.get('https://brilliant.org/')

'''
def dumpCookies():
    print("Attempting to dump cookies...")
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    print("Cookies dumped to cookies.pkl! Please don't delete!")
def importCookies():
    print("Attempting to import cookies...")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("Cookies imported!")
'''

def loginBrilliant():
    login_button = driver.find_element_by_css_selector("#app > div > div > div > div.index-hero > header > a.btn.login-btn")
    login_button.click()

def dumpCourse():
    start_course_button = driver.find_element_by_css_selector("#app > div > div:nth-child(2) > div > section.header.mobile > div > div > a")
    start_course_button.click()
    restart_course_button = driver.find_element_by_css_selector("#cmp_quizzes_interstitial_pane_id > div.course-quiz-sidebar.pane-sidebar > div.course-quiz-footer.row > div > div > div.course-quiz-restart")
    restart_course_button.click()
    yes_restart_button = driver.find_element_by_css_selector("#confirm-modal > div.modal-footer > a.btn.btn-accent.confirm")
    yes_restart_button.click()
    time.sleep(2)
    #Course progress has been reset to zero and we're on page one. Let's start dumping the course
    course_condition = 0
    print("Please tell me which button to press:\n1 for 'Continue'\n2 for 'Show explanation' and then 'Continue' and\n3 when you're on the last panel of the course and\n4 when you're done!")
    while course_condition != 4:
        course_condition = input()
        course_condition = course_condition.strip()
        course_condition = int(course_condition)
        print(course_condition)
        if course_condition == 1:
            print("1 selected!")
            continue_button = driver.find_element_by_css_selector("#interstitial-pane-continue-form")
            DownloadSiteAsPDF(driver, "1.pdf")
            time.sleep(5)
            continue_button.click()
        if course_condition == 2:

            show_explanation_button = driver.find_element_by_css_selector("#cmp_quizzes_problemset_id > div.course-quiz-sidebar > div.solv-details.course-quiz-solv-details.row > div.solv-details-footer.clearfix > div > a > span.solutions-hidden")
            show_explanation_button.click()
            SavePageWithExtension()
        if course_condition == 3:
            SavePageWithExtension()
            finish_quiz_button = driver.find_element_by_css_selector("#interstitial-pane-continue-form > button")
            finish_quiz_button.click()
    input("Done! Wanna do another course? [y/n]: ")

def DownloadSiteAsPDF(driver, target_path):
    """Download the currently displayed page to target_path."""
    def execute(script, args):
        driver.execute('executePhantomScript',
                       {'script': script, 'args': args})

    # hack while the python interface lags
    driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
    # set page format
    # inside the execution script, webpage is "this"
    page_format = 'this.paperSize = {format: "A4", orientation: "portrait" };'
    execute(page_format, [])

    # render current page
    render = '''this.render("{}")'''.format(target_path)
    execute(render, [])
    html = driver.page_source
    with io.open(driver.title + ".html", "w", encoding="utf-8") as f:
        f.write(html)
        f.close()


    try:
        # create the API client instance
        client = pdfcrowd.HtmlToPdfClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
        client.setPageHeight("-1")
        client.setNoMargins(True)

        # run the conversion and write the result to a file
        client.convertFileToFile(driver.title + ".html", 'MyLayout.pdf')
    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

        # handle the exception here or rethrow and handle it at a higher level
        raise

    driver.quit()
    pdf = PyPDF2.PdfFileReader("MyLayout.pdf", "rb")
    p = pdf.getPage(0)
    w_in_user_space_units = p.mediaBox.getWidth()
    h_in_user_space_units = p.mediaBox.getHeight()
    # 1 user space unit is 1/72 inch
    # 1/72 inch ~ 0.352 millimeters
    w = float(p.mediaBox.getWidth()) * 0.352
    h = float(p.mediaBox.getHeight()) * 0.352

    print(w)
    print(h)

if __name__ == '__main__':
    main()