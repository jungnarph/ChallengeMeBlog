from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Recipe
from django.db.models import Q


class RecipeListView(ListView):
    model = Recipe
    template_name = "blogapp/recipes/list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        queryset = Recipe.objects.published()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "blogapp/recipes/detail.html"
    
    def get_object(self, queryset=None):
        post = get_object_or_404(Recipe, slug=self.kwargs['slug'], 
                                 publish__year=self.kwargs['year'], 
                                 publish__month=self.kwargs['month'], 
                                 publish__day=self.kwargs['day'])
        
        # Allow authors to preview drafts
        if post.status == "draft" and post.author != self.request.user:
            raise Http404("Post not found")
        return post
