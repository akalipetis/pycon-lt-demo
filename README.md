# PyCon LT Demo

This is the repository for the code demonstrated during PyCon LT.

## How to demo this application

This application demonstrates 3 different states of running a Django application, one with the "classic" Django way, one using Uvicorn to win concurrency out of the box and one leveraging Django's built-in asyncio support.

### Simple Gunicorn setup

You can easily run the application with a simple Gunicorn setup using `make gunicorn`

### Uvicorn setup

Running the application using Uvicorn for better concurrency out of the box can be run with `make uvicorn`

### Improved setup

For an improvement to better leverate asyncio checkout the `feat/asyncio` branch.

## Load testing

You can use your tool of choice for load testing the application. Included is a demo load test using vegeta which you can run with this command `make loadtest my-app.eu-5.platform.sh`, after replacing the URL provided by Upsun, or any other host you have your application running.
