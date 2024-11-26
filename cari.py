import hashlib
import hmac
import base64
import random
import requests

# Fungsi untuk menghasilkan tanda tangan (sign) menggunakan MD5
def generate_md5(account, md5pwd, game_token, lang="id"):
    data = account + md5pwd + game_token + lang
    sign = hashlib.md5(data.encode()).hexdigest()
    return sign

# Fungsi untuk menghasilkan tanda tangan (sign) menggunakan SHA1
def generate_sha1(account, md5pwd, game_token, lang="id"):
    data = account + md5pwd + game_token + lang
    sign = hashlib.sha1(data.encode()).hexdigest()
    return sign

# Fungsi untuk menghasilkan tanda tangan (sign) menggunakan SHA256
def generate_sha256(account, md5pwd, game_token, lang="id"):
    data = account + md5pwd + game_token + lang
    sign = hashlib.sha256(data.encode()).hexdigest()
    return sign

# Fungsi untuk menghasilkan tanda tangan (sign) menggunakan SHA512
def generate_sha512(account, md5pwd, game_token, lang="id"):
    data = account + md5pwd + game_token + lang
    sign = hashlib.sha512(data.encode()).hexdigest()
    return sign

# Fungsi untuk menghasilkan tanda tangan (sign) menggunakan HMAC-SHA256
def generate_hmac(account, md5pwd, game_token, lang="id", secret_key="my_secret_key"):
    data = account + md5pwd + game_token + lang
    sign = hmac.new(secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()
    return sign

# Fungsi untuk menghasilkan tanda tangan (sign) menggunakan Base64 encoding dari SHA256
def generate_base64_sha256(account, md5pwd, game_token, lang="id"):
    data = account + md5pwd + game_token + lang
    hash_result = hashlib.sha256(data.encode()).digest()  # Dapatkan hasil SHA256 sebagai byte
    sign = base64.b64encode(hash_result).decode()  # Convert to base64
    return sign

# Data yang akan digunakan untuk pengujian
accounts = ["garfitzyescobar@gmail.com", "example1@gmail.com", "example2@gmail.com"]
md5pwds = ["c7f058ca599176d400f6ae5826c733d3", "d3b07384d113edec49eaa6238ad5ff00", "a56ff4dabc634cd4e6e8b7643f23d91d"]
game_tokens = [
    "AQ1jcZQHdLIef32d6ZQ6PoQFDtuZr1fzQT8xrShFmDW5UguLqjGeqLBsS9LC4d-LxqKp3tYOMys",
    "AZccvdeUDOISN6T3EgtaQszMsk-cOTh-q4R4Op3alUqw2kQodt6tt_LJ2LiyPWcnQUaEAygP-b0",
    "ATAcq9ftL53iS3JuGIeNvuCkcc4k-3-v8-91yW7Ejhh8IFelLgzJMV0EGdTmJyUjaz-QX84PgFk"
]

# Loop untuk menguji semua kombinasi dan semua metode
for account in accounts:
    for md5pwd in md5pwds:
        for game_token in game_tokens:
            # Generate sign menggunakan berbagai metode
            md5_sign = generate_md5(account, md5pwd, game_token)
            sha1_sign = generate_sha1(account, md5pwd, game_token)
            sha256_sign = generate_sha256(account, md5pwd, game_token)
            sha512_sign = generate_sha512(account, md5pwd, game_token)
            hmac_sign = generate_hmac(account, md5pwd, game_token)
            base64_sha256_sign = generate_base64_sha256(account, md5pwd, game_token)

            # Cetak hasil dari setiap metode
            print(f"Testing {account} with game_token {game_token}:")
            print(f"MD5 Sign: {md5_sign}")
            print(f"SHA1 Sign: {sha1_sign}")
            print(f"SHA256 Sign: {sha256_sign}")
            print(f"SHA512 Sign: {sha512_sign}")
            print(f"HMAC Sign: {hmac_sign}")
            print(f"Base64 SHA256 Sign: {base64_sha256_sign}")
            print("-" * 50)

            # Kirim permintaan POST untuk pengujian (misalnya menguji di endpoint API)
            params = {
                "account": account,
                "md5pwd": md5pwd,
                "game_token": game_token,
                "sign": md5_sign,  # Anda bisa mengganti dengan sign dari metode yang diuji
                "lang": "id"
            }
            response = requests.post("https://api.example.com/login", json=params)  # Ganti dengan endpoint yang valid
            print(f"Response: {response.status_code}, {response.text}")
            print("=" * 50)
