import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    # profile_image = models.ImageField(upload_to="profile")
    is_active = models.BooleanField(default=True)  # Required for superusers
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # def __str__(self):
    #     return self.email

class Resume(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resume",
        primary_key=True  # Ensures it uses CustomUser's ID as the primary key
    )
    email = models.EmailField(_("email address"))
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            old_resume = Resume.objects.get(pk=self.pk)
            if old_resume.profile_image and self.profile_image != old_resume.profile_image:
                old_resume.profile_image.delete(save=False)
        except Resume.DoesNotExist:
            pass
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}'s Resume"


class Experience(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="experiences"
    )
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # Allow ongoing experiences
    description = models.TextField()
    achievements = models.JSONField(default=list)  # Store as a list of achievements

    def __str__(self):
        return f"{self.title} at {self.company}"


class Certification(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="certifications"
    )
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    date = models.DateField()
    link = models.URLField(blank=True, null=True)
    skills = models.JSONField(default=list)

    def __str__(self):
        return self.title


class Education(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="education"
    )
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year = models.CharField(max_length=4)  # e.g., "2025"
    grade = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} from {self.institution}"


class TechSkill(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="tech_skills"
    )
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField()  # Assume 1-10 scale for skill level

    def __str__(self):
        return self.name


class SoftSkill(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="soft_skills"
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255)  # Store an icon name or URL

    def __str__(self):
        return self.name


class Hobby(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="hobbies"
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=255)  # Store an icon name or URL
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class SliderGallery(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="resume_gallery/")
    # caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption

    def __str__(self):
        return f"Image for {self.resume.name}'s Resume"

