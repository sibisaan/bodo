import hashlib
import hmac
import base64
import requests
import json
import time
from itertools import product

# Fungsi untuk meng-hash password menggunakan berbagai metode
def generate_sign_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

def generate_sign_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest()

def generate_sign_sha256(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_sign_sha512(password):
    return hashlib.sha512(password.encode()).hexdigest()

def generate_sign_hmac(password, secret_key):
    return hmac.new(secret_key.encode(), password.encode(), hashlib.sha256).hexdigest()

def generate_sign_base64(password):
    sha256_hash = hashlib.sha256(password.encode()).digest()
    return base64.b64encode(sha256_hash).decode()

# Fungsi untuk menambahkan parameter stampdate
def add_stampdate():
    return int(time.time())  # Menggunakan timestamp UNIX sebagai stampdate

# Fungsi untuk menambah variasi parameter dan mencoba pengujian
def generate_combinations(account, password, game_token, extra_params):
    # Daftar metode hashing yang akan diuji
    sign_methods = ['md5', 'sha1', 'sha256', 'sha512', 'hmac', 'base64']

    # Membuat variasi parameter tambahan, misalnya:
    # - Kombinasi recaptcha_token dan country yang berbeda
    recaptcha_tokens = ['', 'token1', 'token2', 'token3']
    countries = ['', 'ID', 'US', 'SG']
    combinations = list(product(recaptcha_tokens, countries))

    # Menyiapkan kombinasi yang lebih banyak, bisa 100 kombinasi
    attempts = 0
    results = []

    for recaptcha_token, country in combinations:
        for sign_method in sign_methods:
            # Menambah kombinasi dari berbagai cara untuk menghitung `sign`
            stampdate = add_stampdate()  # Mendapatkan timestamp sebagai stampdate
            params = {
                "account": account,
                "md5pwd": password,  # Menggunakan md5pwd sesuai format API (sudah di-hash sebelumnya)
                "game_token": game_token,
                "recaptcha_token": recaptcha_token,
                "country": country,
                "stampdate": stampdate,
                "lang": "id"
            }

            # Tentukan cara pembuatan sign
            if sign_method == 'md5':
                sign = generate_sign_md5(password)
            elif sign_method == 'sha1':
                sign = generate_sign_sha1(password)
            elif sign_method == 'sha256':
                sign = generate_sign_sha256(password)
            elif sign_method == 'sha512':
                sign = generate_sign_sha512(password)
            elif sign_method == 'hmac':
                secret_key = "secret"  # Anda perlu mengetahui secret_key yang digunakan
                sign = generate_sign_hmac(password, secret_key)
            elif sign_method == 'base64':
                sign = generate_sign_base64(password)

            # Menambahkan `sign` ke parameter
            params['sign'] = sign

            # Menyiapkan headers sesuai permintaan
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': str(len(json.dumps(params))),
                'Content-Type': 'application/json',
                'Host': 'accountmtapi.mobilelegends.com',
                'Origin': 'https://mtacc.mobilelegends.com',
                'Referer': 'https://mtacc.mobilelegends.com/',
                'sec-ch-ua': '"Chromium";v="130", "Android WebView";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; 220333QAG Build/RKQ1.211001.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.108 Mobile Safari/537.36',
                'X-Requested-With': 'com.mobile.legends'
            }

            # Mengirim permintaan POST
            try:
                response = requests.post("https://accountmtapi.mobilelegends.com/", json=params, headers=headers)

                # Menampilkan hasil respons
                if response.status_code == 200:
                    print(f"Method: {sign_method}, Sign: {sign}")
                    print(f"Response: {response.json()}")
                    results.append({
                        "params": params,
                        "response": response.json()
                    })
                    attempts += 1
                else:
                    print(f"Failed to login. Status Code: {response.status_code}")
                    print(f"Response: {response.text}")
                
                if attempts >= 100:
                    break  # Hentikan setelah 100 percobaan

            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
    
    return results

# Data untuk pengujian
account = "garfitzyescobar@gmail.com"
password = "c7f058ca599176d400f6ae5826c733d3"  # Hash MD5 password
game_token = "AQ1jcZQHdLIef32d6ZQ6PoQFDtuZr1fzQT8xrShFmDW5UguLqjGeqLBsS9LC4d-LxqKp3tYOMys"

# Menjalankan pengujian dengan berbagai kombinasi parameter
print("Starting the search for valid sign with 100 different parameter combinations...\n")
results = generate_combinations(account, password, game_token, {})

# Jika Anda ingin melihat hasil percobaan, misalnya disimpan dalam file atau dicetak
for result in results:
    print(f"Params: {result['params']}")
    print(f"Response: {result['response']}\n")
