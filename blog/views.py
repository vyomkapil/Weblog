from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView
from .forms import RegistrationForm, PostForm
from .models import Post, Comment, Message
from django.utils import timezone

def index(request):
    flag = 0
    latest_post_list = Post.objects.order_by('-post_date')[:5]
    context = {'latest_post_list': latest_post_list, 'flag': flag}
    return render(request, 'blog/index.html', context)

@login_required
def allblog(request):
    flag = 1
    latest_post_list = Post.objects.order_by('-post_date')[:]
    context = {'latest_post_list': latest_post_list, 'flag': flag}
    return render(request, 'blog/index.html', context)

@login_required
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})

@login_required
def post(request):
    if request.method == 'POST':
        a = Post(user=request.user, post_date=timezone.now())
        form = PostForm(request.POST, request.FILES, instance=a)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            print form.errors

    else:
        form = PostForm()
        return render(request, 'blog/post.html', {'form': form })

@login_required
def comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    c = Comment(comment_text=request.POST['txtArea'], comment_date=timezone.now(), user=request.user, post=post)
    c.save()
    return HttpResponseRedirect(reverse('blog:detail',args=(post.id,)))

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details:{0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'blog/login.html')


class RegistrationView(FormView):
    template_name = 'blog/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('blog:index')
    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

@login_required
def search(request):
    if request.method == 'POST':
        flag = 1
        latest_post_list = Post.objects.filter(title__icontains=request.POST['find']) \
                           | Post.objects.filter(user__first_name__icontains=request.POST['find']) \
                           | Post.objects.filter(user__last_name__icontains=request.POST['find'])
        context = {'latest_post_list': latest_post_list, 'flag': flag}
        return render(request, 'blog/index.html', context)

def message(request):
    if request.method == 'POST':
        m = Message(name=request.POST['name'], email=request.POST['email'], contact=request.POST['contact'], message=request.POST['message'])
        m.save()
        return HttpResponseRedirect(reverse('blog:index'))

