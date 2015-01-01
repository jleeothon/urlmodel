

from django.db import models

from urlmodel import CrudUrlModel, ListUrlModel


class Region(CrudUrlModel, ListUrlModel, models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        verbose_name="name",
    )


class Town(CrudUrlModel, models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        verbose_name="name",
    )
    region = models.ForeignKey(Region, related_name='cities')

    def __str__(self):
        return self.name
