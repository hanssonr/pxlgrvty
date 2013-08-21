"""
Helpclass for encrypthing levels

Author: Rickard Hansson, rkh.hansson@gmail.com
"""

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

print "done"