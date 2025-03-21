from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager

def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.title)
        slug = base_slug
        count = 1
        while Recipe.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        self.slug = slug
    super().save(*args, **kwargs)

class RecipeManager(models.Manager):
    def published(self):
        return self.filter(status="published")

    def drafts(self):
        return self.filter(status="draft")

    def by_author(self, user):
        return self.filter(author=user)


class Recipe(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    description = models.TextField()
    ingredients = models.TextField(help_text="Separate ingredients with a semicolon.")
    instructions = models.TextField(help_text="Separate steps with a new line.")
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = RecipeManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogapp:recipe_detail', 
        args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    @property
    def ingredients_list(self):
        return [ingredient.strip() for ingredient in self.ingredients.split(";")]
    
    @property
    def instructions_list(self):
        return [step.strip() for step in self.instructions.split("\n") if step.strip()]

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created' ,)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'