# __Time__ : 2020/10/6 下午5:05
# __Author__ : '__YDongY__'


from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类
        view = super().as_view(**initkwargs)
        return login_required(view)
