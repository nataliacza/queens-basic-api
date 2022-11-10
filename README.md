# Drag Queens Collection API - Beta

Drag Queens API made using python and in FastApi framework.

## Description

Main focus of this project was:
- create fast and easy REST API based on previously prepared api documentation (OpenApi standard)
- deploy and provide API for frontend team to play with it

Application uses in-memory storage, and it's deployed on [Deta Cloud](https://www.deta.sh/).

As the main focus was on <i>fast</i> and <i>deploy</i>, authorization and authentication was omitted.

## Tech tools
- Python >3.10
- FastAPI >0.86.0
- Uvicorn >0.19.0
- Deta (deploy)

Validation relays on Pydantic >1.10.2.

## API Documentation

Original API documentation is located in <i>/docs</i> folder. 

## Run the application

In order to run the project locally, you need to have Python 3 installed.

1. Clone repository:
```
git clone https://github.com/nataliacza/queens-basic-api
```

2. Create virtual environment: [instruction](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

3. Install dependencies:
```
pip install app/requirements.txt
```

4. Run application on your local machine:
```
uvicorn app.main:app --port 8000
```
