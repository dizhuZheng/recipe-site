from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import UserProfile
from django.template.defaultfilters import slugify
# from django.conf import settings

STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipe_posts')
    title = models.CharField(max_length=150)
    updated_on = models.DateTimeField(auto_now=True)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=False, unique=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """returns the url to access a particular recipe access"""
        return reverse('posts:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


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
        return 'Commented {} by {}'.format(self.text[:15], self.author)
