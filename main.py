import sys

from PIL import Image, ImageFile
from Cryptodome.Cipher import AES
from io import BytesIO

filename = "jessica.bmp"
filename_out = "1_enc_img"
key = "aaaabbbbccccdddd"
ImageFile.LOAD_TRUNCATED_IMAGES = True


def pad(data):
    f = open(data, 'rb')
    data = f.read()
    bytearray_data = bytearray()
    l = 0
    for i in range(1, len(data), 1):
        bytearray_data += bytearray(data[l: i] + b"\x00" * (16 - len(data[l: i]) % 16))
        l = i
    f = open('padded_image', 'wb')
    f.write(bytearray_data)
    return bytearray_data


def process_image(filename):
    f = open(filename, 'rb')
    data = f.read()
    img_bytes = aes_ecb_encrypt(key, data)
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


def decode_image(img_file, dict_file):
    f = open(dict_file, 'rb')
    dictionary = f.read()
    im = open(img_file, 'rb')
    data2 = im.read()
    dict = {}
    c = 0
    l = 0
    dict_file = open('./dict.txt', 'a')
    for i in range(16, len(dictionary) + 1, 16):
        temp_dict = {(dictionary[l: i]): c.to_bytes(1, byteorder='little')}
        dict.update(temp_dict)
        # print(temp_dict, c)  // вывести шифрованные байты - байты - 10 сист
        dict_file.write("{} - {}\n".format(temp_dict, c))
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


def create_readable_dict(file):
    f = open(file, 'rb')
    dictionary = f.read()
    dict = {}
    c = 0
    l = 0
    dict_file = open('./dict.txt', 'a')
    for i in range(16, len(dictionary) + 1, 16):
        temp_dict = {(dictionary[l: i]): c.to_bytes(1, byteorder='little')}
        dict.update(temp_dict)
        # print(temp_dict, c)  // вывести шифрованные байты - байты - 10 сист
        dict_file.write("{} - {}\n".format(temp_dict, c))
        c += 1
        l = i


def main():

    if sys.argv[1] == "prepare":
        pad(sys.argv[2])
        f = open('./dict', 'wb')
        f.write(create_dictionary())
        f.close()
        return

    if sys.argv[1] == "encode":
        f = open(sys.argv[2], 'wb')
        f.write(encrypt_dict(create_dictionary()))
        f.close()
        process_image(sys.argv[3])
        return

    if sys.argv[1] == "translate":
        create_readable_dict(sys.argv[2])
        return

    if sys.argv[1] == "decode":
        decode_image(sys.argv[2], sys.argv[3])
        return


main()