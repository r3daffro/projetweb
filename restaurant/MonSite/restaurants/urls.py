from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('rate/<int:restaurant_id>/', views.rate_restaurant, name='rate_restaurant'),
    path('login/', views.login_view, name='login'),
    path('sign_up/', views.signup, name='sign_up'),
    path('logout/', views.log_out, name='logout'),
    path('submit_rating/', views.submit_rating, name='submitrating'),
    
    #path('homepage/', views.show_homepage, name='homepage')
    # Ajoutez vos autres vues ici
]