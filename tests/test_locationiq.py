import unittest
from locationiq.geocoder import LocationIq
from locationiq.geocoder import LocationIqNoPlacesFound, LocationIqInvalidKey, LocationIqInvalidRequest
from locationiq.geocoder import LocationIqRequestLimitExeceeded, LocationIqServerError

class LocationIqTestCase(unittest.TestCase):
    def test_no_api_key(self):
        with self.assertRaises(LocationIqInvalidKey):
            liq = LocationIq("locationiq-key")
            liq.geocode("Lingampally, Hyderabad")


if __name__ == "__main__":
    unittest.main()