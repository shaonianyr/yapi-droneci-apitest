# YApi - DroneCI 接口自动化测试

## 简介

* 使用 YApi 服务端测试
* Python 将包装出 [项目id] + [项目token] + [测试结果pwd]，对接 DroneCI
* 测试报告采用 selenium 遍历网页大小截长图作为邮件发送附件
（发送 pdf / html 附件方案均已抛弃，前者不能被腾讯企业邮箱兼容预览，后者无法在任意邮箱内显示样式。）

技术交流 QQ 群: 552643038

【 欢迎来 Star !!! 】

## 前提

YApi 服务端的测试需要具备 globalCookie 的功能。

详情见：

[github](https://github.com/ShaoNianyr/docker-YApi)

[testerhome](https://testerhome.com/topics/22309)


## DroneCI触发指令

```
    python3 yapi.py [项目id] [项目token] /code/pictures/
```

## 本地开发

```
    git clone https://github.com/ShaoNianyr/yapi-droneci-apitest.git
    cd yapi-droneci-apitest
    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt
    python3 yapi.py [项目id] [项目token] [当前pwd]
```

## 代码详情

* 登录 YApi —— 这里把登录后的 set-cookie 字段取出来放进 headers，实现免密码登录。

```
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
```

* 执行 YApi 接口端服务端测试 —— 借助 selenium 来实现

```
driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
count = 0
fileList = []
for i in data["data"]:
    downloadTestsuiteUrl = 'your_yapi_url/api/open/run_auto_test?id=' + str(i["_id"]) + '&token=' + project_token + '&mode=html&email=false&download=false'
    driver.get(downloadTestsuiteUrl)
```

* 遍历截图测试报告 —— 检测到页面有未通过字段

```
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
```
