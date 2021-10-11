from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    pass

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        # Item must be unique for a particular list
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text