from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import BookReviewSerializers
from books.models import BookReview


class BookReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)
        serializers = BookReviewSerializers(book_review)

        return Response(data=serializers.data)


class BookReviewListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        book_reviews = BookReview.objects.all().order_by("-id")

        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(queryset=book_reviews, request=request)
        serializers = BookReviewSerializers(page_obj, many=True)

        return paginator.get_paginated_response(data=serializers.data)
