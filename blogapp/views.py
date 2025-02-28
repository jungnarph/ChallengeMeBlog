from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.db.models import Q
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_share(request, post_id):
    post = get_object_or_404(Recipe, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {request.build_absolute_uri(post.get_absolute_url())}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blogapp/recipes/share.html', {'post': post, 'form': form, 'sent': sent})

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
