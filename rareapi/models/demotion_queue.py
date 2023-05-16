from django.db import models

class DemotionQueue(models.Model):
    action = models.CharField(max_length=255)
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="demotions_request")
    approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="demotions_approved")
