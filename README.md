# Document Retrieval System

## Overview

This project implements a document retrieval system designed for chat applications, enabling efficient context generation for large language models. The system is built using Python and leverages Elasticsearch for document storage and retrieval, with Redis for caching. 

## Features

- **Backend Retrieval**: Utilizes Elasticsearch for storing and querying documents.
- **Caching**: Redis is used for caching to ensure faster retrieval.
- **Background Scraping**: A background thread which uses SBERT scrapes news articles upon server startup.
- **API Endpoints**:
  - `/health`: Returns a random response to check if the API is active.
  - `/search`: Searches documents based on the text query with parameters for number of results (`top_k`) and similarity score threshold (`threshold`).

## Requirements

- Python 3.9+
- Docker
- Docker Compose

## Setup
- Make sure Docker for desktop is installed 
- Elastic Search should be downloaded for Docker to fetch its elasticsearch.yml file otherwise it will give configuration error.
- after cloning repository open it and save all the files and run the docker command given below also check the dockerfile and docker-compose.yml for any missing dependencies.
- Docker will install all dependencies and will build a container and will start running.
- At last to verify try running test files as the command given below and it will start generating output.

### Clone the Repository

```bash
git clone https://github.com/amannmishraa/21BCE7202_ML.git
cd 21BCE7202_ML
docker-compose up --build  
python <test_file(name)>.py

