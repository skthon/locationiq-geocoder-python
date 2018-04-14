import unittest
from locationiq.locationiq import LocationIq
from locationiq.locationiq import LocationIqNoPlacesFound, LocationIqInvalidKey, LocationIqInvalidRequest
from locationiq.locationiq import LocationIqRequestLimitExeceeded, LocationIqServerError

class LocationIqTestCase(unittest.TestCase):
    def test_no_api_key(self):
        with self.assertRaises(LocationIqInvalidKey):
            liq = LocationIq("locationiq-key")
            liq.geocode("Lingampally, Hyderabad")


if __name__ == "__main__":
    unittest.main()