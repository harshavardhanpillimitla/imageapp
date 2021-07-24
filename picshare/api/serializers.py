from rest_framework import serializers

from picshare.models import Post, Tag, Image
from rest_framework.fields import SerializerMethodField




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)



class ImageSerializer(serializers.ModelSerializer):
    image_url = SerializerMethodField()
    class Meta:
        model = Image
        fields = ('id','image_url',)
    def get_image_url(self, obj):
        print('oo')
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)

class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'tags')


class PicshareSerializer(serializers.ModelSerializer):
    image =  ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id','image','tags')
    
