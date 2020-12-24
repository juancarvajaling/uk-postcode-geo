from django.db import models


class Postcode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    eastings = models.IntegerField(null=True, blank=True)
    northings = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=60, blank=True)
    nhs_ha = models.CharField(max_length=60, blank=True)
    european_electoral_region = models.CharField(max_length=60, blank=True)
    primary_care_trust = models.CharField(max_length=60, blank=True)
    region = models.CharField(max_length=60, blank=True)
    lsoa = models.CharField(max_length=60, blank=True)
    msoa = models.CharField(max_length=60, blank=True)
    incode = models.CharField(max_length=60, blank=True)
    outcode = models.CharField(max_length=60, blank=True)
    parliamentary_constituency = models.CharField(max_length=60, blank=True)
    admin_district = models.CharField(max_length=60, blank=True)
    parish = models.CharField(max_length=60, blank=True)
    admin_county = models.CharField(max_length=60, blank=True)
    admin_ward = models.CharField(max_length=60, blank=True)
    ced = models.CharField(max_length=60, blank=True)
    ccg = models.CharField(max_length=60, blank=True)
    nuts = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.code


class Coordinate(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    postcodes = models.ManyToManyField(
        to=Postcode, related_name='postcodes', blank=True
    )

    def __str__(self):
        return f'{self.lat} - {self.lon}'
