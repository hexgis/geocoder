# Geocoder

A very simple django application that uses [nominatim](https://nominatim.openstreetmap.org/) engine to search locations in [OpenStreetMap](https://www.openstreetmap.org/).

```
Please, check privacy policies for nominatim application and enable your own cache data policies.
```

### Available urls:

The search and reverse urls accept `GET` and `POST` methods, and will search data in the Nominatim API.

```bash
/search?location

/reverse?lat=-12&lon=-53
```

Examples:
`curl -X GET localhost:8080/search?location=MyCity`
or 
`curl -X POST localhost:8080/search -d location=MyCity`

The response will be:
```json
{
  "type":"FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { 
        "type":"Point",
        "coordinates": [
           10.5525370239731, 52.9689393
        ]
      },
      "properties": {
        "name":"mycity, Friedensreich-Hundertwasser-Platz, Veerßen, Uelzen, Niedersachsen, 29525, Deutschland"
      }
    }
  ]
}
```

### Development

Cloning project:
```bash
$ git clone http://github.com/dagnaldo/geocoder.git
```

Install requirements for dev:
```bash
$ pip install -r requirements_dev.txt
```

Apply django migrations:
```bash
$ python manage.py migrate
```

Run tests:
```bash
$ python manage.py test
```

Run project locally:
```bash
$ python manage.py runserver
```

Now, by default, the server will be available in http://localhost:8000 that will be possible to see both __search__ and __reverse__ urls;


### Using Docker

For docker development, we add a Dockerfile that will help with the applications and containers for development.
The default configurations is available in `docker-compose.yaml` file and can be changed according to your development preferences.

Running docker-compose

```bash
$ docker-compose up
```
