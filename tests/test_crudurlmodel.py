from __future__ import unicode_literals

from django.test import TestCase

from .models import Region
from .models import Town


class TestTown(TestCase):

    def setUp(self):
        self.region1 = Region.objects.create(name="Tungurahua")
        self.region2 = Region.objects.create(name="Chocolatey")
        self.town1 = Town.objects.create(name="Cuenca", region=self.region1)
        self.town2 = Town.objects.create(name="Baños de agua santa",
            region=self.region1)

    def test_list_view(self):
        self.assertEquals(Region.list_url(), '/regions')
        self.assertEquals(self.region1.list_url(), '/regions')

    def test_create_view(self):
        pass

    def test_detail_view(self):
        pass
    