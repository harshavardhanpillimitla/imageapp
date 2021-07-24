from rest_framework import viewsets
from PIL import Image as Image_mod
from io import BytesIO
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser

from .serializers import PicshareSerializer, TagSerializer, ImageSerializer, ImageModelSerializer
from picshare.models import Post, Tag, Image
from .paginator import Pagination

class PostViewSet(viewsets.ModelViewSet):
    pagination_class = Pagination
    serializer_class = PicshareSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$tags__name']
    # filter_fields = ('category', 'in_stock')
    queryset = Post.objects.all()

class TagViewSet(viewsets.ModelViewSet):
    pagination_class = Pagination
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

class ImageAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        posts = []
        i_tags = request.data['tags']
        tags = self.tags_present_or_need_to_create(i_tags)
        for image in request.FILES.getlist('image'):
            print('ige')
            data = self.dict_obj(tags, image)
            serializer =  ImageModelSerializer(data=data)
            print(serializer.is_valid())
            if serializer.is_valid():
                obj = serializer.save()
                posts.append(obj.id)
                obj.save()
                print(obj,posts,'----------------')
            else:
                return Response({'succes':False})

        post = Post.objects.create()
        post.image.set(posts)
        post.tags.set(tags)
        post.save()

        return Response({'succes':True})

    def tags_present_or_need_to_create(self, tags):
        tags_arr = tags.split(',')
        present_tags = list(Tag.objects.filter(name__in=tags_arr).values_list('name', flat=True))
        new_tags = set(list(tags_arr)) - set(list(present_tags))
        for tag in new_tags:
            temp_tag = Tag(name=tag)
            temp_tag.save()
        return list(Tag.objects.filter(name__in=tags_arr).values_list('id',flat=True))
    
    def dict_obj(self, tags, image):
        dic = {}
        dic['tags'] = tags
        dic['image'] = image
        return dic

    def get(self, request):
        return Response({'post':'post multiple images'})

class ImageRotateView(APIView):
    def post(self, request, *args, **kwargs):
        from django.core.files.uploadedfile import InMemoryUploadedFile
        print('request',request.data, args,kwargs)
        for image_id,value in request.data.items():
            image_obj = Image.objects.get(id=int(image_id))
            print(image_obj.image.file.name)
            read_image = Image_mod.open(image_obj.image)
            rotated_img = read_image.rotate(int(value))
            img=rotated_img.save(image_obj.image.file.name)
            

        return Response({'succes':True})
    
    def get(self, request):

        return Response({'success':'you can use api to rotate image'})