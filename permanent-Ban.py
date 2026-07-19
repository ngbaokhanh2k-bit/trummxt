import requests, os, sys, json, binascii, time, urllib3, base64, datetime, re, socket, ssl, asyncio, traceback, jwt , aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from xPARA import *
from xHeaders import *
from Pb2 import MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

login_url, ob, version = AuToUpDaTE()

Hr = {
    'User-Agent': Uaa(),
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': ob
}


def b64url_decode(input_str: str) -> bytes:
    rem = len(input_str) % 4
    if rem:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

def extract_jwt_payload_dict(jwt_s: str):
    try:
        parts = jwt_s.split('.')
        if len(parts) < 2:
            return None
        payload_b64 = parts[1]
        payload_bytes = b64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8', errors='ignore'))
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    return None

def encrypt_packet(hex_string: str, aes_key, aes_iv) -> str:
    if isinstance(aes_key, str):
        aes_key = bytes.fromhex(aes_key)
    if isinstance(aes_iv, str):
        aes_iv = bytes.fromhex(aes_iv)
    data = bytes.fromhex(hex_string)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return encrypted.hex()

def build_start_packet(account_id: int, timestamp_ns: int, jwt: str, key, iv) -> str:

    try:
        encrypted = encrypt_packet(jwt.encode().hex(), key, iv)
        head_len = hex(len(encrypted) // 2)[2:]
        ide_hex = hex(account_id)[2:]
        zeros = "0" * (16 - len(ide_hex))
        timestamp_hex = hex(timestamp_ns)[2:].zfill(2)   
        head = f"0115{zeros}{ide_hex}{timestamp_hex}00000{head_len}"
        start_packet = head + encrypted
        return start_packet
    except Exception as e:
        print(f"[!] Error building start packet: {e}")
        traceback.print_exc()
        return None

def send_once(remote_ip, remote_port, payload_bytes, recv_timeout=3.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(recv_timeout)
    try:
        s.connect((remote_ip, remote_port))
        s.sendall(payload_bytes)
        chunks = []
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
        except socket.timeout:
            pass
        return b"".join(chunks)
    finally:
        s.close()


async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def EncRypTMajoRLoGin(open_id, access_token, platform):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = '2.124.1'
    major_login.system_software = "Fuck Garena Free Fire"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Fuck Garena Free Fire"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "Fuck Garena Free Fire"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "Fuck Garena Free Fire"
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = str(platform) if platform else "4"
    major_login.primary_platform_type = str(platform) if platform else "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = f"{login_url}MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto


async def main():
    print("="*60)
    print("         FreeFire Login Script")
    print("="*60)
    print()
    access_token = input("[*] Enter your access token: ").strip()
    if not access_token:
        print("[!] Error: Access token cannot be empty!")
        return

    
    inspect_url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
    inspect_headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)"
    }
    try:
        resp = requests.get(inspect_url, headers=inspect_headers, timeout=10)
        data = resp.json()
        print("[INFO] Inspect response:", json.dumps(data, indent=2))
        if 'error' in data:
            print("[!] Token error:", data.get('error'))
            return
    except Exception as e:
        print("[!] Failed to inspect access token:", e)
        return

    open_id = data.get('open_id')
    platform = data.get('platform')
    if not open_id:
        print("[!] No open_id found in inspect response.")
        return
    print(f"[✓] Open ID: {open_id}")
    print(f"[✓] Platform: {platform}")

    
    print("\n[2] Performing MajorLogin...")
    PyL = await EncRypTMajoRLoGin(open_id, access_token, platform)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE:
        print("[!] MajorLogin failed (account banned / not registered?)")
        return

    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    print(f"[✓] Account ID: {MajoRLoGinauTh.account_uid}")
    print(f"[✓] JWT: {MajoRLoGinauTh.token[:50]}...")
    print(f"[✓] Key: {MajoRLoGinauTh.key.hex()}")
    print(f"[✓] IV: {MajoRLoGinauTh.iv.hex()}")

    
    print("\n[3] Getting login data...")
    LoGinDaTa = await GetLoginData(MajoRLoGinauTh.url, PyL, MajoRLoGinauTh.token)
    if not LoGinDaTa:
        print("[!] Failed to get login data (ports).")
        return
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    online_ip, online_port = OnLinePorTs.split(":")
    online_port = int(online_port)
    print(f"[✓] Online IP: {online_ip}")
    print(f"[✓] Online Port: {online_port}")

    
    print("\n[4] Building final packet...")
    payload_jwt = extract_jwt_payload_dict(MajoRLoGinauTh.token)
    if payload_jwt is None:
        print("[!] Failed to decode JWT payload")
        return
    account_id = int(payload_jwt.get("account_id", 0))
    exp = int(payload_jwt.get("exp", 0))          
    timestamp_ns = exp * 1_000_000_000           
    final_token_hex = build_start_packet(
        account_id=account_id,
        timestamp_ns=timestamp_ns,
        jwt=MajoRLoGinauTh.token,
        key=MajoRLoGinauTh.key,
        iv=MajoRLoGinauTh.iv
    )
    if not final_token_hex:
        print("[!] Failed to build start packet")
        return
    print(f"[✓] Packet built successfully (length: {len(final_token_hex)} hex chars)")

    
    print("\n[5] Connecting to game server...")
    try:
        payload_bytes = bytes.fromhex(final_token_hex)
        print(f"[*] Sending packet to {online_ip}:{online_port}...")
        response = send_once(online_ip, online_port, payload_bytes, recv_timeout=5.0)
        if response:
            print(f"[✓] Got {len(response)} bytes response:")
            print("\n" + "="*80)
            print("✅ Done ban")
            print("This Ban Src Is By Unknown666")
        else:
            print("[!] No response from server")
    except Exception as e:
        print(f"[!] Connection error: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())