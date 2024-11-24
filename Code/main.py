import psycopg2
import hashlib

def hash_password(password):
    # SHA-256 해시 객체 생성
    sha256_hash = hashlib.sha256()
    
    # 비밀번호를 바이트로 변환 후 해싱
    sha256_hash.update(password.encode('utf-8'))
    
    # 해시값을 16진수로 반환
    return sha256_hash.hexdigest()

# 입력 받은 유저명과 비밀번호를 DB에서 확인합니다. 일치하면 True, 일치하지 않으면 False를 리턴합니다.
def try_connection(user_name, user_password):
    connection = psycopg2.connect(
        database = "db_termp",
        user = 'admin',
        password = 'admin',
        host = "::1",
        port = "5432"
        )
    
    cursor = connection.cursor()
    
    cursor.execute(
        f'''
        select user_name
        from users u
        where u.user_name = '{user_name}';
        '''
    )
    
    if len(cursor.fetchall()) > 0:
        cursor.execute(
            f'''
            select *
            from users u
            where u.user_name = '{user_name}' and u.password = '{hash_password(user_password)}';
            '''
        )
        
        if len(cursor.fetchall()) > 0:
            return True
        else:
            print("비밀번호가 틀렸습니다.")
            return False  
    else:
        print("사용자가 존재하지 않습니다.")
        return False


# 사용자에게서 사용자명과 비밀번호를 받아 연결을 시도합니다.
def login():  
    user_name = input("사용자명을 입력해주세요 ")
    user_password = input("비밀번호를 입력해주세요 ")

    if(try_connection(user_name, user_password)):
        print("로그인 성공")
    else:
        print("로그인 실패")

if __name__ == '__main__':   
    while True:
        action = input("\n원하는 기능의 숫자를 입력해주세요 \n(1) 로그인\n(2) 종료\n")
        
        if action == "1":
            login()
        if action == "2":
            print("종료합니다.")
            break