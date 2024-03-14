import os


def get_tc(data):
    """
    Extracts symptoms and medical conditions from provided data and returns a list indicating their presence.

    Parameters:
        data (str): Input text data containing symptoms and medical conditions.

    Returns:
        list: A list indicating the presence (1) or absence (0) of symptoms and medical conditions.
    """

    TMP = []

    # Define symptoms and medical conditions along with their variants
    symptoms = [
        ("dau bung", "tuc bung"),
        ("non"),
        ("chan an", "an uong kem", "an ngu kem"),
        ("tao bon",),
        ("sut can", "giam can"),
        ("tieu chay"),
        ("phan co mau", "di ngoai ra mau"),
        ("da niem mac vang",),
        ("da sam",),
        ("hach ngoai bien"),
        ("hach thuong don"),
        ("bung chuong", "day bung"),
        ("phan ung thanh bung",),
        ("cam ung phuc mac",),
        ("dau hieu ran bo",),
        ("quai ruot noi",),
        ("so thay u", "so thay khoi u", "co khoi u", "co u"),
        ("tham truc trang co kho u",),
        ("chup ct o bung co khoi u", "chup ct o bung co u"),
        ("noi soi dai trang co khoi u", "noi soi dai trang co u"),
    ]

    for symptom_group in symptoms:
        for symptom in symptom_group:
            if symptom in data:
                # Check for negations or variations of the symptom and update presence indicator accordingly
                if "khong " + symptom not in data and symptom + " (-)" not in data and symptom + " am tinh" not in data:
                    TMP.append(1)
                else:
                    TMP.append(0)
                break
        else:
            TMP.append(0)

    # Define symptoms with exclusions
    symptoms_ex = [
        ("tien su ung thu", "tien su k", "ung thu dai trang", "k dai trang"),
    ]
    for symptom_ex_group in symptoms_ex:
        for symptom_ex in symptom_ex_group:
            if symptom_ex in data:
                if "khong " + symptom_ex not in data and symptom_ex + " (-)" not in data and symptom_ex + " am tinh" not in data:
                    # Check for the presence of specific keywords to distinguish medical condition from symptom
                    if not "chan doan" in data and not "chuan doan" in data:
                        TMP.append(1)
                    else:
                        TMP.append(0)
                else:
                    TMP.append(0)
                break
        else:
            TMP.append(0)
    return TMP


def get_last_modified_model(directory, prefix):
    """
    Get the path to the most recently modified model file in a directory.

    Parameters:
        directory (str): The directory containing the model files.
        prefix (str): The prefix that model files must start with.

    Returns:
        str or None: The path to the most recently modified model file, or None if no such file exists.
    """
    models = [file for file in os.listdir(directory) if file.startswith(
        prefix) and file.endswith('.joblib')]
    latest_model = max(models, default=None, key=lambda x: os.path.getmtime(
        os.path.join(directory, x)))
    return os.path.join(directory, latest_model)
