# pip install unidecode, pyviF

from unidecode import unidecode
from pyvi import ViUtils


# Tiền xử lý(dấu câu) + hậu xử lý ()
def main():

    status = "Bệnh nhân nam 60 tuổi. Tiền sử K đại tràng di căn gan ( Đã phẫu thuật hiện đang điều trị hóa chất) Lý do vào viện: Đau cổ và vai trái Bệnh sử: Theo lời bệnh nhân kể, khoảng 1 tháng nay bệnh nhân đau vùng cột sống cổ, đau tê lan xuống vai trái và cánh tay trái, đau nhiều về đêm. Sút 6 kg trong 2 tháng nay. Ở nhà tự dùng thuốc giảm đau nhưng không đỡ. Nay đau tăng vào viện khám và điều trị. Tình trạng lúc vào: Bệnh nhân tỉnh, tiếp xúc tốt Thể trạng trung bình Da niêm mạc hồng Không phù, không xuất huyết dưới da Hạch ngoại vi, tuyến giáp không to Đau vùng cột sống cố, đau tê lan xuống vai trái, cánh tay trái Đau tăng về đêm; hạn chế cử động cột sống cổ và khớp vai trái VAS 7/10 Ấn dọc cột sống cố và cột sống ngực T1-4 đau Tim nhịp đều T1T2 rõ, ts 83 ck/phút Phổi thông khí được, không ran  , không chướng - Siêu âm 1/8/22: HÌNH ẢNH M GAN. - Xquang 1/8/22: Hình ảnh thoái hóa đốt sống cổ C4, C5, C6.Hiện tại hình ảnh X-Quang tim phổi bình thường. - CT ổ bụng22/6/22: Hiện tại không thấy hình ảnh dày thành hay khối bất thường khung đại tràng. Hình ảnh nghĩ đến di chứng tổn thương cũ ở gan. Nang gan trái. Hình ảnh nốt nhỏ vùng đáy phổi hai bên: TD M phổi hai bên Chẩn đoán: Hội chứng cổ vai gáy/ K đại tràng di căn gan, TD di căn phổi, đi căn xương."
    status = status.lower()
    status_1 = ViUtils.remove_accents(status).decode("utf-8")
    print(status_1)
    print("-------------")
    status_2 = unidecode(status)
    print(status_2)

    TMP = get_symptoms(status_1)

    print(TMP)

    TMP = get_symptoms(status_2)

    print(TMP)


if __name__ == "__main__":
    from helpers import add_path_init

    add_path_init()
    from cancer_diagnosis.helpers import get_symptoms
    main()

else:
    from src.cancer_diagnosis.helpers import get_symptoms
