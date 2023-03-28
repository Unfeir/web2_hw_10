from django.db import models


# Create your models here.

class Author(models.Model):
    fullname = models.CharField(max_length=100, null=False)
    born_date = models.DateField()
    born_location = models.CharField(max_length=3000, default='No data')
    description = models.CharField(max_length=10000, default='No data')

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    # def __str__(self):
    #     return f"{self.name}"


class Note(models.Model):
    text = models.CharField(max_length=2000, null=False)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"
