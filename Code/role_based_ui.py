import soldier_information_table

def login(ban):
    if ban == '무선반':
        print('무선반 접속')        
    
    elif ban == '유선반':
        print('유선반 접속')        
    
    elif ban == '전장반':
        print('전장반 접속')        
    
    elif ban == '운통반':
        print('운통반 접속') 
        admin_ui()       
    
    elif ban == '기타':
        print('기타 접속')
        
    else:
        print(ban)
        

def admin_ui():
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 병사 관리\n(2) 종료\n')
        if action == "1":
            soldier_information_table.main()
        elif action == "2":
            print("종료합니다.")
            break