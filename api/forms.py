from rest_framework import serializers
from api import models
from jsonfield import JSONField
from rest_framework.authentication import authenticate
class DeveloperProfileForm(serializers.ModelSerializer):
    class Meta:
        model = models.DeveloperProfile
        fields = ('id', 'email', 'name', 'organisation', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                }
            }
        }
    
    def create(self, validated_data):
        developer_identity = models.DeveloperProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            organisation = validated_data['organisation'],
            password = validated_data['password']
        )
        return developer_identity

class AccessTokenForm(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace = False
    )

    def validate(self, args):
        email = args.get('email')
        password = args.get('password')

        developer = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        
        if not developer:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code = 'authorization')

        args['user'] = developer
        args['is_staff'] = developer.is_staff  
        return args

class PCOSForm(serializers.ModelSerializer):
    class Meta:
        model = models.PCOSModel
        fields = ('id', 'developer_profile', "age", "Chin", "Cheeks", "Lips", "Breast", "Arms", "Thigh", "Exercise", "Eat", "PCOS", "BMI", "Weight", "Period", "Concieve", "Skin", "Hairthin", "Patch", "Tired", "Mood", "Can", "City", "timing","report")
        read_only_fields = ('developer_profile','report')
        """ extra_kwargs = {
            'report': {
                JSONField({}): True,
            }
        }
        """
# class ImageReportForm(serializers.ModelSerializer):
#     class Meta:
#         model = models.ImageReportModel
#         fields = ('id', 'developer_profile', 'url', 'parsed_image', 'timing','report')
#         read_only_fields = ('developer_profile','report', 'url')

# class VideoReportForm(serializers.ModelSerializer):
#     class Meta:
#         model = models.VideoReportModel
#         fields = ('id', 'developer_profile', 'url', 'parsed_video', 'timing','report')
#         read_only_fields = ('developer_profile','report', 'url')
     