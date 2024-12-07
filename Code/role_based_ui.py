import soldier_information_table

import wired_equipment
import wireless_equipment
import computer_equipment

def login(ban):
    if ban == '무선반':
        print('무선반 접속')
        wireless_operator_ui()       
    
    elif ban == '유선반':
        print('유선반 접속')
        field_wireman_ui()
    
    elif ban == '전장반':
        print('전장반 접속')  
        computer_technician_ui()
    
    elif ban == '운통반':
        print('운통반 접속') 
        admin_ui()       
    
    elif ban == '기타':
        print('기타 접속')
 
def wireless_operator_ui():
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 무선 장비 관리\n(2) 종료\n')
        if action == "1":
            wireless_equipment.main()
        elif action == "2":
            print("종료합니다.")
            break
        
def field_wireman_ui():
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 유선 장비 관리\n(2) 종료\n')
        if action == "1":
            wired_equipment.main()
        elif action == "2":
            print("종료합니다.")
            break

def computer_technician_ui():
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 전자 장비 관리\n(2) 종료\n')
        if action == "1":
            computer_equipment.main()
        elif action == "2":
            print("종료합니다.")
            break


def admin_ui():
    while True:
        action = input('\n원하는 기능의 숫자를 입력해주세요 \n(1) 병사 관리\n(2) 무선 장비 관리\n(3) 유선 장비 관리\n(4) 전자 장비 관리\n(5) 종료\n')
        if action == "1":
            soldier_information_table.main()
        elif action == "2":
            wireless_equipment.main()
        elif action == "3":
            wired_equipment.main()
        elif action == "4":
            computer_equipment.main()
        elif action == "5":
            print("종료합니다.")
            break