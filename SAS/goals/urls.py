from django.urls import path
from goals import views

app_name = 'goals'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_goal/', views.add_goal, name='add_goal'),
    path('statistics/', views.statistics, name='statistics'),

    #Ignore, this is graph testing
    path('api/data/', views.get_data, name='api_data'),
]
