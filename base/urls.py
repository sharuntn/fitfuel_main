from django.urls import path
from .  import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('',views.homePage,name="home"),
    path('register/',views.registerPage,name="register"),
    path('scan/',views.scan,name="scan"),
    path('result/',views.result,name="result"),
    path('profile/',views.update_user,name="profile"),
    path('logout/',views.lgout,name="logout"),
    path('chatbot/',views.chat,name="chatbot"),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_compelete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]