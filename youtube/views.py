from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Video, User, Subscriber, Comment
import json
from .filters import VideoFilter

# Create your views here.
def home(request):
    allVideos = Video.objects.all().order_by('?')
    try:
        subscriptions = Subscriber.objects.filter(subscribers=request.user)
    except:
        subscriptions = False
    for i in allVideos:
        if len(i.caption)>50:
            i.caption = i.caption[:50]+'...'
    return render(request, 'home.html', {
        'videos': allVideos,
        'subscriptions': subscriptions,
    })

def video(request,pk):
    user = request.user
    video = Video.objects.filter(id=pk)
    moreVideos = Video.objects.all().exclude(id=pk).order_by('?')[:10]
    getVideo = Video.objects.get(id=pk)
    views = getVideo.views + 1
    video.update(views=views)
    totalLikes = getVideo.liked_by.all().count()
    liked = False
    disliked = False
    subscribed = False
    if user in getVideo.liked_by.all():
        liked = True
    if user in getVideo.disliked_by.all():
        disliked = True
    subscriberOf = Subscriber.objects.get(channel=getVideo.channel).subscribers.all()
    subscriber = subscriberOf.count()
    if user in subscriberOf:
        subscribed = True

    try:
        subscriptions = Subscriber.objects.filter(subscribers=request.user)
    except:
        subscriptions = False
    allComments = Comment.objects.filter(video=getVideo).order_by('id')
    totalComments = allComments.count()
    for i in moreVideos:
        if len(i.caption)>40:
            i.caption = i.caption[:40]+'...'

    paginator = Paginator(allComments, 2)
    page_number = request.GET.get('page')
    allComments = paginator.get_page(page_number)
    return render(request, 'video.html', {
        'video': video,
        'moreVideos': moreVideos,
        'liked': liked,
        'disliked': disliked,
        'totalLikes': totalLikes,
        'subscriber': subscriber,
        'subscribed': subscribed,
        'allComments': allComments,
        'totalComments': totalComments,
        'subscriptions': subscriptions,
        'views': views,
    })

def search(request):
    #if request.method == 'POST':
    #    str = request.POST['str']
    #print(request.GET['caption'])
    queryset = Video.objects.all()
    filterset = VideoFilter(request.GET, queryset=queryset)
    if filterset.is_valid():
        queryset = filterset.qs

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)
    
    try:
        subscriptions = Subscriber.objects.filter(subscribers=request.user)
    except:
        subscriptions = False
    return render(request, 'search.html',{
        'result': queryset,
        'search': True,
        'caption': request.GET['caption'],
        'subscriptions': subscriptions,
    })

def channel(request, pk):
    user = request.user
    channel = User.objects.filter(id=pk)
    channel2 = User.objects.get(id=pk)
    videos = Video.objects.filter(channel=channel2).order_by('-id')

    subscribed = False
    subscriberOf = Subscriber.objects.get(channel=channel2).subscribers.all()
    subscriber = subscriberOf.count()
    if user in subscriberOf:
        subscribed = True
    
    try:
        subscriptions = Subscriber.objects.filter(subscribers=request.user)
    except:
        subscriptions = False
    for i in videos:
        if len(i.caption)>50:
            i.caption = i.caption[:50]+'...'
    return render(request, 'channel.html',{
        'channel': channel,
        'videos': videos,
        'subscriber': subscriber,
        'subscribed': subscribed,
        'subscriptions': subscriptions,
    })

@login_required(login_url='/')
def upload(request):
    channel = request.user.id
    subscriptions = Subscriber.objects.filter(subscribers=request.user)
    return render(request, 'upload.html', ({'channel': channel, 'subscriptions': subscriptions,}))

def uploadVideo(request):
    channel = request.user
    if request.method == 'POST':
        ytvid = request.POST['ytvid']#Lz6d1ZlEdPU
        caption = request.POST['caption']
        description = request.POST['description']
        Video.objects.create(youtubeVideoId=ytvid, caption=caption, description=description, channel=channel)
        return redirect('channel', channel.id)


def handleSignup(request):
    data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        username = data['username']
        pass1 = data['pass1']
        pass2 = data['pass2']
        if len(username) < 1:
            return JsonResponse({'response':'Username can\'t be empty.'})
        if ' ' in username:
            return JsonResponse({'response':'Username must contain letters, digits and @/./+/-/_ only.'})
        if pass1!=pass2:
            return JsonResponse({'response':'The two password field didn\'t match.'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'response':'This username is already taken. Please try another one.'})
        if len(pass1) < 4:
            return JsonResponse({'response':'Your password must contain at least 4 characters.'})

        myuser = User.objects.create_user(username, '', pass1)
        myuser.save()
        messages.success(request, 'Your account created successfully.')
        Subscriber.objects.create(channel=myuser)
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are Logged in.')
            return JsonResponse({'response': 'ok'})
    else:
        return HttpResponse('404 - Page Not Found')

def handleLogin(request):
    data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        username = data['username']
        password = data['pass']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now Logged in.')
            return JsonResponse({'response': 'ok'})
        else:
            return JsonResponse({'response': 'Invalid username or password, please try again'})
        
    else:
        return HttpResponse('404 - Page Not Found')


def handleLogout(request):
    logout(request)
    messages.warning(request, 'You are Logged out.')
    #return JsonResponse({'response': 'ok'})
    return redirect(request.META['HTTP_REFERER'])

def likeVideo(request, pk):
    user = request.user
    video = Video.objects.get(id=pk)
    if user not in video.liked_by.all():
        video.liked_by.add(user)
    if user in video.disliked_by.all():
        video.disliked_by.remove(user)
    return JsonResponse({'response':'ok'})

def cancelLike(request, pk):
    user = request.user
    video = Video.objects.get(id=pk)
    if user in video.liked_by.all():
        video.liked_by.remove(user)
    return JsonResponse({'response':'ok'})

def dislikeVideo(request, pk):
    user = request.user
    video = Video.objects.get(id=pk)
    if user in video.liked_by.all():
        video.liked_by.remove(user)
    if user not in video.disliked_by.all():
        video.disliked_by.add(user)
    return JsonResponse({'response':'ok'})

def cancelDislike(request, pk):
    user = request.user
    video = Video.objects.get(id=pk)
    if user in video.disliked_by.all():
        video.disliked_by.remove(user)
    return JsonResponse({'response':'ok'})

def subscribe(request, pk):
    user = request.user
    channel = User.objects.get(id=pk)
    subscribeTo = Subscriber.objects.get(channel=channel)
    if user in subscribeTo.subscribers.all():
        subscribeTo.subscribers.remove(user)
        return JsonResponse({'response': 'unSubscribed'})
    
    subscribeTo.subscribers.add(user)
    return JsonResponse({'response':'ok'})

def comment(request, pk):
    user = request.user
    video = Video.objects.get(id=pk)
    data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        body = data['comment']
        Comment.objects.create(video=video, body=body, user=user)
        return JsonResponse({'response':'ok', 'username': user.username, 'comment': body})
    else:
        return HttpResponse('404 - Page Not Found')

def moreComments(request, pk):
    data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        page_number = int(data['pageNumber'])
    video = Video.objects.get(id=pk)
    comments = Comment.objects.filter(video=video)[page_number*2:page_number*2+2]
    moreComments = list(comments.values())
    for i in moreComments:
        i['username'] = User.objects.get(id=i['user_id']).username
    hasMoreComments = True
    if len(Comment.objects.filter(video=video)[page_number*2+2:page_number*2+4])==0:
        hasMoreComments = False
    return JsonResponse({'response': 'ok', 'comments': moreComments, 'hasMoreComments': hasMoreComments})
    