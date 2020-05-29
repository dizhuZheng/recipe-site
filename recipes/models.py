from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import UserProfile
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from  django.core.validators import MinValueValidator
from .unique_slug import unique_slugify
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

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


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') # this is not a field
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Post(BaseModel):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=100)
    favorites = models.ManyToManyField(UserProfile, related_name='post_favo')
    likes = GenericRelation(LikeCount, related_query_name='posts')  # no changes detected in db
    CAT_CHOICE = [
        ('Flavors', (
            (11, 'spicy'),
            (12, 'sour'),
            (13, 'sweet'),
            (14, 'bitter'),
            (15, 'plain')
        )),
        ('Basic', (
            (21, 'breakfast'),
            (22, 'lunch'),
            (23, 'supper'),
            (24, 'snack'),
            (25, 'beverages'),
            (26, 'dessert')
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
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ["-created_on"]
        index_together = (('id', 'slug'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """returns the url to access a particular recipe access"""
        return reverse('posts:post_detail', kwargs={'slug': self.slug})

    def save(self, **kwargs):
        slug = "%s %s" % (self.author, self.title)
        unique_slugify(self, slug)
        return super(Post, self).save()


class Comment(BaseModel):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_author')
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')

    class Meta:
        ordering = ['created_on']

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'id': self.id, 'slug': self.post.slug})


    def __str__(self):
        # return self.text[:20] + "..."
        return 'Commented {} by {}'.format(self.text[:15], self.author)


class CookTime(models.Model):
    cook_time = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0, message='must be greater than 0!')])
    UNIT_CHOICE = [
        ('s', 'seconds'),
        ('m', 'minutes'),
        ('h', 'hours')
    ]
    unit = models.CharField(max_length=5, choices=UNIT_CHOICE, null=True, blank=True, default='m')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='cook_time')

    def __str__(self):
        return '{}--{}'.format(self.cook_time, self.unit)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_ingredients')
    amount = models.DecimalField(max_digits=5, decimal_places=1, help_text="eg: 2g", validators=[MinValueValidator(0.01, message='must be greater than 0.01!')])
    UNIT_CHOICE = [
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
    unit = models.CharField(max_length=5, choices=UNIT_CHOICE, null=True, blank=True)

    def __str__(self):
        return (('name:%s, amount:%d, post_id:%d')%(self.name, self.amount, self.post.id))

    class Meta:
        verbose_name_plural = 'ingredients'


class Step(models.Model):
    text = models.TextField(max_length=500, null=False, blank=False)
    pic = models.ImageField(upload_to='images/', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_steps')

    def __str__(self):
        return 'first step {} from {}'.format(self.text[:15], self.post.slug)

    class Meta:
        verbose_name_plural = 'steps'


class Foo(models.Model):
    bar = models.CharField(max_length=100)
    ratings = GenericRelation(Rating, related_query_name='foos')
