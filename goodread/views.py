from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from books.models import BookReview


def landing_page(request):
    return render(request=request, template_name="landing_page.html")


class HomePageView(View):

    def get(self, request):
        book_reviews = BookReview.objects.all().order_by("-created_at")

        page_size = request.GET.get("page_size", 10)
        paginator = Paginator(book_reviews, page_size)
        page_num = request.GET.get("page", 1)
        page_objects = paginator.get_page(page_num)

        return render(request=request, template_name="home_page.html", context={"page_objects": page_objects})
