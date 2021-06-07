from django.urls import path
from .views import ListingDeleteView
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create',views.create_listing,name="create"),
    path('<int:pk>/detail/',views.detail_view,name="detail"),
    path('<int:pk>/delete/',ListingDeleteView.as_view(),name="delete")
]
