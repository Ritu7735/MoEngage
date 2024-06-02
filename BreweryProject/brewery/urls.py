from django.urls import path
from brewery import views
from .views import homepage


urlpatterns =[
    path('',views.home),
    path('', homepage, name='home'),

    path('loginpage',views.login_page,name='loginpage'),
    path('loginuser',views.login_user,name='loginuser'),
    path('signuppage',views.signup_page,name='signuppage'),
    path('signupuser',views.signup_user),
    path('gotohome',views.go_to_home,name='gotohome'),
    path('add_review', views.add_review, name='addreview'),
    path('brewery_detail', views.brewery_detail, name='brewery_detail'),
    path('search_results', views.search_results, name='search_results'),

]