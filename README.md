LocationIQ Python geocoder
--------------------------
Python client library for LocationIQ Gecoding Services

Usage
-----
LocationIQ python client library can be installed using pip:
   
    $ pip install loationiq

Load the locationiq geocoding module using the below line:
    
    from locationiq.geocoder import LocationIQ
    
Now create a instance of the geocoder module, pass the LocationIQ `API Token` as the parameter to module's constructor.

    geocoder = LocationIQ(key)
    

Forward Geocoding
-----------------

To convert the street addresses into geographic coordinataes (latitude and longitude)

    geocoder.geocode('Charminar Hyderabad')
    
Reverse Geocoding
-----------------

To convert geographic coordinates into street addresses 

    geocoder.reverse_geocoder(17.3850, 78.4867)


Exceptions
----------

if there is any error, below exceptions will be raised.
 * ``LocationIqNoPlacesFound`` if there are no matching results 
 * ``LocationIqInvalidKey`` If the provided api_key is invalid.
 * ``LocationIqInvalidRequest`` If you go past your rate limit.
 * ``LocationIqRequestLimitExeceeded`` If you go past ratelimits.
 * ``LocationIqServerError`` occurs basically when there's server error