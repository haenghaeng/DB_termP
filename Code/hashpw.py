import hashlib

def hash_password(password):
    # SHA-256 해시 객체 생성
    sha256_hash = hashlib.sha256()
    
    # 비밀번호를 바이트로 변환 후 해싱
    sha256_hash.update(password.encode('utf-8'))
    
    # 해시값을 16진수로 반환
    return sha256_hash.hexdigest()