from blog.forms import CommentForm, PostForm, UserForm
from blog.mixins import CommentMixin, UserIsAuthorMixin
from blog.models import Category, Comment, Post, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blogicum.settings import POST_LIMIT


def get_all_posts():
    queryset = (
        Post.objects.select_related(
            "category",
            "location",
            "author",
        )
        .order_by(
            "-pub_date",
        )
        .annotate(
            comment_count=Count("comments"),
        )
    )
    return queryset


def get_all_published():
    queryset = get_all_posts().filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )
    return queryset


class PostListView(ListView):
    model = Post
    paginate_by = POST_LIMIT
    template_name = "blog/index.html"
    queryset = get_all_published()


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    data_post = None

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        self.data_post = get_object_or_404(Post, pk=pk)
        if self.data_post.author == self.request.user:
            return get_all_posts().filter(pk=pk)
        return get_all_published().filter(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.data_post.comments.select_related("author")
        return context


class PostUpdateView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"pk": self.kwargs.get("pk")}
        )


class PostDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user})


class CategoryPostsListView(PostListView):
    template_name = "blog/category.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                category__slug=self.kwargs.get("category_slug"),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs.get("category_slug"),
        )
        return context


class ProfileListView(PostListView):
    template_name = "blog/profile.html"
    author = None

    def get_queryset(self):
        self.author = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        if self.author == self.request.user:
            return get_all_posts().filter(author=self.author)
        return super().get_queryset().filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "blog/user.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            "blog:profile",
            kwargs={"username": self.request.user},
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    data_post = None

    def dispatch(self, request, *args, **kwargs):
        self.data_post = get_object_or_404(
            Post,
            pk=self.kwargs.get("pk"),
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.data_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:post_detail", kwargs={"pk": self.kwargs.get("pk")}
        )


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    pass
