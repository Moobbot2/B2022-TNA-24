import pandas as pd

df = pd.read_excel("./dataset/output.xlsx")

features = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân",
            "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm",
            "hoạch ngoại biên", "hạch thượng đòn",
            "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc",
            "dấu hiệu rắn bò", "quai ruột nổi",
            "sờ thấy khối u", "thăm trực tràng có khối u", "tiền sử ung thư",
            "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u"]

X = df[features]
y = df['KQ']

print(y)