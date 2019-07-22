# Geocoder
A fork from https://github.com/hexgis/geocoder.git

A very simple django application that uses [nominatim](https://nominatim.openstreetmap.org/) engine to  to search locations into [OpenStreetMap](https://www.openstreetmap.org/).

```
Please, check politicies for nominatim application and enable your own cache politicy
```

### Available urls:
```
search/location=youlocation
reverse/lat=-12&lon=-52
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