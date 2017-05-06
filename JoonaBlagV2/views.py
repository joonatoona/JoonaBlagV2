from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Post, File
from .utils import gen_filename
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    return render(request, "JoonaBlagV2/index.html", {'posts': Post.objects.order_by('-date')[:10]});


def get_post(request, post_id):
    req_post = get_object_or_404(Post, pk=post_id)
    return render(request, "JoonaBlagV2/post.html", {'post': req_post});

@login_required
@permission_required('JoonaBlagV2.can_post', raise_exception=True)
def upload(request):
    if request.POST:
        p = Post.objects.create_post(request.POST['title'], request.user.username, request.POST['content'], request.user.id);
        p.save();
        return HttpResponseRedirect(reverse('post', args=[p.pk]))
    return render(request, "JoonaBlagV2/upload.html")

def do_login(request):
    if (request.user.is_authenticated):
        return HttpResponseRedirect(reverse('index'));
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password']);
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'));
        return HttpResponseRedirect(reverse('login', kwargs={'fail':1}));
    return render(request, "JoonaBlagV2/login.html", {'fail':request.GET.get('fail', False),'next':request.GET.get('next')});

def do_logout(request):
    logout(request);
    return HttpResponseRedirect(reverse('login'))

@login_required
@permission_required('JoonaBlagV2.can_upload', raise_exception=True)
def file_upload(request):
    if request.POST:
        p = File(author=request.user.username, owner=request.user.id, filename=gen_filename(request.FILES['upload']), content=request.FILES['upload'], mime=request.FILES['upload'].content_type)
        p.save()
        return HttpResponseRedirect(reverse('file', args=[p.author, p.filename]))
    return render(request, "JoonaBlagV2/file.html")

def get_file(request, username, filename):
    req_file = get_object_or_404(File, author=username, filename=filename)
    return HttpResponse(req_file.content, content_type=req_file.mime)