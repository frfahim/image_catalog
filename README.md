# Image Catalog
Very basic image scrapper from web pages.

### Tech
- Python
- Django
- Django Rest Framework

### Installation

- Clone repo  `git clone git@github.com:frfahim/image_catalog.git`

- Create a virtualenv `python3 -m venv image-venv`

- Activate created virtualenv `source image-venv/bin/activate`

- Goto project directory `cd image_catalog`

- Install requirement file `pip install -r requirements.txt`

- Run project `./startapp.sh`

- API documentation `0.0.0.0:8000/api/v1/docs`

> If script file get permission error run `chmod +x startapp.sh` and hit `./startapp.sh` again

#### TODO
 - Docker support
 - Async support in image downloder
 - Postgres/MySql DB integretion
