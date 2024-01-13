from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


class AdCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name.title()


class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(AdCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title.title()


class Response(models.Model):
    text = models.TextField()
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PrivatePage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PrivateResponse(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    private_page = models.ForeignKey(PrivatePage, on_delete=models.CASCADE)


class Newsletter(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    users = models.ManyToManyField(User)

