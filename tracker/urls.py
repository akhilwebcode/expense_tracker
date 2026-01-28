from django.urls import path
from tracker.views import index, deleteTransaction, login_page, signup, logout_page

urlpatterns = [
    path('', index, name='index'),
    path('delete/<uuid:uuid>/', deleteTransaction, name='delete'),
    path('login/', login_page, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_page, name='logout'),
]
