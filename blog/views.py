from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
# Create your views here.
'''
def post_list(request):
    posts = Post.published.all()
    return render(request,
    'blog/post/list.html',
    {'posts': posts})
'''
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment object but dont save  to database yet
            new_comment = comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                    'blog/post/detail.html',
                    {'post': post,
                    'comments': comments,
                    'new_comment': new_comment,
                    'comment_form': comment_form})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6) #3 post per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post/list.html',
    {'page':page, 'posts': posts, 'tag': tag })

    

def index(request):
    return(post_list(request))
'''
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'post'
    paginate_by = 3
    template_name = 'blog/post/list.html'
'''
#Чомусь не працює відображення списку постів, із новим класом.
 #Розібратися чому
def picture(request):
    return render(request, 'blog/picture.html')

'''
def post_share(request, post_id):
    post = get_object_or_404(Post,id=post_id, status='published')
    if request.method == 'POST':
        #form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
        #Form fields passed validation
            cd = form.cleaned_data
        #send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})
'''

def post_share(request, post_id):
    #retrive post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == "POST":
        #from was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_url(
                post.get_absolute_url())
            subject = f"{cd['name']} recommend you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com',
                    [cd['to']])
            sent = True
    else: 
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

'''
Evrething is ok, forms are working
I must understand how views connected with templates .html
'''


def example(request):
    return render(request, 'blog/post/example.html')