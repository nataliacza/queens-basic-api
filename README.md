# Drag Queens Collection API

Drag Queens Collection API made using python and in FastApi framework.

## Description

Main focus of this project was:
- create fast and easy REST API based on previously prepared api documentation (OpenApi standard)
- deploy and provide API for frontend team to play with it

Application was created in two versions:
- v1 - basic application, uses in-memory "database" with no authorization nor authentication
- v2 - uses [Deta Base](https://docs.deta.sh/docs/base/about/) data storage (NoSQL database), authorization and authentication implemented using JWT

Both versions are deployed on [Deta Micros](https://docs.deta.sh/docs/micros/about/).
Official Deta Cloud web: https://www.deta.sh/.

## Tech tools
- Python
- FastAPI
- Uvicorn
- PyJWT
- bcrypt
- Deta (deploy)

## API Documentation

Original API documentation is located in <i>/docs</i> folder.

## Visit deployed application

### v1

API documentation:

https://e4hke1.deta.dev/docs

Endpoints:
```
[GET/POST]
https://e4hke1.deta.dev/api/v1/queens
[GET/PUT/DELETE]
https://e4hke1.deta.dev/api/v1/queens/{queen_id}

[GET/POST]
https://e4hke1.deta.dev/api/v1/categories
[GET/PUT/DELETE]
https://e4hke1.deta.dev/api/v1/categories/{category_id}

[GET/POST]
https://e4hke1.deta.dev/api/v1/cities
[GET/PUT/DELETE]
https://e4hke1.deta.dev/api/v1/cities/{city_id}
```

### v2

API documentation:

https://gbq2bc.deta.dev/docs

Endpoints:
```
[GET/POST]
https://gbq2bc.deta.dev/api/v2/queens
[GET/PUT/DELETE]
https://gbq2bc.deta.dev/api/v2/queens/{queen_id}

[GET/POST]
https://gbq2bc.deta.dev/api/v2/categories
[GET/PUT/DELETE]
https://gbq2bc.deta.dev/api/v2/categories/{category_id}

[GET/POST]
https://gbq2bc.deta.dev/api/v2/cities
[GET/PUT/DELETE]
https://gbq2bc.deta.dev/api/v2/cities/{city_id}

[POST]
https://gbq2bc.deta.dev/api/v2/users/signup
[POST]
https://gbq2bc.deta.dev/api/v2/users/login
```

## Run the application locally

In order to run the project locally, you need to have <b>Python 3</b> installed.

Each project folder ```app_v1``` and ```app_v2``` should be treated as <b>separate microservice</b>.

1. Clone repository:
```
git clone https://github.com/nataliacza/queens-basic-api
```

2. Create virtual environment for each microservice ```app_v1``` and ```app_v2```: [instruction](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

3. Install dependencies:
```
(while being in folder app_v1 or app_v2)
pip install -r requirements.txt
```

4. For ```app_v2``` create in main project folder a new file ```.env```, copy data from ```.env-example``` file and fill with variables.

5. Run application on your local machine:
```
uvicorn main:app --port 8000
```

5. Go to application api docs:
```
http://127.0.0.1:8000/docs
```
