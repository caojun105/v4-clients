import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class MnemonicManager:
    
    def __init__(self, json_file_path = 'addr_mnemonic.json', password=None, salt=b'salt_value'):
        self.json_file_path = json_file_path
        self.password = password.encode() if password else None
        self.salt = salt
        self.cipher_suite = self.generate_cipher_suite() if password else None
        self.data = self.load_data()

    def generate_cipher_suite(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,  # You can adjust the number of iterations based on your security requirements
            salt=self.salt,
            length=32
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        print(f"Generated Key: {key}")
        return Fernet(key)

    def load_data(self):
        try:
            with open(self.json_file_path, 'r') as file:
                encrypted_data = json.load(file)

                if self.password:
                    decrypted_data = {address: self.decrypt_mnemonic(data['MNEMONIC']) for address, data in encrypted_data.items()}
                else:
                    decrypted_data = {address: data['MNEMONIC'] for address, data in encrypted_data.items()}
                return decrypted_data
        except FileNotFoundError:
            print("not find the file")
            return {}

    def save_data(self):
        encrypted_data = {address: {'MNEMONIC': self.encrypt_mnemonic(mnemonic)} for address, mnemonic in self.data.items()}
        with open(self.json_file_path, 'w') as file:
            json.dump(encrypted_data, file, indent=2)

    def encrypt_mnemonic(self, mnemonic):
        return self.cipher_suite.encrypt(mnemonic.encode()).decode()

    def decrypt_mnemonic(self, encrypted_mnemonic):
        return self.cipher_suite.decrypt(encrypted_mnemonic.encode()).decode()

    def get_mnemonic(self, address):
        try:
            return self.data[address]
        except KeyError:
            raise KeyError(f"Address '{address}' not found in the JSON file.")

    def get_unencrypted_mnemonic(self, address):
        try:
            with open(self.json_file_path, 'r') as file:
                unencrypted_data = json.load(file)
                return unencrypted_data.get(address, {}).get('MNEMONIC', None)
        except FileNotFoundError:
            return None

class MnemonicManagerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MnemonicManagerSingleton, cls).__new__(cls)
            cls._instance.mnemonic_manager = MnemonicManager(*args, **kwargs)
        return cls._instance

    def get_mnemonic_manager(self):
        return self._instance.mnemonic_manager

# # Example usage:
# json_file_path = 'addr_mnemonic.json'  # Replace with the path to your JSON file
# password = 'your_password'  # Replace with your password


# mnemonic_manager = MnemonicManager(json_file_path)
# try:
#     address_to_query = 'address1'
#     mnemonic = mnemonic_manager.get_mnemonic(address_to_query)
#     print(f"MNEMONIC for {address_to_query}: {mnemonic}")
# except KeyError as e:
#     print(e)

# unencrypted_mnemonic = mnemonic_manager.get_unencrypted_mnemonic(address_to_query)
# print(f"Unencrypted MNEMONIC for {address_to_query}: {unencrypted_mnemonic}")
