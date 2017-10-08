"""
Class thats encrypt/decrypt time and level files

http://stackoverflow.com/questions/6425131/encrpyt-decrypt-data-in-python-with-salt
"""
import Crypto.Random, configparser, tempfile, os, hashlib, base64
from Crypto.Cipher import AES
from Resources import Resources

class Crypt(object):

    SALT_SIZE = 16
    NUMBER_OF_ITERATIONS = 20
    AES_MULTIPLE = 16
    PASSWORD = b"pxlgrvty-1.0"

    def encrypt(self, plaintext):
        salt = Crypto.Random.get_random_bytes(self.SALT_SIZE)
        #salt = os.urandom(self.SALT_SIZE)
        key = self.__generate_key(self.PASSWORD, salt, self.NUMBER_OF_ITERATIONS)
        cipher = AES.new(key, AES.MODE_ECB)
        padded_plaintext = self.__pad_text(plaintext, self.AES_MULTIPLE)
        ciphertext = cipher.encrypt(padded_plaintext)
        ciphertext_with_salt = salt + ciphertext
        return ciphertext_with_salt

    def decrypt(self, ciphertext):
        salt = ciphertext[0:self.SALT_SIZE]
        ciphertext_sans_salt = ciphertext[self.SALT_SIZE:]
        key = self.__generate_key(self.PASSWORD, salt, self.NUMBER_OF_ITERATIONS)
        cipher = AES.new(key, AES.MODE_ECB)
        padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
        plaintext = self.__unpad_text(padded_plaintext)
        return plaintext

    def __pad_text(self, text, multiple):
        extra_bytes = len(text) % multiple
        padding_size = multiple - extra_bytes
        padding = chr(padding_size) * padding_size
        padded_text = text + padding
        return padded_text

    def __unpad_text(self, padded_text):
        padding_size = padded_text[-1]
        text = padded_text[:-padding_size]
        return text.decode("utf-8")

    def __generate_key(self, password, salt, iterations):
        assert iterations > 0
        key = password + salt

        for i in range(iterations):
            key = hashlib.sha256(key).digest()
        return key


    def dectryptParser(self, lvlid):
        parser = configparser.ConfigParser()

        #create temp-file
        # fd, temp_path = tempfile.mkstemp(suffix=".lvl", dir="assets/levels/")

        #open crypted file, write the decrypted data to tempfile
        # with open(temp_path, "w+") as w:
        #     with open("assets/levels/decrypted/level%d.lvl" % lvlid, "rb") as reader:
        #         w.write(self.decrypt(reader.read()))

        #parse the decrypted file
        # parser.read(temp_path)
        parser.read(Resources.getInstance().resource_path("assets/levels/decrypted/level%d.lvl" % lvlid))

        #close/remove
        # os.close(fd)
        # os.remove(temp_path)

        return parser
