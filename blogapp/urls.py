from django.urls import path
from .views import RecipeListView, RecipeDetailView

app_name = "blogapp"

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
]