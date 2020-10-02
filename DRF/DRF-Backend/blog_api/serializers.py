# __Time__ : 2020/10/2 下午1:18
# __Author__ : '__YDongY__'
from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')
        model = Post
