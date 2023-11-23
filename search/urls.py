from django.urls import re_path


from .views import ListIndexView, ShowIndexView

urlpatterns = [
    re_path(r"^index/$", ListIndexView.as_view()),
    re_path(r"^index/(?P<index_name>[\w-]+)/$", ShowIndexView.as_view()),
]
