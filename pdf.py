from selenium import webdriver
#python3 -m pip install --user pdfcrowd
import pdfcrowd
import time
import sys
import io
import os
import time
import json
import urllib
import requests
import pyautogui
import pickle
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import pyautogui
from pathlib import Path, PureWindowsPath
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
#python3 -m pip install --user PyPDF2
import PyPDF2


def download(driver, target_path):
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

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    user_data_path = Path('C:/Users/Ryzen/AppData/Local/Google/Chrome/User Data')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    path_to_chromedriver = str(Path("./binaries/chromedriver.exe").absolute())
    options.add_argument(f'user-agent={user_agent}')
    try:
        driver = webdriver.Chrome(options=options) 
    except:
        driver = webdriver.Chrome(path_to_chromedriver, options=options)
    driver = webdriver.PhantomJS(str(Path("./binaries/phantomjs.exe").absolute()))
    driver.get('http://stackoverflow.com')
    time.sleep(5)
    download(driver, "save_me.pdf")
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