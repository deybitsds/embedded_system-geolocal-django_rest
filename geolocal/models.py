from django.db import models

# Create your models here.


class Location(models.Model):

    id = models.AutoField(
            db_column='id',
            primary_key=True
            )

    latitude = models.CharField()
    longitude = models.CharField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'location'

    def __str__(self):
        return "xd"

        return {"id": id}
