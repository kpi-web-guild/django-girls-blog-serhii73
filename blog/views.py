"""Views for the blog app."""
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .forms import PostForm
from .models import Post


class ListView(View):
    """Show list posts on the page."""

    def get(self, request):
        """Render template with post list."""
        posts = Post.objects.filter(
            published_date__lte=timezone.now()
        ).order_by('-published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})


class TemplateView(View):
    """Show the full post on the page."""

    def get(self, request, pk):
        """Render template with post detail."""
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})


class EditView(View):
    """Edit post."""

    def get(self, request, pk):
        """Render template with post edit."""
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

    def post(self, request, pk):
        """Save edit post to db."""
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, 'blog/post_edit.html', {'form': form})


class CreateView(View):
    """Create new post."""

    def get(self, request):
        """Render template with post new."""
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

    def post(self, request):
        """Save new post to db."""
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, 'blog/post_edit.html', {'form': form})
