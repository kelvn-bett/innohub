from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
# from PIL import Image

# Create your models here.
'''
class Roles(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 120)

    def __str__(self):
        return "%s %s" % (self.role_name, self.description)
'''


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    category = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=12)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self):
    #     super().save()
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, created, **kwargs):
        instance.profile.save()


class Ideas(models.Model):
    idea = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    # slug = models.SlugField(unique=True, blank=True)
    problem_statement = models.TextField(max_length=2000)
    executive_summary = models.TextField(max_length=2000)
    objectives = models.TextField(max_length=2000)
    limitations = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='idea_likes')
    # dislikes = models.IntegerField(default = 0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('strathideasapp:idea_detail', kwargs={'pk': self.pk})

    def get_like_url(self):
        return reverse('strathideasapp:idea_like', kwargs={'pk': self.pk})

    def get_api_like_url(self):
        return reverse('strathideasapp:idea_like_api', kwargs={'pk': self.pk})


class Incubator(models.Model):
    incubator = models.AutoField(primary_key = True)
    incubator_name = models.CharField(max_length = 30)
    idea = models.ForeignKey(Ideas, on_delete= models.CASCADE)
    incubator_description = models.CharField(max_length = 120)
    incubator_expertise = models.CharField(max_length = 100)
    user = models.ForeignKey(Profile, on_delete = models.CASCADE)

    def __str__(self):
        return self.incubator_name


class Industry_category(models.Model):
    industry_category_id = models.AutoField(primary_key = True)
    idea = models.ForeignKey(Ideas, on_delete= models.CASCADE)
    industry_category_name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 100)


class Incubatees(models.Model):
    incubator = models.ForeignKey(Incubator,on_delete = models.CASCADE)
    idea = models.OneToOneField(Ideas, on_delete = models.CASCADE)

    def __str__(self):
        return self.idea


class Company(models.Model):
    company = models.AutoField(primary_key = True)
    company_name = models.CharField(max_length = 40)
    industry = models.ForeignKey(Industry_category, on_delete = models.CASCADE)
    description = models.CharField(max_length = 120)
    interested_department = models.CharField(max_length = 40)

    def __str__(self):
        return self.company_name


class Comments(models.Model):
    comment = models.AutoField(primary_key = True)
    user = models.ForeignKey(Profile, on_delete = models.CASCADE)
    idea = models.ForeignKey(Ideas, on_delete = models.CASCADE)
    name = models.CharField(max_length=80)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.name


class Industry_committee(models.Model):
    committee = models.AutoField(primary_key=True)
    committee_name = models.CharField(max_length=30)
    industry = models.OneToOneField(Industry_category, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)

    def __str__(self):
        return self.committee_name


# class ThumbsSignal(models.Model):
#     signal = models.AutoField(primary_key=True)
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     idea = models.ForeignKey(Ideas, on_delete=models.CASCADE)
#     #thumbs_up = models.BooleanField(default = False)
#     #thumbs_down = models.BooleanField(default = False)
#     value = models.IntegerField()
#     date = models.DateTimeField(auto_now=True)


class OpinionPolls(models.Model):
    idea = models.ForeignKey(Ideas, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.OneToOneField(Comments, on_delete=models.CASCADE)
    # signal = models.OneToOneField(Ideation, on_delete=models.CASCADE)
    comment_reply = models.CharField(max_length=200)
    def __str__(self):
        return self.comment


class Industry_request_category(models.Model):
    industry_request_cat = models.AutoField(primary_key = True)
    industry_request_cat_name = models.CharField(max_length = 30)


class Industry_request(models.Model):
    industry_request = models.AutoField(primary_key = True)
    industry_request_cat = models.ForeignKey(Industry_request_category, on_delete = models.CASCADE)
    user = models.ForeignKey(Profile, on_delete = models.CASCADE)
    industry = models.ForeignKey(Industry_category, on_delete = models.CASCADE)
    cost = models.IntegerField()
    description = models.TextField()
    duration = models.IntegerField()
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.industry_request_cat
