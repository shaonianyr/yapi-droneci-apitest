FROM joyzoursky/python-chromedriver:3.6-selenium

# upgrade pip
RUN pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN mkdir code
WORKDIR code
RUN pwd

RUN apt-get update && \
    apt-get install -y ttf-wqy-microhei ttf-wqy-zenhei && \
    apt-get clean

COPY requirements.txt /code/

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY yapi.py /code/ 
COPY sendEmail.py /code/
RUN mkdir pictures && ls

CMD ["/bin/bash"]