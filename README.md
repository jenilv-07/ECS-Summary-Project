# 🌥️ ECS Summary Project

## 📖 Description
This project retrieves information about Elastic Cloud Servers (ECS) from Huawei Cloud and saves the data to a JSON file. It fetches details like server specifications, flavors, network interfaces, security groups, and more.

## 📦 Requirements
- Python 3.6 or higher
- Huawei Cloud SDK for Python

## 🛠️ Setup Instructions

1. **Clone the repository or download the project files.**
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Create a virtual environment.**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment.**
   - **For Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **For macOS and Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages.**
   Create a `requirements.txt` file in your project directory with the following content to specify the required libraries:

   ```
   huaweicloudsdkcore
   huaweicloudsdkecs
   ```

   Then, install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

   If you prefer to install the packages individually, run:
   ```bash
   pip install huaweicloudsdkcore
   pip install huaweicloudsdkecs
   ```

5. **Set up environment variables.** 🌍
   Ensure the following environment variables are set in your environment:

   - `HUAWEI_ACCESS_KEY`: Your Huawei Cloud Access Key
   - `HUAWEI_SECRET_KEY`: Your Huawei Cloud Secret Key
   - `HUAWEI_PROJECT_ID`: Your Huawei Cloud Project ID
   - `HUAWEI_REGION`: Your Huawei Cloud Region

   You can set environment variables in your terminal like this (Linux/macOS):
   ```bash
   export HUAWEI_ACCESS_KEY='your_access_key'
   export HUAWEI_SECRET_KEY='your_secret_key'
   export HUAWEI_PROJECT_ID='your_project_id'
   export HUAWEI_REGION='your_region'
   ```

   For Windows, use:
   ```bash
   set HUAWEI_ACCESS_KEY='your_access_key'
   set HUAWEI_SECRET_KEY='your_secret_key'
   set HUAWEI_PROJECT_ID='your_project_id'
   set HUAWEI_REGION='your_region'
   ```

6. **Run the project.** 🚀
   After setting everything up, you can run the project:
   ```bash
   python ecs_instance_reporter.py
   ```

## 💾 Output
The ECS server data will be saved in a JSON file named `ecs_summary_<access_key>_<project_id>_<region>_<timestamp>.json`.

## ⚠️ Error Handling
The program raises appropriate errors for missing environment variables and failures during API requests.

## 📝 License
This project is licensed under the MIT License.
