# __Time__ : 2020/10/8 下午11:53
# __Author__ : '__YDongY__'


def application(env, start_response):
    start_response('200 ok', [('Content-Type', 'text/html')])
    return [b"Hello World"]
