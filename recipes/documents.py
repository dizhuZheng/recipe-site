from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post, Ingredient, Step, Comment
from recipes.models import UserProfile
from elasticsearch_dsl import analyzer

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class PostDocument(Document):
    author = fields.ObjectField(properties={
        'username': fields.TextField(analyzer=html_strip),
    })
    post_ingredients = fields.NestedField(properties={
        'name': fields.TextField(analyzer=html_strip),
        'amount': fields.DoubleField(),
        'unit': fields.TextField(),
        'pk': fields.IntegerField(),
    })
    post_steps = fields.NestedField(properties={
        'text': fields.TextField(analyzer=html_strip, fields={'raw': fields.KeywordField()}),
        'pk': fields.IntegerField(),
    })
    post_comments = fields.NestedField(properties={
        'text': fields.TextField(analyzer=html_strip),
        'pk': fields.IntegerField(),
    })

    class Index:
        name = 'posts'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
    class Django:
        model = Post
        fields = ['title', 'created_on', 'cook_time']
        related_models = [UserProfile, Ingredient, Step, Comment]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(PostDocument, self).get_queryset().select_related(
            'author'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Post instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, UserProfile):
            return related_instance.post_author.all()
        elif isinstance(related_instance, Ingredient):
            return related_instance.post
        elif isinstance(related_instance, Step):
            return related_instance.post
        elif isinstance(related_instance, Comment):
            return related_instance.post
