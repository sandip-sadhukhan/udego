from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from .util import unique_slug_generator
from django.db.models.signals import pre_save

# Topic model
class Topic(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
# Course Model
class Course(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    coverPic = models.ImageField(upload_to='cover_photos/', default="/cover_photos/default-cover.png")
    date = models.DateField(auto_now_add=True)
    tranding = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# subcourse Model
class SubCourse(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# blogpost
class BlogPost(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    sub_course = models.ForeignKey(SubCourse, on_delete=models.CASCADE)
    body = RichTextUploadingField(blank=True, null=True, external_plugin_resources=[('youtube', '/static/plugins/youtube_2.1.14/youtube/', 'plugin.js')])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=BlogPost)