from django_filters.rest_framework import FilterSet

from picshare.models import Post

class PostFilterSet(FilterSet):
    class Meta:
        model = Post
        fields = ('tags',)