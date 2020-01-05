from rest_framework import serializers

from django.contrib.auth import get_user_model
UserModel = get_user_model()

from pages.models import BlogPost

    ## serializer does two things.
    # - convert to JSON
    # - validations for data passwd

class BlogPostSerializer(serializers.ModelSerializer): # forms.ModelForm
    url    = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
            ]
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get("request")
        #print(request.user)
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used.")
        return value


# DRF 3 allow override create method in serializers:

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    class Meta:
       model = UserModel
       fields = ('password', 'username', 'first_name', 'last_name',)
       # extra_kwargs = {
       #     'password': {write_only}: True
       # }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
              user.set_password(validated_data['password'])
              user.save()
        return user
