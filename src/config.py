PRIMARY_DATA_LINK = "./dataset/data"
OUTPUT_LINK = "./dataset/output.xlsx"
POPPLER_PATH = "./poppler-24.02.0/Library/bin"

FEATURES_VN = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân", "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm", "hoạch ngoại biên", "hạch thượng đòn", "bụng chướng", "phản ứng thành bụng",
                "cảm ứng phúc mạc",  "dấu hiệu rắn bò", "quai ruột nổi", "sờ thấy khối u", "thăm trực tràng có khối u", "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u", "tiền sử ung thư"]
# from unidecode import unidecode
# FEATURES = [unidecode(feature).replace(' ', '_') for feature in FEATURES_old]
FEATURES = ['dau_bung', 'non', 'chan_an', 'tao_bon', 'sut_can', 'tieu_chay', 'phan_co_mau', 'da_niem_mac_vang', 'da_sam', 'hoach_ngoai_bien', 'hach_thuong_don', 'bung_chuong', 'phan_ung_thanh_bung',
            'cam_ung_phuc_mac', 'dau_hieu_ran_bo', 'quai_ruot_noi', 'so_thay_khoi_u', 'tham_truc_trang_co_khoi_u', 'chup_CT_o_bung_co_khoi_u', 'noi_soi_dai_trang_co_khoi_u', 'tien_su_ung_thu']
# Assuming the target variable is named 'KQ' (1 for cancer, 0 for no cancer)
KQ = "ket_qua"

# Database sql
DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_NAME = 'data_ungthu'
TABLE_NAME = 'trieu_chung_va_chuan_doan'
SAVE_MODEL_PATH = 'output/model'
SAVE_TREE_PATH = 'output/image_tree'
SAVE_LOG_PATH = 'output/log'

TEST_SIZE = 0.2
RAMDOM_STATE = 42
N_ESTIMATORS = 100
MODEL_USE = 'DecisionTree'  # DecisionTree or RandomForest or XGBoost
