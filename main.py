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


def convert_to_RGB(data):
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0, len(data)) if i % 3 == d], [0, 1, 2]))
    pixels = tuple(zip(r, g, b))
    return pixels


def process_image(filename):
    f = open(filename, 'rb')
    im3 = Image.open(filename)
    data = f.read()
    new = convert_to_RGB(bytearray(data))
    im2 = Image.new(im3.mode, im3.size)
    im2.putdata(new)
    im2.save("filename_out312.jpeg", 'jpeg')
    print(len(data))
    img_bytes = aes_ecb_encrypt(key, pad(data))
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
    return dictionary


def encrypt_dict(dictionary):
    return aes_ecb_encrypt(key, dictionary)


def decode_image():
    im3 = Image.open(filename)
    f = open('./1_enc', 'rb')
    dictionary = f.read()
    im = open('./1_enc_img', 'rb')
    data2 = im.read()
    dict = {}
    c = 0
    l = 0
    for i in range(16, len(dictionary) + 1, 16):
        temp_dict = {(dictionary[l: i]): c.to_bytes(1, byteorder='little')}
        dict.update(temp_dict)
        # print(temp_dict, c)
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
    f = open('res', 'wb')
    f.write(result)
    print(len(result))
    stream = BytesIO(result)
    image = Image.open(stream).convert("RGBA")
    stream.close()
    image.show()
    picture = image.save("{}.bmp".format("eqwe"))
    new = convert_to_RGB(result)
    im2 = Image.new(im3.mode, im3.size)
    im2.putdata(new)
    im2.save(filename_out + ".jpeg", 'jpeg')


def decode(file):
    im = Image.open(file)
    data = im.convert("RGB").tobytes()
    original = len(data)


def main():
    f = open('./1_enc', 'wb')
    f.write(encrypt_dict(create_dictionary()))
    f.close()
    process_image(filename)
    decode_image()


main()