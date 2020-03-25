from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import UserProfile
from django.template.defaultfilters import slugify



class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Updated Time')

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'parent'], name='unique_name')
        ]
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Post(BaseModel):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=150)
    text = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    CAT_CHOICE = [
        ('Basic', (
            (21, 'breakfast'),
            (22, 'lunch'),
            (23, 'supper'),
            (24, 'snack'),
            (25, 'beverages'),
            (26, 'dessert')
        )),
        ('Flavors', (
            (11, 'spicy'),
            (12, 'sour'),
            (13, 'sweet'),
            (14, 'bitter'),
            (15, 'plain')
        )),
        ('Style', (
            (31, 'foreign food'),
            (32, 'home cooking'),
            (33, 'local characteristics'),
        )),
        ('People', (
            (41, 'Baby'),
            (42, 'Teenager'),
            (43, 'Old people'),
            (44, 'All')
        )),
        ('unknown', 'Unknown'),
    ]
    categories = models.ManyToManyField('Category', choices=CAT_CHOICE, default='unknown')
    STATUS = [
        (0, 'Draft'),
        (1, 'Publish')
    ]
    status = models.IntegerField(choices=STATUS, default=0)
    cook_time = models.IntegerField(null=True, blank=True)

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


class Comment(BaseModel):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_author')
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['created_on']

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'id': self.id, 'slug': self.post.slug})


    def __str__(self):
        # return self.text[:20] + "..."
        return 'Commented {} by {}'.format(self.text[:15], self.author)


class Ingredient(models.Model):
    name = models.CharField(max_length=100, help_text='Ingredient name')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_ingredients')
    amount = models.FloatField(default=1)
    UNIT_CHOICE = [
        ('', ''),
        ('g', 'gram'),
        ('mg', 'milligram'),
        ('kg', 'kilogram'),
        ('oz', 'Oz'),
        ('ml', 'milliliter'),
        ('l', 'liters'),
        ('c', 'cups'),
        ('table', 'tablespoon'),
        ('tea', 'teaspoon'),
        ('p', 'pound')
    ]
    unit = models.CharField(max_length=5, choices=UNIT_CHOICE, default='')

    def __str__(self):
        return (self.name, self.amount, self.post.id)

    class Meta:
        verbose_name_plural = 'ingredients'
