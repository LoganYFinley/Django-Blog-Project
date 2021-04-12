from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    # links author to site superuser
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length = 256)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)

    # sets published date and time
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # filters comments that have been approved
    def approve_comments(self):
        return self.comments.filter(approved_comment = True)
    
    # after publication takes you to details page for primary key of post just created
    # django specifically looks for 'get_absolute_url'
    def get_absolute_url(self):
        return reverse('post_detail', kwargs = {'pk':self.pk})

    # returns post title when printed
    def __str__(self):
        return self.title


class Comment(models.Model):
    # connects each comments to a post
    post = models.ForeignKey('blog.Post', related_name = 'comments', on_delete = models.CASCADE)
    author = models.CharField(max_length = 256)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    # needs to match filtered var in Post/approve_comments above
    approved_comment = models.BooleanField(default = False)

    # sets comment to be approved
    def approve(self):
        self.approved_comment = True
        self.save()

    # returns to main posts list page after approving comment
    # django specifically looks for 'get_absolute_url'
    def get_absolute_url(self):
        return reverse('post_list')
    
    # return comment text when printed
    def __str__(self):
        return self.text
