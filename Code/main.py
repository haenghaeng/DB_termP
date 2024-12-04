import psycopg2
import psycopg2.sql
import hashpw

# 입력 받은 유저명과 비밀번호를 DB에서 확인합니다. 일치하면 True, 일치하지 않으면 False를 리턴합니다.
def try_connection(user_name, user_password):
    try:        
        connection = psycopg2.connect(
            database = "db_termp",
            user = 'login',
            password = 'login',
            host = "::1",
            port = "5432"
            )
        
        cursor = connection.cursor()
        
        # 입력값과 SQL 구문을 분리해야 SQL injection 위험이 없다고 하네용
        query = psycopg2.sql.SQL(
            '''
            select user_name
            from id_pw_view ipv 
            where ipv.user_name = %s;
            '''
        )    
        cursor.execute(query, (user_name,)) # 전달할 땐 tuple로 보내야 함
        
        if cursor.fetchone():            
            query = psycopg2.sql.SQL(
                '''
                select user_name, user_password
                from id_pw_view ipv
                where ipv.user_name = %s and ipv.user_password = %s;
                '''
            )            
            cursor.execute(query, (user_name, hashpw.hash_password(user_password)))
            
            # 결과가 존재하면 True
            if cursor.fetchone() :
                return True
            else:
                print("\n비밀번호가 틀렸습니다.")
                return False  
        else:
            print("\n사용자가 존재하지 않습니다.")
            return False
        
    except Exception as e:
        print(f"\n데이터베이스와 연결에 실패하였습니다. : {e}")
        return False
    
    finally:
        connection.close()

# 사용자에게서 사용자명과 비밀번호를 받아 연결을 시도합니다.
def login():  
    user_name = input("사용자명을 입력해주세요 ")
    user_password = input("비밀번호를 입력해주세요 ")

    if(try_connection(user_name, user_password)):
        print("\n로그인 성공")
    else:
        print("\n로그인 실패")


def main():
    while True:
        action = input("\n원하는 기능의 숫자를 입력해주세요 \n(1) 로그인\n(2) 종료\n")
                
        if action == "1":
            login()
        elif action == "2":
            print("종료합니다.")
            break

if __name__ == '__main__':   
    main()