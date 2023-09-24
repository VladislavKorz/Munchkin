from django.db import models


class MetaTag(models.Model):
	html_path = models.CharField(max_length=64)
	description = models.TextField()
	keywords = models.TextField()
	title = models.CharField(max_length=64)
	image = models.ImageField(upload_to='metatags', blank=True, null=True)
