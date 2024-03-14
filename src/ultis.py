import os
import joblib


def get_tc(data):
    TMP = []

    if "dau bung" in data or "tuc bung" in data:
        if not "khong dau bung" in data and not "khong tuc bung" in data:
            TMP.append(1)
        else:
            TMP.append(0)
    else:
        TMP.append(0)

    if "non" in data and not "khong non" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "chan an" in data or "an uong kem" in data or "an ngu kem" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "tao bon" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "sut can" in data or "giam can" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "tieu chay" in data and not "khong tieu chay" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "phan co mau" in data or "di ngoai ra mau" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "da niem mac vang" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "da sam" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "hach ngoai bien" in data:
        if not "hach ngoai bien am tinh" in data and not "hach ngoai bien (-)" in data:
            TMP.append(1)
        else:
            TMP.append(0)
    else:
        TMP.append(0)

    if "hach thuong don" in data:
        if not "hach thuong don am tinh" in data and not "hach thuong don (-)" in data:
            TMP.append(1)
        else:
            TMP.append(0)
    else:
        TMP.append(0)

    if "bung chuong" in data or "day bung" in data:
        if not "khong day bung" in data:
            TMP.append(1)
        else:
            TMP.append(0)
    else:
        TMP.append(0)

    if "phan ung thanh bung" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "cam ung phuc mac" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "dau hieu ran bo" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "quai ruot noi" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "so thay u" in data or "so thay khoi u" in data or "co khoi u" in data or "co u" in data:
        if not "khong so thay u" in data and not "khong so thay khoi u" in data and not "khong co khoi u" in data and not "khong co u" in data:
            TMP.append(1)
        else:
            TMP.append(0)
    else:
        TMP.append(0)

    if "tham truc trang co kho u" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "tien su ung thu" in data or "tien su k" in data or "ung thu dai trang" in data or "k dai trang" in data:
        if not "khong tien su ung thu" in data and not "khong tien su k" in data and not "khong ung thu dai trang" in data:
            if not "chan doan" in data and not "chuan doan" in data:
                TMP.append(1)
            else:
                TMP.append(0)
        else:
            TMP.append(0)
    else:
        TMP.append(0)

    if "chup ct o bung co khoi u" in data or "chup ct o bung co u" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    if "noi soi dai trang co khoi u" in data or "noi soi dai trang co u" in data:
        TMP.append(1)
    else:
        TMP.append(0)

    return TMP


def get_last_modified_model(directory, prefix):
    models = [file for file in os.listdir(directory) if file.startswith(
        prefix) and file.endswith('.joblib')]
    if not models:
        return None
    latest_model = max(models, key=lambda x: os.path.getmtime(
        os.path.join(directory, x)))
    return os.path.join(directory, latest_model)
