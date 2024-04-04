# Decision trees support the prediction of colorectal cancer in Vietnam

Đây là mô hình thử nghiệm sử dụng cây quyết định hỗ trợ dự đoán ung thư đại trực tràng ở Việt Nam dựa trên triệu chứng tiền lâm sàng, giúp giảm chi phí và tăng tốc độ chẩn đoán.

This is an experimental model using decision trees to support the prediction of colorectal cancer in Vietnam based on preclinical symptoms, helping to reduce costs and increase diagnosis speed.

## Getting Started

### Prerequisites

- Python >= 11.

### Installation

**Ensure that you have the latest version of pip installed:**

```bash
py -m pip install --upgrade pip
```

**Install the required dependencies:**

```bash
py -m pip install requests
```

**Build the environment using the provided setup script:**

```bash
py setup.py
```

**Data base**

To use the MySQL database, follow these steps:

1. Create a new database in MySQL.
2. Import the data from the provided [data_ungthu.sql](.\dataset\data_ungthu.sql) file into the newly created database.
3. Update the login information for the database in the [config.py](.\config\config.py) file.

## Usage

- **Step 1: Run API** To start the API for accessing the decision tree model:

```bash
py api_project
```

- **Step 2: Accessing the Web Demo** The web demo by opening the [Web demo](.\examples\web\index.html) file in a web browser.

## Directory Structure
