from django.urls import re_path


from .views import AddDocumentsView, ListIndexView, MultiSearchView, SearchView, ShowIndexDocuemntCountView, ShowIndexView, DocumentShowView, DocumentIndexView, ShowStoreProductIndexView

urlpatterns = [
    re_path(r"^index/$", ListIndexView.as_view()),
    re_path(r"^index/search/$",
            MultiSearchView.as_view()),
    re_path(
        r"^index/stats/$", ShowIndexDocuemntCountView.as_view()),
    re_path(
        r"^index/(?P<index_name>[\w-]+)/add-documents/$", AddDocumentsView.as_view()),
    re_path(
        r"^store/(?P<store_id>[\w-]+)/remove-documents/$", ShowStoreProductIndexView.as_view()),
    re_path(r"^index/(?P<index_name>[\w-]+)/$", ShowIndexView.as_view()),
    re_path(r"^index/(?P<index_name>[\w-]+)/search/$",
            SearchView.as_view()),
    re_path(
        r"^index/(?P<index_name>[\w-]+)/document/$", DocumentIndexView.as_view()),
    re_path(
        r"^index/(?P<index_name>[\w-]+)/document/(?P<id>[\w-]+)/$", DocumentShowView.as_view()),

]
