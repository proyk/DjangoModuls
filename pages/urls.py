from django.urls import path,include
from . import views
urlpatterns = [
    path('change_languages/', views.change_languages, name="change_languages"),
    path('<slug:slug>/',views.pages,name="pages"),
    
]