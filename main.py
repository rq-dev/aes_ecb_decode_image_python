from PIL import Image, ImageFile
from Cryptodome.Cipher import AES
from io import BytesIO

filename = "jessica.bmp"
filename_out = "1_enc_img"
key = "aaaabbbbccccdddd"
ImageFile.LOAD_TRUNCATED_IMAGES = True


def pad(data):
    bytearray_data = bytearray()
    l = 0
    for i in range(1, len(data), 1):
        bytearray_data += bytearray(data[l: i] + b"\x00" * (16 - len(data[l: i]) % 16))
        l = i
    return bytearray_data


def process_image(filename):
    f = open(filename, 'rb')
    data = f.read()
    img_bytes = aes_ecb_encrypt(key, pad(data))
    # print(img_bytes)   // вывести зашифрованные байты
    f = open(filename_out, 'wb')
    f.write(img_bytes)


def aes_ecb_encrypt(key, data, mode=AES.MODE_ECB):
    aes = AES.new(key.encode("utf8"), mode)
    new_data = aes.encrypt(data)
    return new_data


def create_dictionary():
    dictionary = bytearray()
    for i in range(256):
        dictionary += bytearray(i.to_bytes(16, byteorder='little'))
    # print(dictionary)   // вывести словарь
    return dictionary


def encrypt_dict(dictionary):
    return aes_ecb_encrypt(key, dictionary)


def decode_image():
    f = open('./dict', 'rb')
    dictionary = f.read()
    im = open('./1_enc_img', 'rb')
    data2 = im.read()
    dict = {}
    c = 0
    l = 0
    for i in range(16, len(dictionary) + 1, 16):
        temp_dict = {(dictionary[l: i]): c.to_bytes(1, byteorder='little')}
        dict.update(temp_dict)
        # print(temp_dict, c)  // вывести шифрованные байты - байты - 10 сист
        c += 1
        l = i
    c = 0
    l = 0
    result = bytearray()
    for i in range(16, len(data2), 16):
        # print(dict[data2[l: i]], data2[l: i])
        result += dict[data2[l: i]]
        c += 1
        l = i
    stream = BytesIO(result)
    image = Image.open(stream).convert("RGBA")
    stream.close()
    picture = image.save("{}.bmp".format("decoded_image"))


def main():
    f = open('./dict', 'wb')
    f.write(encrypt_dict(create_dictionary()))
    f.close()
    process_image(filename)
    decode_image()


main()