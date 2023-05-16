from django.db import models

class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    publication_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    image_url = models.TextField()
    content = models.TextField()
    approved = models.BooleanField(default=False)
    reaction = models.ManyToManyField("Reaction", through="PostReaction", related_name="post_reactions")
    tag = models.ManyToManyField("Tag", through="PostTag", related_name="posts")
