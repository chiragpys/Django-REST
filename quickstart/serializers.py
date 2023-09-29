from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Snippet

"""<------------------------------Serializer---------------------------------------->"""
# class SnippetSerializer(serializers.Serializer):
#     '''
#     THis is Serializer.
#     '''
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#
#     def create(self, validated_data):
#         '''
#         Create and return a new `Snippet` instance, given the validated data.
#         '''
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         '''
#         Update and return an existing `Snippet` instance, given the validated data.
#         '''
#
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.save()
#         return instance


"""<------------------------------ModelSerializer---------------------------------------->"""


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'owner']


"""<------------------------------BaseSerializer---------------------------------------->"""


class SnippetBase(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'title': instance.title,
            'code': instance.code,
        }


"""<------------------------------ListSerializer---------------------------------------->"""


class SnippetList(serializers.ListSerializer):
    def create(self, validated_data):
        snippet = [Snippet(**item) for item in validated_data]
        return Snippet.objects.bulk_create(snippet)


class SerializerList(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos']
        list_serializer_class = SnippetList


"""<------------------------------HyperlinkedModelSerializer---------------------------------------->"""


class SnippetSerializerHyperlink(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='hyperlink-list',
    )

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'url']


# User Serializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
