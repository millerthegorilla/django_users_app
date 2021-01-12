from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_init
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_statement = models.TextField(default="")

    def __str__(self):
    	return str(self._meta.get_fields(include_hidden=True))
    
@receiver(post_save, sender=User)
def set_is_active_to_false(sender, instance, created, **kwargs):
	if created:
		instance.is_active = False
		instance.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()