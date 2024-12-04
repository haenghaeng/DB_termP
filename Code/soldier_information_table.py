import psycopg2
import psycopg2.sql
import psycopg2.errors

import hashpw

def crud_operation(operation_type):
    try:        
        connection = psycopg2.connect(
            database = "db_termp",
            user = 'admin',
            password = 'admin',
            host = "::1",
            port = "5432"
            )
        cursor = connection.cursor()
        
        if operation_type == 'c':
            create_soldier(cursor)
        elif operation_type == 'r':
            read_soldier(cursor)
        elif operation_type == 'u':
            update_soldier(cursor)
        elif operation_type == 'd':
            delete_soldier(cursor)
        else:
            return              
        
    except Exception as e:
        print(f"\n데이터베이스와 연결에 실패하였습니다. : {e}")
    
    finally:
        connection.commit() # ?? 트랜젝션 써야지 않을까?
        connection.close()

def create_soldier(cursor):
    while True:
        name = input("병사의 이름을 입력해주세요(10자 이하) : ")
        rank = input("병사의 계급을 입력해주세요(이병/일병/상병/병장) : ")
        user_name = input("병사가 로그인 시 사용할 ID를 입력해주세요(20자 이하) : ")
        user_password = input("병사가 로그인 시 사용할 비밀번호를 입력해주세요 : ")
        
        yes_no = input(f"다음 입력 사항이 맞습니까?(Y/N)\n\n이름 : {name}\n계급 : {rank}\nID : {user_name}\n비밀번호 : {user_password}\n")
        if yes_no == 'Y' or yes_no == 'y':
            break
        else:
            print("다시 입력해주세요")
    
    try:
        query = psycopg2.sql.SQL(
            '''
            insert into soldier_information(name, rank, user_name, user_password) values (%s, %s, %s, %s);
            '''
        )    
        cursor.execute(query, (name, rank, user_name, hashpw.hash_password(user_password)))
    
    except psycopg2.errors.StringDataRightTruncation:
        print("입력한 값이 너무 깁니다.")
        
    except psycopg2.errors.InvalidTextRepresentation:
        print("잘못된 계급을 입력하였습니다.")

def read_soldier(cursor):    
    while True:
        action = input("원하는 검색 방식의 숫자를 입력해주세요\n(1) 이름으로 검색\n(2) 병사가 사용하는 id로 검색\n(3) 검색 종료\n")
        
        if action == '1':
            name = input("병사의 이름을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select name, rank, user_name
                from soldier_information si
                where si.name = %s;
                '''
            )
            cursor.execute(query, (name, ))
            
            result = cursor.fetchall()
            if len(result) > 0:
                print(result)
            else:
                print("입력한 이름을 가진 병사가 데이터베이스에 존재하지 않습니다.")   
            
        
        elif action == '2':
            user_name = input("병사가 사용하는 id를 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select name, rank, user_name
                from soldier_information si
                where si.user_name = %s;
                '''
            )
            cursor.execute(query, (user_name, ))
            
            result = cursor.fetchall()
            if len(result) > 0:
                print(result)                
            else:
                print("입력한 ID를 사용하는 병사가 데이터베이스에 존재하지 않습니다.")  
        
        elif action == '3':
            return
        
        else:
            print("다시 입력해주세요") 

# 업데이트 시 계급, id, pw를 동시에 업데이트해야 함
# 기능 분리 필요
def update_soldier(cursor):
    while True:
        action = input("원하는 검색 방식의 숫자를 입력해주세요\n(1) 이름으로 검색\n(2) 병사가 사용하는 id로 검색\n(3) 검색 종료\n")
        
        if action == '1':
            name = input("병사의 이름을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select id, name
                from soldier_information si
                where si.name = %s;
                '''
            )
            cursor.execute(query, (name, ))
            
            result = cursor.fetchall()
            if len(result) > 1:
                print("데이터베이스에 동명이인이 존재합니다. 병사가 사용하는 id로 검색 부탁드립니다.")
                
            elif len(result) == 1:
                name = result[0][1]
                while True:
                    rank = input("병사의 계급을 입력해주세요(이병/일병/상병/병장) : ")
                    user_name = input("병사가 로그인 시 사용할 ID를 입력해주세요(20자 이하) : ")
                    user_password = input("병사가 로그인 시 사용할 비밀번호를 입력해주세요 : ")                
                    yes_no = input(f"다음 입력 사항이 맞습니까?(Y/N)\n\n이름 : {name}\n계급 : {rank}\nID : {user_name}\n비밀번호 : {user_password}\n")
                    
                    if yes_no == 'Y' or yes_no == 'y':
                        break
                    else:
                        print("다시 입력해주세요")
                
                try:
                    query = psycopg2.sql.SQL(
                        '''
                        update soldier_information si
                        set rank = %s, user_name = %s, user_password = %s
                        where si.id = %s
                        '''
                    )    
                    cursor.execute(query, (rank, user_name, hashpw.hash_password(user_password), result[0][0]))
        
                except psycopg2.errors.StringDataRightTruncation:
                    print("입력한 값이 너무 깁니다.")
                    
                except psycopg2.errors.InvalidTextRepresentation:
                    print("잘못된 계급을 입력하였습니다.")
                    
            else:
                print("입력한 이름을 가진 병사가 데이터베이스에 존재하지 않습니다.")   
            
        
        elif action == '2':
            user_name = input("병사가 사용하는 id를 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                select id, name
                from soldier_information si
                where si.user_name = %s;
                '''
            )
            cursor.execute(query, (user_name, ))
            
            result = cursor.fetchone()
            if result:
                name = result[1]
                while True:
                    rank = input("병사의 계급을 입력해주세요(이병/일병/상병/병장) : ")
                    user_name = input("병사가 로그인 시 사용할 ID를 입력해주세요(20자 이하) : ")
                    user_password = input("병사가 로그인 시 사용할 비밀번호를 입력해주세요 : ")                
                    yes_no = input(f"다음 입력 사항이 맞습니까?(Y/N)\n\n이름 : {name}\n계급 : {rank}\nID : {user_name}\n비밀번호 : {user_password}\n")
                    
                    if yes_no == 'Y' or yes_no == 'y':
                        break
                    else:
                        print("다시 입력해주세요")
                
                try:
                    query = psycopg2.sql.SQL(
                        '''
                        update soldier_information si
                        set rank = %s, user_name = %s, user_password = %s
                        where si.id = %s
                        '''
                    )    
                    cursor.execute(query, (rank, user_name, hashpw.hash_password(user_password), result[0]))
        
                except psycopg2.errors.StringDataRightTruncation:
                    print("입력한 값이 너무 깁니다.")
                    
                except psycopg2.errors.InvalidTextRepresentation:
                    print("잘못된 계급을 입력하였습니다.")
                             
            else:
                print("입력한 ID를 사용하는 병사가 데이터베이스에 존재하지 않습니다.")  
        
        elif action == '3':
            return
        
        else:
            print("다시 입력해주세요") 

def delete_soldier(cursor):
    while True:
        action = input("원하는 검색 방식의 숫자를 입력해주세요\n(1) 이름으로 검색\n(2) 병사가 사용하는 id로 검색\n(3) 검색 종료\n")
        
        if action == '1':
            name = input("병사의 이름을 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                delete from soldier_information si
                where si.name = %s;
                '''
            )
            
            cursor.execute(query, (name, ))
            
            if cursor.rowcount > 0:
                print(f"{name} 병사가 데이터베이스에서 삭제되었습니다.")            
            else:
                print("입력한 이름을 가진 병사가 데이터베이스에 존재하지 않습니다.") 
        
        elif action == '2':
            user_name = input("병사가 사용하는 id를 입력해주세요 : ")
            query = psycopg2.sql.SQL(
                '''
                delete from soldier_information si
                where si.user_name = %s;
                '''
            )
            
            cursor.execute(query, (user_name, ))
            if cursor.rowcount > 0:
                print(f"{user_name} 병사가 데이터베이스에서 삭제되었습니다.")            
            else:
                print("입력한 ID를 가진 병사가 데이터베이스에 존재하지 않습니다.") 
        
        elif action == '3':
            return
        
        else:
            print("다시 입력해주세요") 

def main():
    while True:
        action = input("원하는 기능의 숫자를 선택해주세요\n(1) 병사 추가\n(2) 병사 확인\n(3) 병사 정보 수정\n(4) 병사 정보 삭제\n(5) 종료\n")
        
        if action == '1':
            crud_operation('c')        
        elif action == '2':
            crud_operation('r')
        elif action == '3':
            crud_operation('u')
        elif action == '4':
            crud_operation('d')
        elif action == '5':
            return
        else: 
            print("잘못된 입력입니다.\n")

if __name__ == "__main__":
    main()