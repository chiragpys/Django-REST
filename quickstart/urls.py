from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.routers import DefaultRouter

# router = DefaultRouter(trailing_slash=False)
# router.register(r'snippets', SnippetViewSet, basename='snippet')
# router.register(r'permission', SnippetPermissionView, basename='permission',)


urlpatterns = [
    # path('snippets/', snippet_list,),
    # path('snippets/<int:pk>/', snippet_detail,),
    # path('snippetsbase/<int:pk>', snippetbaseserializer),
    # path('listserilizer/', snippetlistserializer),
    # path('hyperlink/', snippetlisthyperlink, name='hyperlink'),
    # path('hyperlink/<int:pk>', snippetdetailhyperlink, name='hyperlink-list'),

    path('', ApiRoot.as_view()),
    path('snippets/', SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>', SnippetDetail.as_view(), name='snippet-detail'),

    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user-detail'),

    path('api/login', Login.as_view()),
    path('api/logout/', Logout.as_view()),

    # path('', include(router.urls)),

    path('filter/', ListSnippet.as_view()),
    path('djangofilter', ListDjangoFilter.as_view()),
    path('costomfilter', ListCustomFilter.as_view()),

    path('throttle', example_view)

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', 'api'])
