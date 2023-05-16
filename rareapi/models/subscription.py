from django.db import models

class Subscription(models.Model):
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscriptions")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscribers")
    created_on = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=True)
    ended_on = models.DateField(null=True, blank=True, auto_now=False)
