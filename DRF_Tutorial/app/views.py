import json
from datetime import datetime

from django.views import View
from django.http.response import JsonResponse, HttpResponse

from rest_framework.views import APIView, status
from rest_framework.response import Response

from .models import BookInfo, HeroInfo
from .serializers import BookInfoSerializer, HeroInfoSerializer


class BooksAPIVIew(View):
    """
    查询所有图书、增加图书
    """

    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'title': book.title,
                'pub_date': book.pub_date,
                'read': book.read,
                'comment': book.comment,
                'image': book.image.url if book.image else ''
            })
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
        新增图书
        路由：POST /books/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            title=book_dict.get('title'),
            pub_date=datetime.strptime(book_dict.get('pub_date'), '%Y-%m-%d').date()
        )

        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'pub_date': book.pub_date,
            'read': book.read,
            'comment': book.comment,
            'image': book.image.url if book.image else ''
        }, status=201)


class BookAPIView(View):
    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'pub_date': book.pub_date,
            'read': book.read,
            'comment': book.comment,
            'image': book.image.url if book.image else ''
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.title = book_dict.get('title')
        book.pub_date = datetime.strptime(book_dict.get('pub_date'), '%Y-%m-%d').date()
        book.save()

        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'pub_date': book.pub_date,
            'read': book.read,
            'comment': book.comment,
            'image': book.image.url if book.image else ''
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse(status=204)


class DRFBooksAPIView(APIView):
    def get(self, request):
        queryset = BookInfo.objects.all()
        serializer = BookInfoSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class DRFBookAPIView(APIView):
    def get(self, request, pk):
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)
        serializer = BookInfoSerializer(instance=book)
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        book = BookInfo.objects.get(id=pk)
        serializer = BookInfoSerializer(book, data=data)
        if serializer.is_valid():  # True
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pass


class DRFHerosAPIView(APIView):
    def get(self, request):
        queryset = HeroInfo.objects.all()
        serializer = HeroInfoSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

