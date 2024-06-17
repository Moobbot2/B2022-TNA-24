import io
import zipfile
import os
import subprocess

try:
    import requests
except ModuleNotFoundError as e:
    subprocess.run(["pip", "install", "requests"])
    import requests


def check_gpu():
    """
    Kiểm tra xem máy có GPU hay không.
    Returns:
    bool: True nếu máy có GPU, False nếu không.
    """
    try:
        import torch

        return torch.cuda.is_available()
    except ImportError:
        subprocess.run(["pip", "install", "torch"])
        import torch

        return torch.cuda.is_available()


def download_file(url, folder, filename):
    """
    Tải một tệp từ URL và lưu vào thư mục đã chỉ định.
    Arguments:
    url (str): URL của tệp cần tải.
    folder (str): Đường dẫn của thư mục để lưu tệp.
    filename (str): Tên của tệp sau khi được tải.
    Returns:
    str: Đường dẫn đầy đủ của tệp đã được tải và lưu, hoặc None nếu đã tồn tại.
    """
    # Tạo đường dẫn đầy đủ của tệp
    filepath = os.path.join(folder, filename)
    # Kiểm tra xem tệp đã tồn tại không
    if os.path.exists(filepath):
        print("Tệp đã tồn tại:", filepath)
        return filepath
    # Tạo thư mục nếu nó chưa tồn tại
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        # Tải file từ URL và lưu vào thư mục đích
        response = requests.get(url)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("File đã được tải xuống và lưu vào:", filepath)
        return filepath
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        return None


def download_and_extract_zip(url, extract_path="."):
    """
    Download a ZIP file from the given URL and extract its contents.
    Args:
    - url (str): The URL of the ZIP file to download.
    - extract_path (str): The path where the contents of the ZIP file will be extracted. Default is the current directory.
    Returns:
    - bool: True if the download and extraction were successful, False otherwise.
    """
    try:
        # Check if the destination folder exists, if not, create it
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
        # Get the filename from the URL
        filename = url.split("/")[-1]
        # Check if the file already exists in the destination folder
        if os.path.exists(os.path.join(extract_path, filename)):
            print(f"{filename} already exists. Skipping download.")
            return True
        # Download the ZIP file
        print(f"Downloading {filename}...")
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the contents of the ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"{filename} downloaded and extracted successfully.")
            return True
        else:
            print("Failed to download the ZIP file.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def main():
    # Kiểm tra xem máy có GPU hay không
    has_gpu = check_gpu()

    # Cài đặt các gói cần thiết
    if has_gpu:
        subprocess.run(
            [
                "pip",
                "install",
                "torch",
                "torchvision",
                "torchaudio",
                "--index-url",
                "https://download.pytorch.org/whl/cu121",
            ]
        )
    else:
        subprocess.run(
            [
                "pip",
                "install",
                "torch",
                "torchvision",
                "torchaudio",
            ]
        )
    from config.config import BASE_PATH

    # Cài đặt các gói từ requirements.txt
    subprocess.run(
        ["python", "-m", "pip", "install", "-r", BASE_PATH + "/requirements.txt"]
    )

    # Tải và giải nén Poppler
    tools_support = "./tools"
    print("Dowload poppler.")
    url_poppler = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.02.0-0/Release-24.02.0-0.zip"
    download_and_extract_zip(url_poppler, tools_support)


if __name__ == "__main__":
    main()
