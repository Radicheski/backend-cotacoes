# Stock Price API

## Overview

The Stock Price API provides an interface for retrieving historical stock prices for valid tickers listed on the B3 (Brazilian Stock Exchange). It allows users to fetch stock prices over specific date ranges or for a specific date.

## Features

- Fetch stock prices for one or more tickers.
- Specify a date range (start and end dates) or a specific date.
- Support for Docker deployment.
- Includes a script for updating the stock price database.

## Setup and Installation

To get started with the Stock Price API, follow these steps:

### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Radicheski/backend-cotacoes.git
cd backend-cotacoes
```

### 2. Install the dependencies

Ensure you have Python 3.x installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Update data

**Warning:** Running this script will download over 4GB of data. Ensure you have enough storage and a stable internet connection before proceeding.

```bash
chmod +x update.sh
./update.sh
```

### 4. Run the Flask app

To start the API locally, run the following command:

```bash
flask run
```

By default, the Flask app will run on `http://127.0.0.1:5000`. You can change the port or host in the code if needed.

## Docker Setup

If you prefer to run the API inside a Docker container, you can follow these steps.

### 1. Build the Docker image

Run the following command to build the Docker image from the provided `Dockerfile`:

```bash
docker build -t stock-price-api .
```

### 2. Run the Docker container

Once the image is built, you can run the container with:

```bash
docker run -p 5000:5000 stock-price-api
```

This will start the API in a Docker container and bind it to port `5000` on your machine. You can access the API at `http://localhost:5000`.


## Dependencies

The following dependencies are required to run the project:

- `Flask`: A micro web framework for Python used to build the API.

You can install all the dependencies using the `pip install -r requirements.txt` command.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
