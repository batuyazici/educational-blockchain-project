# Project Title
Simulating Blockchain Architecture for Educational Purposes in University Courses

## Description

## Project Status

## Installation
First, clone the repository to your local machine:
```bash
git clone https://github.com/batuyazici/educational-blockchain-project.git
cd educational-blockchain-project
```
Then, install the required Python libraries:
```bash 
pip install -r requirements.txt
```
Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
After activating the virtual environment, install the required libraries:
```bash
pip install -r requirements.txt
```
## Usage
To use the system, you have two main components: the blockchain itself and the client interface. Below are the commands to run each component.
### Running the Blockchain
To start the blockchain, use the following command:
```
python blockchain.py
```
Optionally, you can specify a port for the blockchain server:
```
# Using a short flag
python blockchain.py -p 5000
```
```
# Using a full flag
python blockchain.py --port 5000
```
### Running the Blockchain Client
To start the blockchain client, use this command:
```
python blockchainClient.py
```
Similarly, you can specify a port for the client:
```
# Using a short flag
python blockchainClient.py -p 8080
```
```
# Using a full flag
python blockchainClient.py --port 8080
```
In these commands, `-p` or `--port` followed by a number assigns the specific port on which the service will run. Adjust the port numbers according to your network configuration and requirements.
## Features




## License

