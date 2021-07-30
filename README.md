# OpenCLI
![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiR2ZJNFp4S243bmNBVW13VGRuQkNndGRuVVRiK2tzSDhGRkcyQ1BhRWdCZXlnaGI0T2E5MlJ0dElzbjFqNEY5ZHFZcDdKYS9JT0h1SmVLdjF3Q1RDUnVZPSIsIml2UGFyYW1ldGVyU3BlYyI6Im9sdXhWQnh5K2FoMWI5NnYiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

A CLI for every service which exposes a OpenAPI (Swagger) specification endpoint.

From the OpenAPI Specification project:

> The goal of The OpenAPI Specification is to define a standard, language-agnostic interface to REST APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection.

## Demo

![Alt Text](https://github.com/privcloud-com/open-cli/blob/master/demo.gif)
![Alt Text](https://github.com/privcloud-com/open-cli/blob/master/demo_table.gif)

## Docker

To start a CLI session run:

    docker run -it privcloud-com/open-cli3 <swagger-spec-url>

e.g:

    docker run -it privcloud-com/open-cli3 http://petstore.swagger.io/v3/swagger.json


To start a CLI session run:

    open-cli3 <swagger-spec-url>

e.g:

    open-cli3 https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore-expanded.json

For more options run:

    open-cli3 -h

Credits
-------
This project relies on OpenApi3 [openapi3](https://github.com/Dorthu/openapi3) project & on Jonathan Slenders [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit).
