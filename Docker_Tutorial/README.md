# Docker Tutorial

## Docker 快速搭建 Python 环境

```shell
$ tree
.
├── Dockerfile
├── main.py
└── README.md
0 directories, 3 files
```

### 创建 Python 项目

```python
# main.py

print("Docker Tutorial")
```

### 创建 Dockerfile 文件

```dockerfile
# https://hub.docker.com/_/python

FROM python:3.7-alpine3.11

COPY main.py /

CMD ["python","./main.py"]
```

### 构建 Image

```shell
sudo docker build -t python-test .
```

- `-t`选项指明构建 Image 的名称

### 运行 Docker 镜像

```shell
sudo docker run python-test
```

> 更多命令参考[我的博客](https://blog.ydongy.cn/2020/05/01/docker-cli.html)


# Docker-Compose Tutorial

Docker　用于管理应用程序，往往是单个容器(服务)，而对于我们经常开发的项目而言，往往是由多个服务相互作用。比如使用 Python 开发一个网站，至少需要 Python 应用程序服务以及数据库服务。
Docker-Compose 就是为同一个应用程序同时管理多个服务(容器)。

下面我们将使用 Docker-Compose 创建 C/S 应用程序

## Docker-Compose 搭建 C/S 应用程序

### 创建项目

```shell
.
├── client/
├── docker-compose.yml
└── server/

2 directories, 1 files
```

### 创建服务器

进入 server 目录创建三个文件

- server.py
- index.html
- Dockerfile

```shell
$ tree
.
├── Dockerfile
├── index.html
└── server.py
```

### 编辑　server.py

```python
import http.server
import socketserver

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", 5000), handler) as httpd:
    httpd.serve_forever()
```

### 编辑　HTML 文件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Hello Docker-Compose</h1>
</body>
</html>
```

### 编写 Dockerfile

```dockerfile
FROM python:3.7-alpine3.11

# 拷贝文件到容器 server 目录
ADD server.py /server/
ADD index.html /server/

# 容器运行后的工作目录
WORKDIR /server/
```

### 创建客户端

进入 client 目录创建三个文件

- client.py
- Dockerfile

```shell
$ tree
.
├── client.py
└── Dockerfile
```

### 编辑 client.py

```python
import urllib.request

fp = urllib.request.urlopen("http://localhost:5000")

content = fp.read().decode("utf-8")

print(content)

fp.close()
```

### 编辑 Dockerfile

```dockerfile
FROM python:3.7-alpine3.11

# 拷贝文件到容器　client 目录
ADD client.py /client/

# 容器运行后的工作目录
WORKDIR /client/
```

### 编辑 Docker-Compose

```yml
# 版本，与本地下载的 Docker-Compose有关
# 可在官网查看对应版本　https://docs.docker.com/compose/compose-file/
version: "3.8"

# 服务配置，一个服务就是一个容器
services:

    # 服务端容器，名称随便起，这里用 server
    server:
        build: server/
        command: python ./server.py
        ports:
            - 5000:5000

    # 客户端容器
    client:
        build: client/
        command: python ./client.py
        # 定义网络类型，这是 host 就是指 localhost,因为我们代码里写的就是 localhost
        # 如果不指定该参数，docker-compose 会随机分配一个 ip
        network_mode: host

        # 表示当前 clinet 服务依赖于 server 服务，希望客户端服务等待，直到服务器服务准备就绪
        depends_on:
            - server
```

### 构建 Docker-Compose

```shell
sudo docker-compose build
```

### 运行 Docker-Compose

```shell
sudo docker-compose up
```

我们会在控制台看到 index.html 内容，如果在本地浏览器访问 `http://localhost:5000` 同样可以看到相同内容

## Docker-Compose 基本命令[[官方](https://docs.docker.com/compose/reference/)]

- 启动

```shell script
sudo docker-compose up
# 容器重新编译再启动
sudo docker-compose up --build
# 后台启动
sudo docker-compose up -d --build
```

- 查看容器状态

```shell script
$ sudo docker-compose ps
          Name                  Command          State     Ports
----------------------------------------------------------------
docker_tutorial_client_1   python ./client.py   Exit 0
docker_tutorial_server_1   python ./server.py   Exit 137
```

- 执行容器内命令

```shell script
sudo docker-compose run flaskweb top
```

- 查看容器输出日志

```shell script
sudo docker-compose logs -f flaskweb
```

- 容器停止

```shell script
sudo docker-compose stop
# 容器停止并清除容器和网络
sudo docker-compose down
# 停止删除容器，网络，镜像
sudo docker-compose down --rmi all
```

- 在运行的容器中执行命令，例如：`docker-compose exec server ls`

```shell
docker-compose exec [service name][command]
```

- 检查镜像

```shell
docker inspect <tag or id>
```

## Docker-Compose 搭建 Flask+Redis 服务[[官网](https://docs.docker.com/compose/gettingstarted/)]

- 创建目录

```shell
mkdir composetest
cd composetest
```

- 创建一个 app.py 文件，编辑一下内容

```python
import time

import redis
from flask import Flask

app = Flask(__name__)

# redis 是应用程序网络上的 redis 容器的主机名。我们为 Redis 使用默认端口6379
# 因为容器会自动分配 IP，会与容器名称对应
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

- 在目录中创建 Dockerfile 输入以下内容

```dockerfile
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
# 安装依赖
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# 对外提供访问端口
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

- 在目录中创建 docker-compose.yml 输入以下内容

```yml
version: "3.8"
services:
  web:
    build: .
    ports:
      # 将容器和主机绑定到暴露的端口5000
      - "5000:5000"
  redis:
    # 该redis服务使用 从Docker Hub注册表中提取的公共Redis映像。
    image: "redis:alpine"
```

- 在项目目录中，通过运行来启动应用程序docker-compose up

```shell
docker-compose up
```

- 编辑 Compose 文件以添加绑定安装

```yml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
  redis:
    image: "redis:alpine"
```

volumes：将主机上的项目目录（当前目录）映射到容器 /code 内部，从而可以即时修改代码，而无需重建映像
environment：键设置了 FLASK_ENV 环境变量，该变量指示 flask run 要在开发模式下运行并在更改时重新加载代码


# 更多参考

- [Dockerfile 配置文件参考](https://docs.docker.com/engine/reference/builder/)
- [Docker-Compose 配置文件参考](https://docs.docker.com/compose/compose-file/)
- [Docker-Compose 命令](https://docs.docker.com/compose/reference/)
- [快速入门：Compose 和 Django](https://docs.docker.com/compose/django/)