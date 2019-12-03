from django.test import TestCase
from RootEBDS.apps.ams.models import AmsBaseInfo
# Create your tests here.


class AmsBaseInfoTestCase(TestCase):
    def setUp(self):
        AmsBaseInfo.objects.create(alert_id=191123758)

    def test_ams(self):
        ams = AmsBaseInfo.objects.get(alert_id=191123758)
        self.assertEqual(ams.stat_id, None)


