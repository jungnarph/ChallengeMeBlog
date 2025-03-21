from django.http import Http404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment
from django.db.models import Q
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def post_share(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{cd['name']} recommends you read {recipe.title}"
            message = f"Read {recipe.title} at {request.build_absolute_uri(recipe.get_absolute_url())}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blogapp/recipes/share.html', {'recipe': recipe, 'form': form, 'sent': sent})

def post_detail(request, year, month, day, post):
    recipe = get_object_or_404(Recipe, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = recipe.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.save()
            messages.success(request, "Your comment has been added successfully!")  # Add success message

            return redirect(request.path)
    
    return render(request, 'blogapp/recipes/detail.html', {
        'recipe': recipe,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form})

class RecipeListView(ListView):
    model = Recipe
    template_name = "blogapp/recipes/list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        queryset = Recipe.objects.published()
        query = self.request.GET.get("q")

        if query:
            search_query = SearchQuery(query)
            search_vector = (
                SearchVector("title", weight="A") +
                SearchVector("description", weight="B")
            )
            queryset = queryset.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gt=0).order_by("-rank")  # Filter and sort by rank

        return queryset

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "blogapp/recipes/detail.html"
    
    def get_object(self, queryset=None):
        post = get_object_or_404(Recipe, slug=self.kwargs['slug'], 
                                 publish__year=self.kwargs['year'], 
                                 publish__month=self.kwargs['month'], 
                                 publish__day=self.kwargs['day'])

        if post.status == "draft" and post.author != self.request.user:
            raise Http404("Post not found")
        return post
