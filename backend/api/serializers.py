from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Resume, Experience, Certification, Education, TechSkill, SoftSkill, Hobby, SliderGallery
# from .models import Note

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        Resume.objects.create(user=user, email=user.email)
        return user

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        read_only_fields = ('resume',)

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        read_only_fields = ('resume',)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        read_only_fields = ('resume',)

class TechSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechSkill
        read_only_fields = ('resume',)

class SoftSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        read_only_fields = ('resume',)

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        read_only_fields = ('resume',)

class SliderGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderGallery
        read_only_fields = ('resume',)


class ResumeSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(use_url=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    education = EducationSerializer(many=True, required=False)
    tech_skills = TechSkillSerializer(many=True, required=False)
    soft_skills = SoftSkillSerializer(many=True, required=False)
    hobbies = HobbySerializer(many=True, required=False)
    slider_gallery = SliderGallerySerializer(many=True, required=False)


    def create(self, validated_data):
        # Handle nested data
        experiences_data = validated_data.pop('experiences')
        certifications_data = validated_data.pop('certifications', [])
        education_data = validated_data.pop('education', [])
        tech_skills_data = validated_data.pop('tech_skills', [])
        soft_skills_data = validated_data.pop('soft_skills', [])
        hobbies_data = validated_data.pop('hobbies', [])
        sliderGallery_data = validated_data.pop("slider_gallery", [])

        print("Validated Data:", validated_data)

        resume = Resume.objects.create(**validated_data)

        for experience in experiences_data:
            Experience.objects.create(resume=resume, **experience)

        for cert_data in certifications_data:
            Certification.objects.create(resume=resume, **cert_data)

        for edu_data in education_data:
            Education.objects.create(resume=resume, **edu_data)

        for skill_data in tech_skills_data:
            TechSkill.objects.create(resume=resume, **skill_data)

        for skill_data in soft_skills_data:
            SoftSkill.objects.create(resume=resume, **skill_data)

        for hobby_data in hobbies_data:
            Hobby.objects.create(resume=resume, **hobby_data)

        for gallery_item in sliderGallery_data:
            SliderGallery.objects.create(resume=resume, **gallery_item)
      
        return resume

    def update(self, instance, validated_data):
        # Update nested data
        experiences_data = validated_data.pop('experiences', [])
        certifications_data = validated_data.pop('certifications', [])
        education_data = validated_data.pop('education', [])
        tech_skills_data = validated_data.pop('tech_skills', [])
        soft_skills_data = validated_data.pop('soft_skills', [])
        hobbies_data = validated_data.pop('hobbies', [])
        sliderGallery_data = validated_data.pop("slider_gallery", [])


        # Update Resume fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related models
        instance.experiences.all().delete()
        for exp_data in experiences_data:
            Experience.objects.create(resume=instance, **exp_data)

        instance.certifications.all().delete()
        for cert_data in certifications_data:
            Certification.objects.create(resume=instance, **cert_data)

        instance.education.all().delete()
        for edu_data in education_data:
            Education.objects.create(resume=instance, **edu_data)

        instance.tech_skills.all().delete()
        for skill_data in tech_skills_data:
            TechSkill.objects.create(resume=instance, **skill_data)

        instance.soft_skills.all().delete()
        for skill_data in soft_skills_data:
            SoftSkill.objects.create(resume=instance, **skill_data)

        instance.hobbies.all().delete()
        for hobby_data in hobbies_data:
            Hobby.objects.create(resume=instance, **hobby_data)

        instance.gallery.all().delete()  # Remove old gallery images
        for gallery_item in sliderGallery_data:
            SliderGallery.objects.create(resume=instance, **gallery_item)

        return instance

    class Meta:
        model = Resume
        fields = (
            "user_id",
            "name",
            "title",
            "bio",
            "profile_image",
            "experiences",
            'certifications',
            'education',
            'tech_skills',
            'soft_skills',
            'hobbies',
            'slider_gallery',
        )