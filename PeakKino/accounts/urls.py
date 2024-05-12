from django.urls import path
from .views import CustomLoginView, logout_view, register, approve_accounts, approve_account

app_name="accounts"
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register, name='register'),
    path('approve_accounts/', approve_accounts, name='approve_accounts'),
    path('approve_account/<int:id>/', approve_account, name='approve_account'),
]