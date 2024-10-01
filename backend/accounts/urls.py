from django.urls import path
from .views import HomePageView, SignUpView, Login, Logout, Done, SendOtp, Check, Password_reset, archive_note_view, archive_page_view, unarchive_note_view, trash_note, trash_page_view, delete_note_permanently, untrash_note, save_note, search_function

app_name = 'accounts'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('done/', Done.as_view(), name='done'),
    path('send_otp/', SendOtp.as_view(), name='send_otp'),
    path('otp_check/', Check.as_view(), name='otp_check'),
    path('change_password/', Password_reset.as_view(), name='change_password'),
    path('archive/<int:pk>', archive_note_view, name = 'archive'),
    path('archives/', archive_page_view, name = 'archive_page'),
    path('unarchive/<int:pk>', unarchive_note_view, name = 'unarchive'),
    path('trash/<int:pk>', trash_note, name = 'trash'),
    path('trash/', trash_page_view, name='trash_page'),
    path('trash/<int:pk>', delete_note_permanently, name = 'delete'),
    path('untrash/<int:pk>',untrash_note, name='untrash'),
    path('save/', save_note , name='save'),
    path('search/', search_function, name='search'),
]