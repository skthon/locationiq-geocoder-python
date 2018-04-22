import unittest
from locationiq.geocoder import LocationIQ
from locationiq.geocoder import LocationIqNoPlacesFound, LocationIqInvalidKey, LocationIqInvalidRequest
from locationiq.geocoder import LocationIqRequestLimitExeceeded, LocationIqServerError

class LocationIqTestCase(unittest.TestCase):
    def test_no_api_key(self):
        with self.assertRaises(LocationIqInvalidKey):
            liq = LocationIQ("locationiq-key")
            liq.geocode("Lingampally, Hyderabad")

    #Todo more tests

if __name__ == "__main__":
    unittest.main()