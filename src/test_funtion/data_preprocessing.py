import pandas as pd
from pyvi import ViUtils
import xlsxwriter
import os
import math

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def get_excel(path):
    name = []

    df = pd.read_excel(r"" + path)
    for i in df.columns:
        name.append(i)
    return name, df


def get_info(df, infos):

    for r in range(len(df)):
        data = []
        for i in range(len(df.columns)):
            nul = False
            try:
                nul = math.isnan(float(df.iloc[r, i]))
            except:
                data.append(str(df.iloc[r, i]))
                continue
            if nul == True:
                data.append('null')
            else:
                data.append(str(df.iloc[r, i]))

        infos.append(data)

    return infos


def get_data(infos):
    db_ngay_dau = []
    db_code = []
    db_hand = []

    for info in infos:
        db_ngay_dau.append(info[2])
        db_code.append(info[0])
        db_hand.append(info[1])

    return db_ngay_dau, db_hand, db_code


def get_symptoms(data):
    TMP = []

    if "dau bung" in data or "tuc bung" in data:
        if not "khong dau bung" in data and not "khong tuc bung" in data:
            TMP.append("đau bụng")

    if "non" in data and not "khong non" in data:
        TMP.append("nôn")

    if "chan an" in data or "an uong kem" in data or "an ngu kem" in data:
        TMP.append("chán ăn")

    if "tao bon" in data:
        TMP.append("táo bón")

    if "sut can" in data or "giam can" in data:
        TMP.append("sút cân")

    if "tieu chay" in data and not "khong tieu chay" in data:
        TMP.append("tiêu chảy")

    if "phan co mau" in data or "di ngoai ra mau" in data:
        TMP.append("phân có máu")

    if "da niem mac vang" in data:
        TMP.append("da niêm mạc vàng")

    if "da sam" in data:
        TMP.append("da sạm")

    if "hach ngoai bien" in data:
        if not "hach ngoai bien am tinh" in data and not "hach ngoai bien (-)" in data:
            TMP.append("hoạch ngoại biên")

    if "hach thuong don" in data:
        if not "hach thuong don am tinh" in data and not "hach thuong don (-)" in data:
            TMP.append("hạch thượng đòn")

    if "bung chuong" in data or "day bung" in data:
        if not "khong day bung" in data:
            TMP.append("bụng chướng")

    if "phan ung thanh bung" in data:
        TMP.append("phản ứng thành bụng")

    if "cam ung phuc mac" in data:
        TMP.append("cảm ứng phúc mạc")

    if "dau hieu ran bo" in data:
        TMP.append("dấu hiệu rắn bò")

    if "quai ruot noi" in data:
        TMP.append("quai ruột nổi")

    if "so thay u" in data or "so thay khoi u" in data or "co khoi u" in data or "co u" in data:
        if not "khong so thay u" in data and not "khong so thay khoi u" in data and not "khong co khoi u" in data and not "khong co u" in data:
            TMP.append("sờ thấy khối u")

    if "tham truc trang co kho u" in data:
        TMP.append("thăm trực tràng có khối u")

    if "tien su ung thu" in data or "tien su k" in data or "ung thu dai trang" in data or "k dai trang" in data:
        if not "khong tien su ung thu" in data and not "khong tien su k" in data and not "khong ung thu dai trang" in data:
            try:
                idx = data.index("ung thu")
            except:
                idx = data.index("k")

            if not "chan doan" in data[:idx] and not "chuan doan" in data[:idx]:
                TMP.append("tiền sử ung thư")

    if "chup ct o bung co khoi u" in data or "chup ct o bung co u" in data:
        TMP.append("chụp CT ổ bụng có khối u")

    if "noi soi dai trang co khoi u" in data or "noi soi dai trang co u" in data:
        TMP.append("nội soi đại tràng có khối u")

    return TMP


def Convert(string):
    li = list(string.split(","))
    return li


fields = ["đau bụng", "nôn", "chán ăn", "táo bón", "sút cân",
          "tiêu chảy", "phân có máu", "da niêm mạc vàng", "da sạm",
          "hoạch ngoại biên", "hạch thượng đòn",
          "bụng chướng", "phản ứng thành bụng", "cảm ứng phúc mạc",
          "dấu hiệu rắn bò", "quai ruột nổi",
          "sờ thấy khối u", "thăm trực tràng có khối u", "tiền sử ung thư",
          "chụp CT ổ bụng có khối u", "nội soi đại tràng có khối u"]

output_link = "./dataset/output.xlsx"
if __name__ == "__main__":
    if os.path.exists(output_link):
        os.remove(output_link)
        # os.system(f"rm -rf {output_link}")

    workbook = xlsxwriter.Workbook(output_link)
    worksheet = workbook.add_worksheet()

    average = 'macro'

    bn = 0
    error = 0
    row = 0
    col = 0

    correct_bn = 0

    for idx, field in enumerate(fields):
        worksheet.write(row, col+idx, field)
    worksheet.write(row, col+len(fields), "ket_qua")

    row = 1

    input = "./dataset/data"
    input_sv = "./dataset/data_hand"
    output = "./dataset/data_code"
    os.makedirs(output, exist_ok=True)

    total_pred = []
    total_ground = []

    for xlsx in os.listdir(input):
        rol_kq = 1
        workbook_kq = xlsxwriter.Workbook(f"{output}/{xlsx}")
        worksheet_kq = workbook_kq.add_worksheet()

        worksheet_kq.write(0, 0, "code extract")
        worksheet_kq.write(0, 1, "sv extract")
        worksheet_kq.write(0, 2, "diff code")
        worksheet_kq.write(0, 3, "diff sv")
        worksheet_kq.write(0, 4, "code -same- sv")
        worksheet_kq.write(0, 5, "code -diff- sv")
        worksheet_kq.write(0, 6, "acc")
        worksheet_kq.write(0, 7, "f1 - score")
        # worksheet_kq.write(0, 8, "precision score")
        # worksheet_kq.write(0, 9, "recall score")

        path_excel = f"{input}/{xlsx}"
        infos = []

        name, df = get_excel(path_excel)
        infos = get_info(df, infos)
        data, _, kq = get_data(infos)

        # -------------------------------------------------
        path_excel1 = f"{input_sv}/{xlsx}"
        infos1 = []
        name1, df1 = get_excel(path_excel1)
        infos1 = get_info(df1, infos1)
        _, sv, _ = get_data(infos1)
        # -------------------------------------------------

        for id, _ in enumerate(data):
            bn += 1

            data[id] = data[id].lower()
            data[id] = ViUtils.remove_accents(data[id]).decode('utf-8')
            # print(data[id])

            kq[id] = kq[id].lower()
            kq[id] = ViUtils.remove_accents(kq[id]).decode('utf-8')

            TMP = get_symptoms(data[id])
            worksheet_kq.write(rol_kq, col, str(TMP).replace(
                "[", "").replace("]", "").replace("'", ""))
            worksheet_kq.write(rol_kq, col+1, str(sv[id]).replace("  ", " "))

            nampq_extract = Convert(str(TMP).replace(
                "[", "").replace("]", "").replace("'", ""))
            sv_extract = Convert(str(sv[id]).replace("  ", " "))
            # print(nampq_extract, sv_extract)

            nampq_extract_cp = nampq_extract.copy()
            sv_extract_cp = sv_extract.copy()

            count_same = 0
            count_total = len(sv_extract)

            thua = ""
            thieu = ""

            for idn, n in enumerate(nampq_extract):
                n = n.lower().strip()
                n = ViUtils.remove_accents(n).decode('utf-8')

                for ids, s in enumerate(sv_extract):
                    s = s.lower().strip()
                    s = ViUtils.remove_accents(s).decode('utf-8')

                    if n in s:
                        count_same += 1
                        nampq_extract[idn] = "0"
                        sv_extract[ids] = "0"

            for n in nampq_extract:
                if n != "0":
                    thua += n
                    thua += ", "

            for s in sv_extract:
                if s != "0":
                    thieu += s
                    thieu += ", "

            worksheet_kq.write(rol_kq, col+2, str(thua))
            worksheet_kq.write(rol_kq, col+3, str(thieu))
            worksheet_kq.write(rol_kq, col+4, count_same)
            worksheet_kq.write(rol_kq, col+5, count_total)

            pred = [0]*21
            ground = [0]*21

            for idn, n in enumerate(nampq_extract_cp):
                nampq_extract_cp[idn] = n.lower().strip()

            for idn, n in enumerate(sv_extract_cp):
                sv_extract_cp[idn] = n.lower().replace(
                    "-", "").replace("  ", " ").strip()

            # print(nampq_extract_cp)
            # print(sv_extract_cp)

            for idx, field in enumerate(fields):
                if field.lower() in nampq_extract_cp:
                    worksheet.write(row, col+idx, 1)
                    total_pred.append(1)
                    pred[idx] = 1
                else:
                    worksheet.write(row, col+idx, 0)
                    total_pred.append(0)
                    pred[idx] = 0

                if field.lower() in sv_extract_cp:
                    total_ground.append(1)
                    ground[idx] = 1
                else:
                    total_ground.append(0)
                    ground[idx] = 0

            # print(pred)
            # print(ground)

            acc = accuracy_score(ground, pred)
            f1 = f1_score(ground, pred, average=average)
            # p_s = precision_score(ground, pred)
            # r_s = recall_score(ground, pred)
            # print(acc, f1)

            worksheet_kq.write(rol_kq, col+6, acc)
            worksheet_kq.write(rol_kq, col+7, f1)
            # worksheet_kq.write(rol_kq, col+8, p_s)
            # worksheet_kq.write(rol_kq, col+9, r_s)

            rol_kq += 1

            # print(TMP)

            if "khong" in kq[id]:
                worksheet.write(row, col+len(fields), 0)

                if acc == 1:
                    correct_bn += 1
            else:
                if "ung thu" in kq[id]:
                    worksheet.write(row, col+len(fields), 1)

                    if acc == 1:
                        correct_bn += 1

                else:
                    error += 1
                    print("-------> ", id+2, path_excel, kq[id])
                    continue

            # for idx, field in enumerate(fields):
            #     if field in TMP:
            #         worksheet.write(row, col+idx, 1)
            #     else:
            #         worksheet.write(row, col+idx, 0)

            row += 1

        workbook_kq.close()

    workbook.close()

    print("\n Correct: ", correct_bn)
    print("\n Total error: ", error)
    print("\n Total bn: ", bn)

    print("\n-------------TOTAL----------------\n")
    acc = accuracy_score(total_ground, total_pred)
    f1 = f1_score(total_ground, total_pred, average=average)
    print("ACC -------> ", acc)
    print("F1-SCORE --> ", f1)
    # print("precision_score --> ", p_s)
    # print("recall_score --> ", r_s)
    print("\n--------------END-----------------")
