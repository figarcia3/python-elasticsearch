from django.urls import re_path


from .views import AddDocumentsView, ListIndexView, SearchView, ShowIndexView, DocumentShowView, DocumentIndexView

urlpatterns = [
    re_path(r"^index/$", ListIndexView.as_view()),
    re_path(
        r"^index/(?P<index_name>[\w-]+)/add-documents/$", AddDocumentsView.as_view()),
    re_path(r"^index/(?P<index_name>[\w-]+)/$", ShowIndexView.as_view()),
    re_path(r"^index/(?P<index_name>[\w-]+)/search/$",
            SearchView.as_view()),
    re_path(
        r"^index/(?P<index_name>[\w-]+)/document/$", DocumentIndexView.as_view()),
    re_path(
        r"^index/(?P<index_name>[\w-]+)/document/(?P<id>[\w-]+)/$", DocumentShowView.as_view()),

]
