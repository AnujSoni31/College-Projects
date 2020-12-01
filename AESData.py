from Crypto.Cipher import AES
from Crypto.Hash import SHA256

message = input('Enter the Message: ')
hashObj = SHA256.new(message.encode('utf-8'))
hashKey =  hashObj.digest()

def encrypt(info):
	information = info
	block_size = 16
	pad = '_'
	padding = lambda s: s + (block_size - len(s) % block_size) * pad
	cipher = AES.new(hashKey, AES.MODE_ECB)
	result = cipher.encrypt(padding(information).encode('utf-8'))
	return result

cipher_text = encrypt(message)
print(cipher_text)