from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView,
    CreateView, UpdateView, 
    DetailView, DeleteView,
    )

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    # grabs posts with published dates less than or equal to current time and order them in decending order (newest first)
    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(CreateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = '/blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = '/blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


#######################################
## Functions that require a pk match ##
#######################################


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            # definined in blog/models.py/Comment
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    # definined in blog/models.py/Comment
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    # save pk of comment before deletion
    post_pk = comment.post.pk
    # definined in blog/models.py/Comment
    comment.delete()
    return redirect('post_detail', pk = post_pk)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    # definined in blog/models.py/Post
    post.publish()
    return redirect('post_detail', pk = pk)

