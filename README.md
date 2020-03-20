# YApi - DroneCI 接口自动化测试

## 简介

* 使用 YApi 服务端测试
* Python 将包装出 [项目id] + [项目token] + [测试结果pwd]，对接 DroneCI
* 测试报告采用 selenium 遍历网页大小截长图作为邮件发送附件
（发送 pdf / html 附件方案均已抛弃，前者不能被腾讯企业邮箱兼容预览，后者无法在任意邮箱内显示样式。）

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