from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from collections import deque
from .forms import *
from dashboard.templatetags import extras
# Create your views here.

@login_required
def index(request):
    user=request.user
    private_files=MusicFile.objects.filter(uploaded_by=user,upload_type='private')
    public_files=MusicFile.objects.filter(upload_type='public')
    protected_files_music=Access.objects.filter(user=request.user, access_type='protected').values('music_file')
    playlists=Playlist.objects.filter(byUser=user)
    protected_files=deque([])
    for pfm in protected_files_music:
        protected_files.append(MusicFile.objects.get(id=pfm['music_file']))
    context={'user': user,'private_files': private_files,'public_files': public_files,"protected_files": protected_files,'playlists': playlists}
    return render(request,'index.html',context)

def register_user(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        if username!='' and password!='' and password==password2 and email!='':
            
            if User.objects.filter(email=email).exists():
                messages.warning(request,'Email already in use. Choose another E-mail')
                return redirect('register_user')
            elif User.objects.filter(username=username).exists():
                messages.warning(request,'Username already in use. Choose another Username')
                return redirect('register_user')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                userlogin=authenticate(username=username,password=password)
                login(request,userlogin)
                return redirect('dashboard')
                
        elif username=='':
            messages.warning(request,'Enter the username')
            return redirect('register_user')
        elif email=='':
            messages.warning(request,'Enter the email ID')
            return redirect('register_user')
        
        elif password =='' or password!=password2:
            messages.warning(request,'Confirmation password did not match with the given password')
            return redirect('register_user')
    else:
        return render(request,'register_user.html')

def login_user(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.warning(request,'Invalid Credentials. Please put down correct username and password')
            return redirect('login_user')
    return render(request,'login_user.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required
def upload_file(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        file=request.FILES.get('file')
        upload_type=request.POST.get('upload_type')
        allowed_emails=request.POST.get('allowed_emails')
        uploaded_by=request.user
        music_file = MusicFile.objects.create(
            name=name,
            file=file,
            uploaded_by=uploaded_by,
            upload_type=upload_type,
            allowed_emails=allowed_emails
        )
        if upload_type=='public':
            Access.objects.create(user=request.user, music_file=music_file, access_type='public')
        elif upload_type == 'private':
            Access.objects.create(user=request.user, music_file=music_file, access_type='private')
        elif upload_type == 'protected':
            allowed_emails_list = allowed_emails.split(',')
            emails_not_registered =deque([])
            for user_email in allowed_emails_list:
                user_email=user_email.strip()
                user=User.objects.filter(email=user_email).first()
                if user is not None:
                    Access.objects.create(user=user, music_file=music_file, access_type='protected')
                else:
                    emails_not_registered.append(user_email)
                    messages.warning(request,f'These emails are not registered - {list(emails_not_registered)}. So, we could not provide them access to your protected file.')
        return redirect('dashboard')

    return render(request,'upload_file.html')

@login_required
def search(request):
    user=request.user
    if request.method == "POST":
        filename = request.POST.get("filename")
        searchedfiles = MusicFile.objects.filter(name__icontains=filename)
        context = {
            "user": user,
            "searcheduserfiles": searchedfiles,
            'filename': filename
        }
        return render(request, "search.html", context)
    else:
        return redirect("/")
    
@login_required
def create_playlist(request):
    user=request.user
    if request.method == "POST":
        form=PlaylistCreateForm(request.POST)
        if form.is_valid():
            name = form.data.get("name")
            addedfiles = form.cleaned_data.get("files")
            playlist = Playlist.objects.create(name=name, byUser=request.user)
            playlist.files.set(addedfiles)
            messages.success(request, "Playlist created successfully.")
            return redirect("dashboard")
    else:
        form=PlaylistCreateForm()
    context={'form': form,'user':user}
    return render(request, 'create_playlist.html', context)