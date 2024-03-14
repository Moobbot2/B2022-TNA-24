from pyvi import ViUtils
c = ViUtils.remove_accents("Bệnh nhân nam 60 tuổi. Tiền sử K đại tràng di căn gan")
print(c.decode('utf-8'))

# import unicodedata
# def remove_accents(text):
#     return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')