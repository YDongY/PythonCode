FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /src
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
