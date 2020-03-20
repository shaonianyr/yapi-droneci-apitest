import requests
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import sys
import re
import os
from sendEmail import sendEmail

# getCookie
login_url = 'your_yapi_url'
login_parameters = {"email": "", "password": ""}
login_response = requests.post(login_url, login_parameters)
set_cookie = login_response.headers['Set-Cookie']
array = re.split('[;,]',set_cookie)
cookie = ''
for arr in array:
    if arr.find('_yapi_token') >= 0 or arr.find('_yapi_uid') >= 0:
        cookie += arr + ';'

# getProjectIdTestsuites
project_id = sys.argv[1]
project_url = 'your_yapi_url/api/col/list?project_id=' + project_id
project_name = 'your_yapi_url/api/project/get?id=' + project_id
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "cookie": cookie
}
response = requests.get(project_name, headers=headers)
dataName = response.json()
name = dataName['data']['name']
print("测试项目：", name)
response = requests.get(project_url, headers=headers)
data = response.json()

# RunProjectIdTestsuites
project_token = sys.argv[2]
pwd = sys.argv[3]

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': pwd}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
count = 0
fileList = []
for i in data["data"]:
    downloadTestsuiteUrl = 'your_yapi_url/api/open/run_auto_test?id=' + str(i["_id"]) + '&token=' + project_token + '&mode=html&email=false&download=false'
    driver.get(downloadTestsuiteUrl)

    '''
        download html 方案及转 pdf 发邮件方案。
        因腾讯企业邮箱 pdf 预览功能做的比其他邮箱差得多，弃之。
        html 在各大邮箱中均无法显示样式，弃之。
    '''

    # time.sleep(3)
    # oldName = 'test.html'
    # newName = 'test_' + str(count) + '.html'
    # newNamePng = 'test_' + str(count) + '.png'
    # dir_link = pwd
    # os.chdir(dir_link)
    # os.rename(oldName, newName)
    # path = pwd + '/' + newName
    # content = open(path, "r", encoding="utf-8")
    # content = content.read()
    # print()
    # if '验证失败' in content:
    #     print('验证不通过')
    #     driver.get(path)
    #     scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    #     scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    #     driver.set_window_size(scroll_width, scroll_height)
    #     driver.save_screenshot(newNamePng)
    #     # pdfkit.from_file(newName, newNamePDF)
    #     sendSubject = '接口自动化测试报告'
    #     sendName = newNamePng
    #     sendContent = '部分接口验证失败，详情请下载附件查看。【YApi-DroneCI接口自动化开发测试】'
    #     sendPath = pwd + '/' + newNamePng
    #     sendFile = open(sendPath, 'rb').read()
    #     time.sleep(2)
    #     sendEmail(sendSubject, sendName, sendContent, sendFile)
    # else:
    #     print('验证通过')

    '''
        直接读 html 并转 png 发送方案。
        预览效果好，采纳。
    '''

    html = driver.execute_script("return document.documentElement.outerHTML")
    if '未通过' in html:
        print('测试集合：' + i['name'] + '验证不通过')
        count += 1
        newNamePng = 'test_' + str(count) + '_' + i['name'] + '.png'
        downloadPath = pwd + newNamePng
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(downloadPath)
        time.sleep(2)
    else:
        print('验证通过')
driver.quit()

if count > 0:
    sendSubject = name
    sendContent = '接口测试部分验证失败，详情请查看附件。【YApi-DroneCI接口自动化测试】'
    fileList = []
    for parent, dirnames, filenames in os.walk('./pictures'):
        for filename in filenames:
            fileList.append(filename)
    sendEmail(sendSubject, sendContent, pwd, fileList)