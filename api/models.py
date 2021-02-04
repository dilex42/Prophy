from django.db import models

# Create your models here.

class TextDoc(models.Model):
    text = models.TextField()
    uploader = models.CharField(max_length=80,blank=True, default='')
    description = models.CharField(max_length=240)
    keyphrases = models.ManyToManyField("Keyphrases")


class Keyphrases(models.Model):
    phrase = models.CharField(max_length=40)
    wiki_title = models.CharField(max_length=200,blank=True,default='')
    wiki_url = models.URLField(blank=True,null=True)
    wiki_dis = models.BooleanField(blank=True,null=True)

