# 从零开始部署 Django(Nginx+uWSGI)

## 搭建虚拟环境

- 安装 VirtualEnv 和 VirtualEnvWrapper

```shell script
sudo pip install virtualenv -i https://pypi.doubanio.com/simple
sudo pip install virtualenvwrapper -i https://pypi.doubanio.com/simple
```

- 更改配置

```shell script
vim .bashrc

# ----添加，保存----
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

source .bashrc 
```

- 进入项目目录创建虚拟环境

```shell script
cd Django_Deploy

mkvirtualenv -p python3 venv
```

- 安装依赖

```shell script
pip install -r requirements.txt
```

## 安装 uWSGI

如果 requirements.txt 没有 uWSGI 包，执行以下命令进行安装

```shell script
sudo apt-get install build-essential python-dev
pip install uwsgi
```

### 测试你的 Django 项目

```shell script
python manage.py runserver 0.0.0.0:8000
```

如果正常运行，使用 uWSGI 运行它

```shell script
uwsgi --http :8000 --chdir /home/ydongy/Code/code_snippets/Django_Deploy --wsgi-file Django_Deploy/wsgi.py --master --processes 4 --threads 2
```

- `--chdir`：是项目目录
- `--wsgi-file`：是 Django 项目 wsgi.py 文件所在目录（属于相对目录）

接着访问浏览器，如果站点出现，则表示 uWSGI 能够从服务你的 Django 应用程序，其服务结构如下：

```shell script
client <-> uWSGI <-> Django
```

但是通常我们不会让浏览器直接与 uWSGI 通信，而是利用 Nginx 进行反向代理，且帮助 uWSGI 处理静态资源

## 安装 Nginx

在这里我们使用 APT 安装方式

```shell script
sudo apt-get install nginx
```

输入以下内容来启动 Nginx 服务器

```shell script
sudo systemctl start nginx
```

现在我们需要通过浏览器访问 IP:80，来访问 Nginx 服务器来检查它是否正常工作。如果收到　Welcome to nginx! 表示 Nginx 启动成功。

**注意：如果你使用云主机，需要检查自己的安全组是否开启 80 端口**

### 为站点配置 Nginx

在　/etc/nginx/sites-available/ 目录新建 `django_nginx.conf`

需要把配置文件中的 /path/to/your/mysite 更改为自己项目目录所在路径。其中还需要注意 uwsgi_params 文件所在目录，一般在 /etc/nginx/uwsgi_params 它是用来 Nginx 与 uWSGI 通信的

```editorconfig
# django_blog_nginx.conf

# the upstream component nginx needs to connect to
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name example.com; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /path/to/your/mysite/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }
}
```

该配置文件告诉 Nginx 在 8000 端口上为站点服务。Nginx 将处理静态文件和媒体文件，以及需要 Django 干预的请求

接着将此文件的符号链接到 /etc/nginx/sites-enabled 使 nginx 可以加载它：

```editorconfig
sudo ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled/
```

### 部署静态文件
在运行 Nginx 之前，我们必须将所有 Django 静态文件收集到静态文件夹中。首先，我们必须编辑 Django_Deploy/settings.py 添加：

```python
import os
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
```

然后运行

```python
python manage.py collectstatic
```

接着修改 settings.py

```python
DEBUG = False

ALLOWED_HOSTS = ['*']
```

### 测试 Nginx 服务器

由于我们对 Nginx 服务器配置进行了更改，因此我们需要重新启动服务器，以使这些更改生效：

```shell script
sudo systemctl restart nginx
```

将新图像（media.png）添加到 /media 目录，然后可以在浏览器中访问 http://yourdomain.com:8000/media/media.png 来查看 Nginx 是否正确提供了媒体文件。如果它不起作用，请尝试停止并重新启动 Nginx 服务器


## 完成部署

现在我们已经正确安装和配置了 uWSGI 和 Nginx，我们可以用它们同时服务 Django应用程序：

```shell script
uwsgi --socket yourdomain.com:8001 --module mysite.wsgi --chmod-socket=664

# eg:uwsgi --socket 127.0.0.1:8001 --module Django_Deploy.wsgi --chmod-socket=664
```

现在在浏览器中访问 http://yourdomain.com:8000　已经可以看到站点正常显示

### 配置 uWSGI 使用 .ini 文件运行

最后我们将与 uWSGI 一起使用的相同选项放入文件中，然后要求 uWSGI 与该文件一起运行。它使管理配置变得更加容易。

创建一个名为的文件 django_uwsgi.ini，同样修改对应的目录

```shell script
# django_uwsgi.ini file
[uwsgi]
# the socket (use the full path to be safe
socket          = 127.0.0.1:8001
# Django-related settings
# the base directory (full path)
chdir           = /path/to/your/project
# Django's wsgi file
module          = project.wsgi
# the virtualenv (full path)
home            = /path/to/virtualenv
# process-related settings
# master
master          = true
# maximum number of worker processes
processes = 2
threads = 2
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true

# 设置缓冲区
#post-buffering = 65535
# 设置缓冲区文件大小
#buffer-size = 65535
#harakiri-verbose = true
# 设置超时时间
#harakiri = 300
#pidfile = /opt/srv/run/uwsgi.pid
#daemonize = /opt/srv/log/uwsgi.log
```

- 通过配置文件启动 uWSGI

```shell script
uwsgi --ini django_uwsgi.ini
```

- 停止 uWSGI

```shell script
uwsgi --stop uwsgi.pid
```
