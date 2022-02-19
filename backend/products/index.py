from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register


from .models import Product


@register(Product)
class ProductIndex(AlgoliaIndex):
    # should_index = 'is_public'
    fields = [
        'title',
        'content',
        'price',
        'user',
        'public'
    ]
    settings = {
        'searchableAttributes': ['title', 'content'],
        'attributesForFaceting': ['user', 'public']
    }
    tags = 'get_tags_list'
