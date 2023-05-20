# Drag Queens Collection API

Drag Queens Collection API made using python and in FastApi framework.

## Description

Main focus of this project was:
- create fast and easy REST API based on previously prepared api documentation (OpenApi standard)
- deploy and provide API for frontend team to play with it

Application was created in two versions:
- v1.0.0 - basic application, uses in-memory "database" with no authorization nor authentication
- v2.1.0 - deployed to [Deta Space](https://deta.space/developers) with data storage (NoSQL database),
authorization and authentication implemented using JWT

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

### v1.0.0

API documentation:

https://e4hke1.deta.dev/docs

### v2.1.0

API documentation:

https://queensapiv21-1-z9994616.deta.app/docs

## Run the application locally

In order to run the project locally, you need to have <b>Python 3</b> installed.

Each project folder ```app_v1``` and ```app_v2``` should be treated as <b>separate microservice</b>.

1. Clone repository:
```
git clone https://github.com/nataliacza/queens-basic-api
```

2. Create virtual environment for each microservice ```app_v1``` and ```app_v2```:
[instruction](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).
Project was build using [Poetry](https://python-poetry.org/).

3. Install dependencies:
```
(while being in folder app_v1 or app_v2)
pip install -r requirements.txt
```
For Poetry:
```
poetry install
```

4. For ```app_v2``` create in main project folder a new file ```.env```, copy data from
```.env-example``` file and fill with variables.

5. Run application on your local machine:
```
uvicorn main:app --port 8000
```

6. Go to application API docs:
```
http://127.0.0.1:8000/docs
```


# ENJOY!
