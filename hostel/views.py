from django.contrib.auth import authenticate, login
import datetime
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from .forms import ProfileForm, MarkscardForm, UserForm,VoteForm
from .models import Profile,Marks_card,Vote
from twilio.rest import Client
from django.contrib import messages

MARKS_CARD_FILE_TYPES = ['jpg', 'pdf'] #audio-marks_card
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
class a():

    def message(self,number):
        account_sid = "AC212451a1549921604f20696e75ef11e2"
        auth_token  = "1e2a798cb6a4db62cbad5bb13cd8994a"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+919019494616", 
            from_="+18582643742",
            body="\n number of students coming are: "+number)
        


def create_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'hostel/login.html')
    else:
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.photo = request.FILES['photo']
            file_type = profile.photo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'profile': profile,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'hostel/create_profile.html', context)
            profile.save()  
            return render(request, 'hostel/detail.html', {'profile': profile})
        context = {
            "form": form,
        }
        return render(request, 'hostel/create_profile.html', context)


def create_file(request, profile_id):
    form = MarkscardForm(request.POST or None, request.FILES or None)
    profile = get_object_or_404(Profile, pk=profile_id)
    if form.is_valid():
        files = profile.marks_card_set.all()                         #albums_songs=files
        for s in files:
            if s.semester == form.cleaned_data.get("semester"):
                context = {
                    'profile': profile,
                    'form': form,
                    'error_message': 'You already added that file',
                }
                return render(request, 'hostel/create_file.html', context)
        file = form.save(commit=False)
        file.profile = profile
        file.marks_card = request.FILES['marks_card']
        file_type = file.marks_card.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in MARKS_CARD_FILE_TYPES:
            context = {
                'profile': profile,
                'form': form,
                'error_message': 'Marks Card  must be PDF or JPG',
            }
            return render(request, 'hostel/create_file.html', context)

        file.save()
        return render(request, 'hostel/detail.html', {'profile': profile})
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'hostel/create_file.html', context)


#def delete_album(request, album_id):
 #   album = Album.objects.get(pk=album_id)
  #  album.delete()
   # albums = Album.objects.filter(user=request.user)
    #return render(request, 'music/index.html', {'albums': albums})


def delete_file(request, profile_id, file_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    file = Marks_card.objects.get(pk=file_id)
    file.delete()
    return render(request, 'hostel/detail.html', {'profile': profile})


def detail(request, profile_id):
    if not request.user.is_authenticated():
        return render(request, 'hostel/login.html')
    else:
        user = request.user
        profile = get_object_or_404(Profile, pk=profile_id)
        return render(request, 'hostel/detail.html', {'profile': profile, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'hostel/login.html')
    else:
        profiles = Profile.objects.filter(user=request.user)
        file_results = Marks_card.objects.all()
        query = request.GET.get("q")
        if query:
            profiles = profiles.filter(
                Q(college__icontains=query) |
                Q(name__icontains=query)
            ).distinct()
            file_results = file_results.filter(
                Q(semester__icontains=query)
            ).distinct()
            return render(request, 'hostel/index.html', {'profiles': profiles,'files': file_results,})
        else:
            return render(request, 'hostel/index.html', {'profiles': profiles})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'hostel/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profiles = Profile.objects.filter(user=request.user)
                return render(request, 'hostel/index.html', {'profiles': profiles})
            else:
                return render(request, 'hostel/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'hostel/login.html', {'error_message': 'Invalid login'})
    return render(request, 'hostel/login.html')

def files(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'hostel/login.html')
    else:
        try:
            file_ids = []
            for profile in Profile.objects.filter(user=request.user):
                for file in profile.marks_card_set.all():
                    file_ids.append(file.pk)
            users_files = Marks_card.objects.filter(pk__in=file_ids)
            if filter_by == 'favorites':
                users_files = users_files.filter(is_favorite=True)
        except Profile.DoesNotExist:
            users_files = []
        return render(request, 'hostel/files.html', {
            'file_list': users_files,
            'filter_by': filter_by,
        })
def about(request):
    
    return render(request,'hostel/about.html')


def studentlist(request):
    members=Profile.objects.filter(answer=True)
    print(members)
    
    return render(request,'hostel/studentlist.html',{'members':members})


def vote(request,profile_id):
    if not request.user.is_authenticated():
            return render(request, 'hostel/login.html')
    instance=get_object_or_404(Profile,pk=profile_id)
    print(instance)
    if request.method=="POST":
        form = VoteForm(request.POST or None)
        if form.is_valid():
            instance.answer = form.cleaned_data['answer']
            instance.save()
            messages.success(request,"You have successfully filled the form .Thank you")
            return render(request, 'hostel/about.html',{})
        else:
            return render(request,'hostel/index.html',{})
    else:
        
        today=datetime.date.today()
        tomorrow=datetime.date.today() + datetime.timedelta(days=1)
        ct=datetime.datetime.now()
        time=("{:%H:%M}".format(ct))
        day=datetime.datetime.today().weekday()
        hour=datetime.datetime.now().hour
        if(day is not 6):
            if(hour>6 & hour<19):
                date=today
                type1='Dinner'
            if(hour>19 & hour<22):
                date=tomorrow
                type1='Breakfast'

        if(day is 6):
            if(hour>6 & hour<10):
                date=today
                type1='Lunch'
            if(hour>13 & hour<22):
                date=tomorrow
                type1='Breakfast'
        

        user=request.user
        form=VoteForm(request.POST )
        context={
            "form":form,
            "user":user,
            "date":date,
            "time":time,
            "type1":type1
            }
        return render(request,'hostel/vote.html',context)
  #  b=a()
   # b.message()
def messageinfo(request):

    today=datetime.date.today()
    tomorrow=datetime.date.today() + datetime.timedelta(days=1)
    ct=datetime.datetime.now()
    time=("{:%H:%M}".format(ct))
    day=datetime.datetime.today().weekday()
    hour=datetime.datetime.now().hour
    members=Profile.objects.filter(answer=True)
    k=0
    for p in members:
        k=k+1
    messageinfo=str(k)    
    b=a()
    b.message(messageinfo)
    return render(request,'hostel/about.html')

    # if(day is not 6):

    #     if(hour==17):

    #         b=a()
    #         b.message(k)
    #     if(hour==22):
    #         b=a()
    #         b.message(k)

    # if(day is 6):

    #     if(hour==10):
    #         b=a()
    #         b.message(k)
    #     if(hour==22):
    #         b=a()
    #         b.message(k)  

