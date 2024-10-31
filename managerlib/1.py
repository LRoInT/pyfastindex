from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def generate_key_pair():
    # 生成RSA密钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def sign_file(file_path, private_key):
    # 使用私钥对文件进行签名
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(file_bytes)
    file_hash = digest.finalize()
    signature = private_key.sign(file_hash, padding.PSS(mgf=padding.MGF1(
        hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return signature


def verify_file(file_path, signature, public_key):
    # 使用公钥验证文件的签名
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(file_bytes)
    file_hash = digest.finalize()
    try:
        public_key.verify(signature, file_hash, padding.PSS(mgf=padding.MGF1(
            hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception as e:
        print(e)
        return False
