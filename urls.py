from .import views
from django.urls import path

from .views import course, course_detail, usercertificate

urlpatterns = [

    path('', views.demo, name='demo'),
    path('LOGIN/', views.LOGIN, name='LOGIN'),
    path('REGISTRATION/', views.REGISTRATION, name='REGISTRATION'),
    path('REGISTRATION-mentor/', views.mentor_registration, name='mentor_registration'),
    path('user_reg/', views.user_reg, name='user_reg'),
    path('test/', views.test, name='test'),
    path('Home_mentor/', views.Home_mentor, name='Home_mentor'),
    path('login', views.login, name='login'),
    path('mentor-login', views.mentor_login, name='mentor_login'),
    path('logout', views.logout, name='logout'),
    path('home1/', views.home1, name='home1'),
    path('Home/', views.Home, name='Home'),
    path('courses_mentor', views.courses_mentor, name='courses_mentor'),
    path('about2/', views.about2, name='about2'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('activity/', views.activity, name='activity'),
    path('Messages/', views.Messages, name='Messages'),
    path('course/', views.course, name='course'),
    path('course/', views.course, name='course'),
    path('quiz/', views.quiz, name='quiz'),
    path('course-details/<slug:course_slug>/', views.course_details, name='course_details'),
    path('courses/', views.courses, name='courses'),
    path('reports/', views.reports, name='reports'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path('view_cart/',views.view_cart,name='view_cart'),
    path('de_cart/<int:id>/',views.de_cart,name='de_cart'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-profilementor/', views.update_profilementor, name='update_profilementor'),
    path('checkout/<slug:slug>/', views.checkout, name='checkout'),
    path('review/', views.Review, name='Review'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('search/',views.search_course,name='search_course'),
    path('payment/', views.payments, name='payments'),
    #
    path('certificate/', views.certificate, name='certificate'),


    ]
