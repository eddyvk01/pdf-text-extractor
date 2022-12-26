from django.db import models

class Text(models.Model):
    text = models.TextField()
    pdf_file = models.FileField()


