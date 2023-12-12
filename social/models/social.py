from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# create message
class Message(models.Model):
    user = models.ForeignKey(User, related_name="message", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="twitter_likes", blank=True)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def number_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"<p class='fw-bold d-inline'>{self.user}</p>"
            f"<small class='text-muted'> @{str(self.user).lower()} &#183; </small>"
            f"<small class='text-muted'>({self.created_at:%Y-%m-%d %H:%M})</small>"
            f"<br/>{self.body}..."
        )


# create a User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    date = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to="images/profile/"
    )
    background_image = models.ImageField(
        null=True, blank=True, upload_to="images/background/"
    )
    profile_bio = models.CharField(null=True, blank=True, max_length=160)
    profile_location = models.CharField(null=True, blank=True, max_length=30)
    profile_website = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)
