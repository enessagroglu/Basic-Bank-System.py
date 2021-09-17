#Enes Sagiroglu

import random
import time
from datetime import datetime

usersDict = {'admin':'123'}
newUser = {}
customer_nums = []

def create_customer_num():
    customer_num = str(random.randrange(1000,9999))
    if customer_num in customer_nums:
        create_customer_num()
    else:
        customer_nums.append(customer_num)
    return customer_num

def customer_registration():
    print("*** Registration ***")
    #Taking info from user
    customer_num = create_customer_num()
    name = input("Name:")
    surname = input("Surname:")
    birth_date = input("Birth date:")
    phone_number = input("Phone number:")
    mail = input("Your active e-mail account:")
    customer_password = input("Create a password to login:")
    wealth = float(0)
    debt = [float(0),float(0)] # [total debt, monthly payment]
    register_time = datetime.now()
    #Keeping all values in info as a list
    info = [customer_num,name,surname,birth_date,phone_number,mail,customer_password,wealth,register_time,debt]
    newUser[customer_num] = info #customer num = key, info = value
    usersDict.update(newUser)
    print(
        f'''
        
        Your account has been created succesfully. Your customer number is {customer_num},
        You will use this number and password to access your bank account...

        '''
    )
    time.sleep(1)
    print(
        f'''
        ----------------------------------
                **WARNING**              
         Customer number: {customer_num} 
         Password: {customer_password}   
        ----------------------------------

        '''
    )
    time.sleep(1)

def login(id, password):
    if id == 'admin' and password == '123':
        print("--- Welcome Admin ---")
        admin_menu()
    else:
        #checking the customer number is it exist in the system or not
        if id in usersDict and usersDict[id][6] == password :
            print(f"--- Welcome {usersDict[id][1].upper()} {usersDict[id][2].upper()} ---")
            global current_id #current id keeps the customer number of current user
            current_id = id
            user_menu()
        else:
            print("User not found...")
            main_menu()
 
def main_menu():
    print(
        '''
        $  WELCOME TO THE BANK  $
        [1] Login
        [2] Register
        [3] Quit
        '''
        )
    choice = int(input('Choice:'))
    if choice == 1:
        id = input('Customer number:')
        password = input('Password:')
        login(id,password)
    elif choice == 2:
        customer_registration()
        main_menu()
    elif choice == 3:
        print('Have a nice day...')
        quit()
    else:
        print('Invalid choice...')
        main_menu()

def user_menu():
    print(
        '''
                USER MENU

        [1] Show account information
        [2] Withdraw money from account
        [3] Deposit money into account
        [4] Money transfer
        [5] Loan transactions
        [6] Debt payment
        [7] Quit
        '''
    )
    choice = int(input('Choice:'))
    if choice == 1:
        print(#printing customer info from users dict usersDict[key][index number for info list]
        f'''
        Customer number : {usersDict[current_id][0]}
        Account opening date : {usersDict[current_id][8]}

        Name : {usersDict[current_id][1].upper()}
        Surname : {usersDict[current_id][2].upper()}
        Birth date : {usersDict[current_id][3]}

        Phone number : {usersDict[current_id][4]}
        E-mail : {usersDict[current_id][5]}

        Money in account : {usersDict[current_id][7]} $
        Debt : 
            Total payment : {usersDict[current_id][9][0]} $
            Monthly payment : {usersDict[current_id][9][1]} $
        
        Total Money : {usersDict[current_id][7] - usersDict[current_id][9][0]} $

        '''
        )
        user_menu()

    elif choice == 2:
        value = float(input('\nAmount of money you want to withdraw:'))
        if value > usersDict[current_id][7]:
            print(f'Insufficient funds...\nMoney in account: {usersDict[current_id][7]} $')
            user_menu()
        else:
            usersDict[current_id][7] -= value
            print(f'\nCurrent money: {usersDict[current_id][7]} $')
            user_menu()
    elif choice == 3:
        value = float(input('\nAmount of money you want to deposit:'))
        usersDict[current_id][7] += value
        print(f'Current money: {usersDict[current_id][7]} $')
        user_menu()
    elif choice == 4:
        target_acc = input('\nThe customer number of the person you want to send the money to:')
        if target_acc not in usersDict:
            print('Invalid customer number.')
            user_menu()
        else:
            value = float(input('Amount:'))
            if value > usersDict[current_id][7]:
                print(f'Insufficient funds...\nMoney in account: {usersDict[current_id][7]} $')
                user_menu()
            else:
                #updating the money in current and target account
                usersDict[current_id][7] = usersDict[current_id][7] - value
                usersDict[target_acc][7] = usersDict[target_acc][7] + value
                print(f'\nCurrent money: {usersDict[current_id][7]} $')
                user_menu()
            
    elif choice == 5:
        loan = int(input('Loan amount:'))
        lterm_m = int(input('Loan term in months:'))
        interest_rates = [1.90 , 1.35 , 1.45 ]
        #interest rate is randomly selected from this list

        interest_rate = interest_rates[random.randrange(0,3)]
        monthly_payment = float("{:.2f}".format((loan*interest_rate)/lterm_m))
        total_payment = float("{:.2f}".format(loan*interest_rate))

        usersDict[current_id][9][0] += total_payment
        usersDict[current_id][9][1] += monthly_payment
        usersDict[current_id][7] += loan
        time.sleep(2)

        print(
            f'''
            \nLoan operation completed.
            Interest rate : {interest_rate}%
            Loan amount : {loan} $

            Monthly payment : {monthly_payment} $
            Loan term in months : {lterm_m}

            Total payment : {total_payment} $ 

            '''
        )
        user_menu()
    elif choice == 6:
        print(
            f'''
            [1] Total payment ({usersDict[current_id][9][0]} $)
            [2] Monthly payment ({usersDict[current_id][9][1]} $)
            
            '''
        )
        pay = int(input('Select a payment type: '))

        if pay == 1:     #current money  <  total debt
            if usersDict[current_id][7] < usersDict[current_id][9][0]:
                print('Insufficient funds...')
                user_menu()
            else:
                usersDict[current_id][7] -= usersDict[current_id][9][0]
                usersDict[current_id][9][0] = 0
                usersDict[current_id][9][1] = 0
                print(
                   f'''
                    $ Payment process completed $
                    
                    Money in account : {usersDict[current_id][7]} $
                    Debt : 
                        Total payment : {usersDict[current_id][9][0]} $
                        Monthly payment : {usersDict[current_id][9][1]} $
        
                        Total Money : {usersDict[current_id][7] - usersDict[current_id][9][0]} $

                    '''
                )
                user_menu()
        elif pay == 2:
            if usersDict[current_id][7] < usersDict[current_id][9][1]:
                print('Insufficient funds...')
                user_menu()
            else:
                usersDict[current_id][7] -= usersDict[current_id][9][1]
                usersDict[current_id][9][0] -= usersDict[current_id][9][1]

                if usersDict[current_id][9][0] < usersDict[current_id][9][1]:
                    usersDict[current_id][9][0] = usersDict[current_id][9][1]
                print(
                   f'''
                    $ Payment process completed $
                    
                    Money in account : {usersDict[current_id][7]} $
                    Debt : 
                        Total payment : {usersDict[current_id][9][0]} $
                        Monthly payment : {usersDict[current_id][9][1]} $
        
                        Total Money : {usersDict[current_id][7] - usersDict[current_id][9][0]} $

                    '''
                )
                user_menu()
        else:
            print('Invalid choice...')
            user_menu()

    elif choice == 7:
        print('Have a nice day...')
        main_menu()
    else:
        print('Invalid choice...')
        user_menu()

def print_customers():
    i = 1
    print('             --------------- CUSTOMERS -----------------')
    for key in usersDict:
        if key == 'admin': # do not show the admin info in customers list
            continue
        print(
            f'''
            [{i}] Customer number : {key} 
            Full name : {usersDict[key][1].upper()} {usersDict[key][2].upper()}
            -------------------------------------------
            '''
        )
        i +=1


def admin_menu():
    print(
        '''
            * ADMIN MENU *

        [1] Show customers as a list
        [2] Delete customer
        [3] View a customer's account in detail
        [4] Quit
        '''
    )
    choice = int(input('Choice:'))

    if choice == 1:
        print_customers()
        admin_menu()

    elif choice == 2:
        print_customers()
        target = input("Customer number:")
        usersDict.pop(target)
        print('The customer has been deleted..')
        admin_menu()
    
    elif choice == 3:
        print_customers()
        customer = input('Customer number:')
        print(
        f'''
        Customer number : {usersDict[customer][0]}
        Account opening date : {usersDict[customer][8]}

        Name : {usersDict[customer][1].upper()}
        Surname : {usersDict[customer][2].upper()}
        Birth date : {usersDict[customer][3]}

        Phone number : {usersDict[customer][4]}
        E-mail : {usersDict[customer][5]}

        Money in account : {usersDict[customer][7]} $
        Debt : 
            Total payment : {usersDict[customer][9][0]} $
            Monthly payment : {usersDict[customer][9][1]} $
        
        Total Money : {usersDict[customer][7] - usersDict[customer][9][0]} $

        '''
        )
        admin_menu()

    elif choice == 4:
        print('Have a nice day...')
        main_menu()
    
    else:
        print('Invalid choice...')
        admin_menu()

main_menu()