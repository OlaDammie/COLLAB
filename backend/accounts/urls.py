from django.urls import path
from . import views
from .views import HomePageView, SignUpView, Login, Logout, Done, SendOtp, Check

app_name = 'accounts'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('done/', Done.as_view(), name='done'),
    path('send_otp/', SendOtp.as_view(), name='send_otp'),
    path('otp_check/', Check.as_view(), name='otp_check'),
     path('index', views.index, name='index'),
    path('archive/<int:pk>', views.archive_note_view, name = 'archive'),
    path('archives/', views.archive_page_view, name = 'archive_page'),
    path('unarchive/<int:pk>', views.unarchive_note_view, name = 'unarchive'),
    path('trash/<int:pk>', views.trash_note, name = 'trash'),
    path('trash/', views.trash_page_view, name='trash_page'),
    path('trash/<int:pk>', views.delete_note_permanently, name = 'delete'),
    path('untrash/<int:pk>',views.untrash_note, name='untrash'),
    path('login/', views.login , name='login'),
    path('save/', views.save_note , name='save'),
    path('search/', views.search_function, name='search'),
    # path('change_password/', Password_reset.as_view(), name='change_password'),
]