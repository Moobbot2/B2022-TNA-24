PRIMARY_DATA_LINK = "./dataset/data"
OUTPUT_LINK = "./dataset/output.xlsx"

FEATURES = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân",
            "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm",
            "hoạch ngoại biên", "hạch thượng đòn",
            "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc",
            "dấu hiệu rắn bò", "quai ruột nổi",
            "sờ thấy khối u", "thăm trực tràng có khối u", "tiền sử ung thư",
            "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u"]

# Assuming the target variable is named 'KQ' (1 for cancer, 0 for no cancer)
KQ = "ket_qua"

# Database sql
DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_NAME = 'data_ungthu'
TABLE_NAME = 'trieu_chung_va_chuan_doan'
SAVE_MODEL_PATH = 'output/model/'
SAVE_TREE_PATH = 'output/image_tree/'
