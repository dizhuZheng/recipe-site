from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from recipes import documents as posts_documents


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = posts_documents.PostDocument
        fields = (
            'id',
            'title',
            'body',
            'author',
            'created',
            'modified',
            'pub_date',
        )
