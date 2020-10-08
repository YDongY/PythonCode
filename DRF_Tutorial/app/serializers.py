# __Time__ : 2020/10/7 下午10:14
# __Author__ : '__YDongY__'

from rest_framework import serializers
from .models import BookInfo, HeroInfo


def about_django(value):
    if 'django' not in value.lower():
        raise serializers.ValidationError("图书不是关于Django的")


class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    # title = serializers.CharField(label='名称', max_length=20, validators=[about_django]) # 补充验证行为
    title = serializers.CharField(label='名称', max_length=20, required=False)
    pub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    comment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)

    # heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    # def validate_title(self, value):
    #     """对<field_name>字段进行验证"""
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("图书不是关于Django的")
    #     return value
    #
    # def validate(self, attrs):
    #     """对多个字段进行比较验证"""
    #     read = attrs['read']
    #     comment = attrs['comment']
    #     if read < comment:
    #         raise serializers.ValidationError('阅读量小于评论量')
    #     return attrs

    def create(self, validated_data):
        """新建"""
        # return BookInfo(**validated_data)
        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.title = validated_data.get('title', instance.title)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.read = validated_data.get('read', instance.read)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

    # 实现了上述两个方法后，在反序列化数据的时候，就可以通过save()方法返回一个数据对象实例了
    # book = serializer.save()


class HeroInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='名字', max_length=20)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    description = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)
    # book = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
    # book = serializers.StringRelatedField(label='图书')
    book = BookInfoSerializer()


"""
book = PrimaryKeyRelatedField：此字段将被序列化为关联对象的主键。

   {'id': 6, 'name': '乔峰', 'gender': 1, 'description': '降龙十八掌', 'book': 2}

book = StringRelatedField：此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）

   {'id': 6, 'name': '乔峰', 'gender': 1, 'description': '降龙十八掌', 'book': '天龙八部'}
   
book = BookInfoSerializer()

　　{'id': 6, 'name': '乔峰', 'gender': 1, 'comment': '降龙十八掌', 
            'book': OrderedDict([('id', 2), ('title', '天龙八部'), ('pub_date','1986-07-24'), ('read', 36), ('comment', 40),
                ('image', None)])}
"""

""" 
一本书关联多个人物，使用 Many

heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  

"""


class HeroModelSerializer(serializers.ModelSerializer):
    book = BookInfoSerializer()

    class Meta:
        model = HeroInfo
        fields = ('id', 'name', 'gender', 'description', 'book')
