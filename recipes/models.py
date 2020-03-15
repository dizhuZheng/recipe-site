from django.db import models
from django.utils import timezone
from users.models import UserProfile
from django.urls import reverse
# from django.conf import settings

STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipe_posts')
    title = models.CharField(max_length=150)
    updated_on = models.DateTimeField(auto_now=True)
    text = models.TextField()
    slug = models.SlugField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',  kwargs={'slug': self.slug})


class Comment(models.Model):
    created_time = models.DateTimeField(default=timezone.now)
    approved_status = models.BooleanField(default=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    pic = UserProfile.photo
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # recipes.Post

    def approve(self):
        self.approved_status = True
        self.save()

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        # return self.text[:20] + "..."
        return 'Commented {} by {}'.format(self.text[:20], self.author)
