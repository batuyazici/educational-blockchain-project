## 🌐 Simulating Blockchain Architecture for Educational Purposes 🌐

[![Python Badge](https://img.shields.io/badge/-Python-3776AB?style=flat-square&labelColor=3776AB&logo=Python&logoColor=white&link=link)](link)
[![HTML Badge](https://img.shields.io/badge/-HTML-E34F26?style=flat-square&labelColor=000&logo=html5&logoColor=white&link=link)](link)
[![CSS Badge](https://img.shields.io/badge/-CSS-1572B6?style=flat-square&labelColor=000&logo=css3&logoColor=white&link=link)](link)
[![JavaScript Badge](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&labelColor=F7DF1E&logo=JavaScript&logoColor=white&link=link)](link)
[![jQuery Badge](https://img.shields.io/badge/-jQuery-0769AD?style=flat-square&labelColor=0769AD&logo=jQuery&logoColor=white&link=link)](link)
[![Bootstrap Badge](https://img.shields.io/badge/-Bootstrap-563D7C?style=flat-square&labelColor=563D7C&logo=Bootstrap&logoColor=white&link=link)](link)

<i>This project aims to explain the fundamental concepts of blockchain technology through an interactive and educational simulation. Our goal is to make blockchain accessible to beginners and anyone interested in the technology. To create this simulation, we used Python and specific libraries to construct the blockchain backend. For the user interface, we employed HTML, CSS, and JavaScript to create a simple yet effective interactive platform. This project serves as an entry-level gateway into the world of blockchain, offering hands-on experience with its key concepts and workings. </i>

## 🖇 Demo Video



https://github.com/batuyazici/educational-blockchain-project/assets/92368839/cefc1151-9ab6-439a-b922-56e435bfc040



## 🖇 Blockchain Network Architecture Diagram
![blockchain_diagram](https://github.com/batuyazici/educational-blockchain-project/assets/117301486/79b83580-d7eb-48ac-aee6-86b31e1f15b3)

## 🖇 Project Status
<b>Current Status:</b> <i>Active Development</i> 🟢

## 🖇 Features

<i>The simulation includes the following key features:</i>

🔹 <b>Mining and Consensus Mechanism:</b> <i>Demonstrates how new blocks are created and verified in a blockchain network.</i> <br>
🔹 <b>Proof of Work Algorithm:</b> <i>Explains the process that maintains integrity and security within the blockchain.</i> <br>
🔹 <b>Transaction Structure:</b> <i>Describes how transactions are created, structured, and recorded.</i> <br>
🔹 <b>Signature Creation and Verification:</b> <i>Shows how digital signatures maintain the authenticity of transactions.</i> <br>
🔹 <b>Ledger Structure:</b> <i>Provides insights into how data is stored and organized in a blockchain.</i> <br>
🔹 <b>Block Connectivity:</b> <i>Visualizes how blocks are linked to form a secure and unalterable chain.</i> <br>
🔹 <b>Public-Private Key Pair Creation:</b> <i>Highlights the cryptographic methods used in blockchain for secure communications.</i> <br>

## 🖇 Upcoming Features

<i>We are dedicated to enhancing the functionality and user experience of our blockchain simulation. Here are some key features we plan to implement:</i>

🔹 <b>Block Broadcast After Mining: </b><i>Newly mined blocks and updated chains are automatically broadcasted to the entire network, ensuring that all nodes have the latest version of the blockchain.</i> <br>
🔹 <b>Transaction Pool for Each Node: </b><i>Individual transaction pools allow nodes to collect and store transactions before they are mined into blocks, enhancing the efficiency of the transaction process.</i> <br>
🔹 <b>Peer-to-Peer (P2P) Connections Between Nodes: </b><i>Establishing a P2P network enables nodes to communicate directly with each other, a crucial feature for decentralization and robustness in blockchain networks</i> <br>
🔹 <b>Web Application UI with React:</b> <i>Upgrading the user interface to a web application, possibly using React, provides a more interactive and user-friendly experience.</i> <br>
🔹<b>Enhanced Wallet Mechanism: </b><i>Improving the wallet functionality to include features like saving created wallets and their balances enhances user interaction and security.</i> <br>
🔹 <b>Advanced Mining Mechanism: </b><i>Updating the mining mechanism to work with more complex and difficult hashes simulates the real-world challenges in blockchain mining.</i> <br>

## 🖇 Installation
<i>🔹 First, clone the repository to your local machine:</i>

```bash
git clone https://github.com/batuyazici/educational-blockchain-project.git
cd educational-blockchain-project
```
<i>🔹 Then, install the required Python libraries:</i>
```bash 
pip install -r requirements.txt
```
<i>🔹 Virtual Environment (Optional)</i>
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
<i>🔹 After activating the virtual environment, install the required libraries:</i>
```bash
pip install -r requirements.txt
```
## 🖇 Usage
<i>🔹 To use the system, you have two main components: the blockchain itself and the client interface. Below are the commands to run each component.</i>
### ▶️ Running the Blockchain
<i>🔹 To start the blockchain, use the following command:</i>
```
python blockchain.py
```
<i>🔹 Optionally, you can specify a port for the blockchain server:</i>
```
# Using a short flag
python blockchain.py -p 5000
```
```
# Using a full flag
python blockchain.py --port 5000
```
### ▶️ Running the Blockchain Client
<i>🔹 o start the blockchain client, use this command:</i>
```
python blockchainClient.py
```
<i>🔹 Similarly, you can specify a port for the client:</i>
```
# Using a short flag
python blockchainClient.py -p 8080
```
```
# Using a full flag
python blockchainClient.py --port 8080
```
<i>🔹 In these commands, `-p` or `--port` followed by a number assigns the specific port on which the service will run. Adjust the port numbers according to your network configuration and requirements.</i>


## 🖇 References

🔹 <b>Karpathy, A. (Year). cryptos. GitHub repository. </b>  <br>
<i>Available at:</i> https://github.com/karpathy/cryptos <br>
🔹 <b> Romero, J. (Year). Dumbcoin. GitHub repository.</b> <br>
<i>Available at:</i> https://github.com/julienr/ipynb_playground/blob/master/bitcoin/dumbcoin/dumbcoin.ipynb</b> <br>
🔹 <b> Moujahid, A. (Year). Blockchain Python Tutorial. GitHub repository.</b> <br>
<i>Available at:</i> https://github.com/adilmoujahid/blockchain-python-tutoria <br>


