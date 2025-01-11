import json
# from cryptography.fernet import Fernet


class EncryptionStrategy():
    def __init__(self):
        pass
    
    @staticmethod
    def generate_key():
        pass
        # key = Fernet.generate_key()
        
        # with open('encryption_key.key', 'wb') as key_file:
        #     key_file.write(key)
        
        # return key
    
    @staticmethod
    def load_key():
        pass
        # with open('encryption_key.key', 'rb') as key_file:
        #     return key_file.read()
        
    @staticmethod    
    def encrypt_json(data, key):
        pass
        # json_str = json.dumps(data)
        
        # f = Fernet(key)
        
        # encrypted_data = f.encrypt(json_str.encode())
        # return encrypted_data
    
    @staticmethod
    def decrypt_json(encrypted_data, key):
        pass
        # f = Fernet(key)
        
        # decrypted_data = f.decrypt(encrypted_data)
        
        # json_data = json.loads(decrypted_data.decode())
        # return json_data
    
    @staticmethod
    def save_encrypted_data(encrypted_data, filename):
        pass
        # with open(filename, 'wb') as file:
        #     file.write(encrypted_data)
            
    @staticmethod        
    def load_encrypted_data(filename):
        pass
        # with open(filename, 'rb') as file:
        #     return file.read()