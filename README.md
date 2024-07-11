# Decision trees support the prediction of colorectal cancer in Vietnam

Đây là mô hình thử nghiệm sử dụng cây quyết định hỗ trợ dự đoán ung thư đại trực tràng ở Việt Nam dựa trên triệu chứng tiền lâm sàng, giúp giảm chi phí và tăng tốc độ chẩn đoán.

This is an experimental model using decision trees to support the prediction of colorectal cancer in Vietnam based on preclinical symptoms, helping to reduce costs and increase diagnosis speed.

## Table of Contents

- [Decision trees support the prediction of colorectal cancer in Vietnam](#decision-trees-support-the-prediction-of-colorectal-cancer-in-vietnam)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Server Setup Instructions](#server-setup-instructions)
    - [Installation Steps](#installation-steps)
      - [a. Setting Up the Environment](#a-setting-up-the-environment)
      - [b. Installing Python:](#b-installing-python)
      - [c. Installing MySQL Database:](#c-installing-mysql-database)
      - [d. Setting Up the Software Source Code and Virtual Environment:](#d-setting-up-the-software-source-code-and-virtual-environment)
      - [e. Setting Up Nginx Service:](#e-setting-up-nginx-service)
  - [Directory Structure](#directory-structure)

## Getting Started

### Server Setup Instructions

The software is installed on a server with:

- OS: Ubuntu 22.04 LTS
- CPU: Min 2 cores
- RAM: Min 4GB
- Remote SSH access enabled

### Installation Steps

#### a. Setting Up the Environment

**Required software:**

- Programming language: Python 11
- Database: MySQL
- Source code management: Git
- Related services: Nginx
- Remote connection software: MobaXterm

**Connecting to the Server:**

1. Open MobaXterm.
2. Access the server via SSH:

```sh
ssh username@ServerIP:ServerPort
```

Example:

```sh
ssh yte@192.168.233.128
```

3. Enter the password and press Enter.

#### b. Installing Python:

1. Install Python and extension virtual environment:

```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2
sudo update-alternatives --config python3
sudo apt install python3-pip
python3 -m pip install virtualenv
sudo apt install python3.11-venv
```

2. Add path for virtualenv:

```sh
nano ~/.bashrc
```

Add the following line at the end of the file:

```file
export PATH="$PATH:/home/yte/.local/bin"
```

Apply the changes:

```sh
source ~/.bashrc
```

#### c. Installing MySQL Database:

**1. Install MySQL:**

```sh
sudo apt install mysql-server
```

**2. Create a database `ung_thu` and grant privileges to user `admin`:**

```sh
sudo mysql
```

In MySQL shell:

```sh
CREATE DATABASE ung_thu;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'abc';
GRANT ALL PRIVILEGES ON ung_thu.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### d. Setting Up the Software Source Code and Virtual Environment:

**1. Download the source code:**

```sh
sudo apt-get install git
git clone https://github.com/Moobbot2/B2022-TNA-24.git
```

**2. Create a virtual environment:**

```sh
cd ~/B2022-TNA-24
python3 -m venv .venv
source .venv/bin/activate
```

**3. Run the setup script to install the necessary environment:**

```sh
python3 setup.py
```

**4. Update the database:**

```sh
sudo mysql
```

```sh
USE ung_thu;
SOURCE dataset/data_ungthu.sql;
EXIT;
```

**5. Update config.py with the MySQL connection information:**

```sh
nano config/config.py
```

**6. Start the API:**

```sh
python3 api_project.py
```

#### e. Setting Up Nginx Service:

**1. Install Nginx:**

```sh
sudo apt update
sudo apt install nginx
```

**2. Update the web interface connection link:**

```sh
sudo nano ~/B2022-TNA-24/examples/web/index.html
```

Change the line:

```javascript:
var link_connect = "http://127.0.0.1:5000"
```

To:

```javascript:
var link_connect = "http://server_domain_or_IP:5000"
```

**3. Move HTML file to the web directory:**

```sh
sudo mkdir -p /var/www/html/ungthu
sudo cp ~/B2022-TNA-24/examples/web/* /var/www/html/ungthu/
```

**4. Configure Nginx:**

```sh
sudo nano /etc/nginx/sites-available/ungthu
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name server_domain_or_IP;

    location / {
        root /var/www/html/ungthu;
        index index.html;
    }
}
```

**5. Activate Nginx:**

```sh
sudo ln -s /etc/nginx/sites-available/ungthu /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 5000
sudo ufw allow 'Nginx Full'
```

## Directory Structure

Here is an overview of the project's directory structure:

```
B2022-TNA-24/
├── config/
│   └── config.py
├── dataset/
│   └── data_ungthu.sql
├── examples/
│   └── web/
│       └── index.html
├── models/
│   └── DecisionTree.joblib
├── src/
│   └── cancer_diagnosis/
│   └── connect_database/
│   └── ocr_medical_record/
│   └── test/
├── tools/
│   ├── metrics.py
│   ├── utils.py
│   └── logging.py
├── api_project.py
├── setup.py
└── .venv/
```
