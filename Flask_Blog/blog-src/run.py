# __Time__ : 2020/9/30 上午10:40
# __Author__ : '__YDongY__'

from blog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
