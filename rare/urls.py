from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rareapi.views import login_user, register_user, PostView, CategoryView, TagView, CommentView, UserView, RareUserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'category', CategoryView, 'category')
router.register(r'user', UserView, 'user')
router.register(r'rareuser', RareUserView, 'rareuser')
router.register(r'tags', TagView, 'tag')
router.register(r'posts', PostView, 'post')
router.register(r'comments', CommentView, 'comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
    # path('rareuser/<int:pk>/', RareUserView.as_view({'get': 'get'}), name='rareuser'),
]
