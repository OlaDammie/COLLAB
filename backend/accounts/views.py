from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utility import generate_otp
from django.core.mail import send_mail
from django.core.cache import cache
from .models import Note
from . forms import AddNote
from django.db.models import Q


# Create your views here.
class HomePageView(View):
    template_name = 'accounts/home.html'

    def get(self, request):

        return render(request, self.template_name)
    
class SignUpView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
       
        if User.objects.filter(email=email).exists():
            return redirect('accounts:signup')
        elif password != confirm_password:
            return redirect('accounts:signup')
        else:
            request.session['username'] = username #this place might not be needed
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('accounts:login')

class Login(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}, enter your notes")
            return redirect('accounts:home')
        else:
            return redirect('accounts:login')
        
class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('accounts:home')

class SendOtp(View):
    template_name = 'accounts/send_otp.html'

    def get(self, request):
        otp = generate_otp()
        request.session['otp'] = otp
        context = {
            'otp': otp
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        email_address = request.POST['email_address']
        request.session['email_address'] = email_address
        user = User.objects.get(email=email_address)

        cache.set(f'otp_{email_address}', request.session['otp'], 300)

        body = f"the otp >> {request.session['otp']} and incase you forgot, your username is {user.username}"
        send_mail(
            'Password reset',
            body,
            from_email='preciousakpe266@gmail.com',
            recipient_list=[email_address]
        )

        return redirect('accounts:otp_check')
    
class Done(View):
    template_name = 'accounts/done_send.html'

    def get(self, request):
        return render(request, self.template_name)
    
class Check(View):
    template_name = 'accounts/check.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST['email']
        otp_checker = request.POST['otp_checker']

        cached_otp = cache.get(f'otp_{email}')
        
        if cached_otp and otp_checker == cached_otp:
            # valid otp
            return redirect('accounts:login')
        else:
            return redirect('accounts:otp_check')
        


def search_function(request):
    q = request.GET.get('q', '')  # Get 'q' from request.GET, default to an empty string if not present
    if q != '':
        multiple_q = Q(Q(title__icontains=q) | Q(body__icontains=q))
        notes = Note.objects.filter(multiple_q)
    else:
        notes = Note.objects.filter(archive=False, trash=False)
    return render(request, 'search_results.html', {'notes': notes, 'query': q})


def index(request):
   
    notes = Note.objects.filter(archive=False, trash=False)
    form = AddNote(request.POST or None)
    return render(request, 'index.html', {'notes': notes, 'form': form})


def save_note(request):
    form = AddNote(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
                form.save()
                return redirect('notesapp:index')
    
    else:
        messages.error(request, 'You must be logged in to add a record')
        return redirect('notesapp:index')
    # return render(request, 'index.html', {'form': form})



# Archive a specific note
def archive_note_view(request, pk):
    notes = get_object_or_404(Note, id=pk)
    notes.archive = True
    notes.save()
    messages.success(request, 'note archived')
    return redirect('notesapp:archive_page')

#displaying the archive page
def archive_page_view(request):
    archived_notes = Note.objects.filter(archive=True, trash=False)
    
    return render(request, 'archive.html', {'notes': archived_notes})

#unarchive fuctionality   
def unarchive_note_view(request, pk):
    note = get_object_or_404(Note, id=pk)
    note.archive = False
    note.save()
    messages.success(request, 'note unarchived')
    return redirect('notesapp:index')  # Redirect to the archive page

#trash fuctionality   
def trash_note(request, pk):
    note = Note.objects.get(id=pk)
    note.trash = True
    note.save()
    messages.success(request, 'note sent to trash')
    return redirect('notesapp:trash_page') 

def untrash_note(request, pk):
    note = Note.objects.get(id=pk)
    note.trash = False
    note.save()
    messages.success(request, 'note restored from Trash')
    return redirect('notesapp:index') 

#trash page view
def trash_page_view(request):
    trash_note = Note.objects.filter(trash=True, archive=False)
    return render(request, 'trash.html', {'notes':trash_note})


def delete_note_permanently(request, pk):
    if request.method == 'POST':
        delete_it = Note.objects.get(id=pk)
        delete_it.delete()
        return redirect('notesapp:index')
    

