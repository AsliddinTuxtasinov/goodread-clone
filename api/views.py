from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework import views, response, status, pagination, validators, permissions

from api.serializers import BookReviewSerializers
from books.models import BookReview


class BookReviewDetailAPIView(views.APIView):

    @permission_classes((permissions.IsAuthenticatedOrReadOnly,))
    def get(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)
        serializers = BookReviewSerializers(book_review)

        return response.Response(data=serializers.data)

    @permission_classes((permissions.IsAuthenticated, ))
    def delete(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)

        if book_review.user == request.user:
            book_review.delete()
        else:
            raise validators.ValidationError(
                detail={"message": "You cannot delete this review"}, code=status.HTTP_400_BAD_REQUEST
            )

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @permission_classes((permissions.IsAuthenticated,))
    def put(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)
        serializers = BookReviewSerializers(instance=book_review, data=request.data)

        if serializers.is_valid():
            if book_review.user == request.user:
                serializers.save()
                return response.Response(data=serializers.data, status=status.HTTP_200_OK)
            else:
                raise validators.ValidationError(
                    detail={"message": "You cannot update this review"}, code=status.HTTP_400_BAD_REQUEST
                )

        return response.Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((permissions.IsAuthenticated,))
    def patch(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)
        serializers = BookReviewSerializers(
            instance=book_review, data=request.data, partial=True, context={"request_user": request.user}
        )

        if serializers.is_valid():
            if book_review.user == request.user:
                serializers.save()
                return response.Response(data=serializers.data, status=status.HTTP_200_OK)
            else:
                raise validators.ValidationError(
                    detail={"message": "You cannot update this review"}, code=status.HTTP_400_BAD_REQUEST
                )

        return response.Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviewListAPIView(views.APIView):
    queryset = BookReview.objects.all().order_by("-id")
    pagination_class = pagination.PageNumberPagination()

    @permission_classes((permissions.AllowAny,))
    def get(self, request):
        paginator = self.pagination_class
        page_obj = paginator.paginate_queryset(queryset=self.queryset, request=request)
        serializers = BookReviewSerializers(page_obj, many=True)

        return paginator.get_paginated_response(data=serializers.data)

    @permission_classes((permissions.IsAuthenticated,))
    def post(self, request):
        serializers = BookReviewSerializers(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return response.Response(data=serializers.data, status=status.HTTP_201_CREATED)

        return response.Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
