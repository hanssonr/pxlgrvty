from libs.Crypt import Crypt
import os

def crypter(filepath):
    crypt = Crypt()
    
    with open(filepath, "r") as reader:
        plaintext = reader.read()
    
    return crypt.encrypt(plaintext)


crypt = Crypt()

#level
for root, _, files in os.walk("assets/levels/decrypted"):
    for file in files:
        decryptpath = os.path.join(root, file)
        encryptpath = os.path.join("assets/levels/", file)
        with open(encryptpath, "wb+") as w:
            w.write(crypter(decryptpath))

#state
"""
#data = crypter("assets/state/state.json")
with open("assets/state/state.json", "wb+") as w:
    w.write(crypt.encrypt('{"LVL":"1"}'))"""

#time
"""
with open("assets/state/time.json", "wb+") as w:
    w.write(crypter("assets/state/orgtime.json"))"""

