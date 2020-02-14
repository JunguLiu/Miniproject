# importing module
import sqlite3
import datetime
import getpass

def searchReq(): #search by email
    global c, conn, current_email
    c.execute("SELECT * FROM requests WHERE requests.email = '%s';"%current_email)
    all_requests = c.fetchall()
    
    for i in all_requests:
        print(i)
    ask = input("Would you like to select a request or delete? press s to select, d for delete: ")
    if (ask == 'd'):
        deleteReq()
    elif (ask == 's'):
        searchReqcode()

    
def searchReqcode(): #search by location code
    global c, conn, current_email
    askCode = input("Would you like to search by location code [l] or city [c]? ")
    if askCode == 'l':
        locCode = input("Please enter the location code: ")
        c.execute("SELECT * FROM requests WHERE pickup = '%s' limit 5;" %locCode)
        result = c.fetchall()
        if result == None:
            print("No requests for that location, try again.")
            searchReqcode()
        else:
            for x in result:
                print(x)
    if askCode == 'c':
        locCode = input("Please enter the city: ")
        city = locCode.lower()
        city = city.capitalize()   
        c.execute("SELECT * FROM locations l, requests r WHERE r.pickup = l.lcode and  l.city = '%s' limit 5;"%city)
        result = c.fetchall()
        if result == []:
            print("No requests for that location, try again.")
            searchReqcode()
        else:
            for x in result:
                print(x[4:])
    selectReq()
    

def selectReq(): #select a request and send message  
    global c, conn, current_email
    now = datetime.datetime.now()
    ask = input("Do you want to send message? (y/n)")
    if ask.lower() == 'y':
        email = input("Please enter the eamil you want to send the message: ")
        if check_email(email):
            msg = input("Please enter the message: ")
            properMessage = (email, now, current_email, msg, "null", "n")
            c.execute("INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) values (?, ?, ?, ?, ?, ?);", properMessage)
            print("Message sent")
        else:
            print("Please enter the right email")
            selectReq()
    elif ask.lower() == 'n':
        return
    else:
        print("Please enter y / n")
        selectReq()
    
        
def deleteReq(): #retrieve all the requests by matching request emails with the users email
    global c, conn, current_email
    c.execute("SELECT * FROM requests WHERE requests.email = '%s';"%current_email)
    all_requests = c.fetchall()
    for i in all_requests:
        print(i)
    rid = input("select a request by rid: ")
    delete(rid)

            

def delete(rid):
    global c, conn, current_email
    c.execute("Select * from requests where rid = ? and email = ?;",(rid,current_email))
    result = c.fetchone()
    if result == None:
        print("Please enter the right rid.")
        deleteReq()
    else:
        c.execute("DELETE FROM requests WHERE rid = '%s';"%rid)
        conn.commit()
        print("The request has been deleted.")

def check_loc_ride(loc):
    c.execute('select*from rides;')
    rides = c.fetchall()
    for ride in rides:
        if loc == ride[5] or loc == ride[6]:
            print(ride)
    c.execute('select * from enroute e,rides r where e.rno = r.rno')
    enroutes = c.fetchall()
    for enroute in enroutes:
        if loc == enroute[1]:
            print(enroute[2:])
    
    
    
    
def search_loc_1 (loc):
    c.execute('select*from locations')
    locations = c.fetchall()
    for l in locations:
        if loc in l[3]:
            check_loc_ride(l[0])
            return True
    for l in locations:
        if loc.upper() == l[1].upper():
            check_loc_ride(l[0])
            return True
    for l in locations:
        if loc.upper() == l[2].upper():
            check_loc_ride(l[0])
            return True
        
            
def check_locde(code):
    global c, conn, current_email
    c.execute('''select* from locations''')
    locs = c.fetchall()
    for loc in locs:
        if loc[0]== code:
            return True
    else:
        return False

def searchLoc():
    global c, conn, current_email
    #ask user for location
    c.execute('''select* from rides, enroute''')
    rides = c.fetchall()
    
    numberKey = input("How many keywords are you inputting to search for rides? 1, 2 or 3? ")
    if numberKey == '1':
        src1 = input("Please input first keyword: ")
        if search_loc_1(src1) or check_locde(src1):
            data = [src1.lower(),src1.lower(),src1.lower()]
            c.execute("select * from rides r, enroute e WHERE src = ? or dst = ? or lcode = ?", data)
            place = c.fetchall()
            if len(place) > 5:
                for i in range(5):
                    print(place[i])
                    carInfo(place[i])
            
                more = input("More rides available. Would you like to see more? y/n : ")
                if more == 'y':
                    data = [src1.lower(),src1.lower(),src1.lower()]
                    c.execute("select * from rides r, enroute e WHERE src = ? or dst = ? or lcode = ?", data)
                    place = c.fetchall()                   
                    for i in range(len(place)):
                        print(place[i]) 
                        carInfo(place[i])
                    selectRno()                    
                else:
                    selectRno()
            else:
                for i in range(len(place)):
                    print(place[i]) 
                    carInfo(place[i])
                selectRno()                
        else:
            searchLoc()
             
        
    elif numberKey == '2':
        src1 = input("Please input first keyword: ")
       
        data = [src1,src1,src1]
        c.execute("select * from rides r, enroute e WHERE src = ? or dst = ? or lcode = ? ", data)
        place1 = c.fetchall()       
        src2 = input("please input second keyword: ")
        if check_location(src1) and check_location(src2):     
            data = [src2,src2,src2]
            c.execute("select * from rides r, enroute e WHERE src = ? or dst = ? or lcode = ? ", data)
            place2 = c.fetchall()
            key2 = []
            for i in place1:
                for j in place2:
                    if i == j:
                        key2.append(i)
                        
            if len(key2) > 5:
                for i in range(0, 5):
                    print(key2[i])
                    carInfo(key2[i])
                    more = input("More rides available. Would you like to see more? y/n : ")
                    if more == 'y':
                        for i in range(len(key2)):
                            print(key2[i]) 
                            carInfo(key2[i])
                    elif more == 'n':
                        pass
                    else: 
                        print("wrong input")
                        searchLoc()
            else:
                for i in range(len(key2)):
                    print(key2[i])
                    carInfo(key2[i])
                    selectRno()
        else:
            print("Please enter location code.")
            searchLoc()
        
    elif numberKey == '3':
        src1 = input("Please input first keyword: ")
        data = [src1,src1,src1]
        c.execute("select * from rides r, enroute e WHERE src = ? or dst = ? or lcode = ?", data)
        place1 = c.fetchall()        
        src2 = input("please input second keyword: ")
        data = [src2,src2,src2]
        c.execute("select * from rides r, enroute e WHERE src = ? or dst = ? or lcode = ?", data)
        place2 = c.fetchall() 
        src3 = input("please input third keyword: ")
        data = [src3,src3,src3]
        c.execute("select * from rides r, enroute e WHERE src = ? or dst = ? or lcode = ?", data)
        place3 = c.fetchall()
        key3=[]
        if check_location(src1) and check_location(src2) and check_location(src3):
            for i in place1:
                for j in place2:
                    for k in place3:
                        if i == j == k:
                            key3.append(i)
            
            c.execute("select * from cars")
            car = c.fetchall()
    
            if len(key3) > 5:
                for i in range(0, 5):
                    print(key3[i])
                    carInfo(key3[i])
                    more = input("More rides available. Would you like to see more? y/n : ")
                    if more == 'y':
                        for i in range(len(key3)):
                            print(key3[i])
                            carInfo(key3[i])
                    elif more == 'n':
                        pass
                    else: 
                        print("wrong input")
                        searchLoc()
            else:
                for i in range(len(key3)):
                    print(key3[i])
                    carInfo(key3[i])
                    selectRno()
        else:
            print('Please enter the location code.')
            searchLoc()
    else:
        print("Invalid input. Please try again")
        searchLoc()
    
        
def carInfo(key): #retrieve car information for the rides that match
    global c, conn, current_email
    c.execute("select * from cars")
    car = c.fetchall()
    if key[8] == ("%s"):
        return
    for i in car:
        if (key[8] == i[0]):
            print(i)
        
                
def selectRno(): #select a ride that you wish to email
    global c, conn, current_email
    c.execute("SELECT * FROM rides")
    chooseR = input("Type the RNO of the ride you wish to access ")
    rides = c.fetchall()
    for ride in rides:
        if chooseR == str(ride[0]):
            msg = input("would you like to email the member to book for a ride? press y to confirm: ")
            if msg.lower() == 'y':
                select_book()
            elif msg.lower() == 'n':
                print("Exiting from rides")
                read_instructions()
            else: 
                print("Invalid input, try again")
                selectRno()


def check_my_profile(user_email):
    #let the indob massage be seenale 
    global c, conn, current_email
    check_file = input('which information would you like to check:\n*Booking[B]\n*Request[RE]\n*Inbox[I]\n*Rides[RI]\n*Private Info[PI]\n*Cars[C]\n Your instruction: ')
    
    if check_file.upper() == 'B':
        c.execute('select*from bookings;')
        all_booking_info = c.fetchall()
        for i in all_booking_info:
            if user_email == i[1]:
                print(i)
    if check_file.upper() == 'RE':
        c.execute('select*from requests;')
        all_requests_info = c.fetchall()
        for i in all_requests_info:
            if user_email == i[1]:
                print(i)    
    if check_file.upper() == 'I':
        check = input("check massage you sent[S] / check inbox[I]")
        if check.upper() == 'S':
            c.execute('select*from inbox;')
            all_inbox_info = c.fetchall()
            for i in all_inbox_info:
                if user_email == i[2]:
                    print(i)   
        if check.upper() == 'I':
            c.execute('select*from inbox;')
            all_inbox_info = c.fetchall()
            for i in all_inbox_info:
                if user_email == i[0]:
                    print(i)   
    if check_file.upper() == 'RI':
        c.execute('select*from rides;')
        all_rides_info = c.fetchall()
        for i in all_rides_info:
            if user_email == i[7]:
                print(i)   
    if check_file.upper() == 'PI':
        c.execute('select*from members;')
        all_members_info = c.fetchall()
        for i in all_members_info:
            if user_email == i[0]:
                print(i)  
    if check_file.upper() == 'C':
        c.execute('select*from cars;')
        all_cars_info = c.fetchall()
        for i in all_cars_info:
            if user_email == i[5]:
                print(i)  
    
    



def how_much_loc_code(locations,loc_code):
    global c, conn, current_email
    count_loc = 0
    for loc in locations:
        if loc_code.upper() == loc[1].upper():
            count_loc += 1
        elif loc_code.upper() in loc[3].upper():
            count_loc += 1
        elif loc_code.upper() == loc[2].upper():
            count_loc += 1
    
            
            
    if count_loc < 5:
        for loc in locations:
            if loc_code.upper() == loc[1].upper():
                print(loc)
            elif loc_code.upper() == loc[2].upper():
                print(loc)
            elif loc_code.upper() in loc[3].upper():
                print(loc)
    elif count_loc >=5:
        count =0
    
        for loc in locations:
            if loc_code.upper() == loc[1].upper() and count<5:
                print(loc)  
                count+=1
            elif loc_code.upper() == loc[2].upper() and count <5:
                print(loc)
                count +=1
            elif loc_code.upper() in loc[3].upper() and count<5:
                print(loc)
                count += 1
                
                
        see_more = input("See more option? (Y/N) ")
        if see_more.upper() == 'Y':
            for loc in locations:
                if loc_code.upper() == loc[1].upper():
                    print(loc)   
                if loc_code.upper() == loc[2].upper():
                    print(loc)
                if loc_code.upper() in loc[3].upper():
                    print(loc)
                else:
                    print(loc)
        elif see_more.upper()=='N':
            pass
        else:
            print('Please enter y/n')
            Ins_offer(current_email)
        
    
    

def check_location(loc_code):
    global c, conn, current_email
    c.execute('''select*from locations''')
    locations = c.fetchall()    
    word = []
    for i in locations:
        if loc_code.upper() == i[0].upper():
            return True
        
    for i in locations:
        if loc_code.upper() == i[1].upper():
            how_much_loc_code(locations, loc_code)
            return False 
    for i in locations:      
        if loc_code.upper() == i[2].upper():
            how_much_loc_code(locations, loc_code)
            return False
            
    for i in locations:       
        if loc_code.upper() in i[3].upper():
            how_much_loc_code(locations, loc_code)
            return False 
   
   
           
        
   
def generate_rno(table):
    global c, conn, current_email
    c.execute("select*from '%s';"%table)
    rides = c.fetchall()
    largest = 0
    for i in rides:
        if i[0]>largest:
            largest = i[0]
    return (largest+1)

def check_cno(offer_cno):
    global c, conn, current_email
    
    c.execute("select*from cars where cno = '%s';"%offer_cno)
    rides = c.fetchone()
    if rides == None:
        return False
    elif rides[5] == str(current_email):
        return True
    else:
        return False
                

def location_check(loc_code):
    global c, conn, current_email,loc_code_c
    if check_location(loc_code):
        loc_code_c = loc_code
        return True  
    loc_code_c = input('enter location code: ')
    if location_check(loc_code_c):
        return True
    
def add_car(user_email):
    global c, conn, current_email
    car_make = input("What's the brand name of the car: ")
    car_model = input("What car model of yourcar: ")
    car_year = input("Which year was it produced: ")
    car_seats = input('How many seats does the car have: ')
    car_num = generate_rno('cars')
    c.execute("insert into cars values(?,?,?,?,?,?)",(car_num,car_make,car_model,car_year,car_seats,user_email))
    conn.commit()
    print("successfully recorded car information and your car number is "+ str(car_num))
    
    
    

def Ins_offer(user_email):
    global c, conn, current_email,loc_code_c
    offer_rno = generate_rno('rides') 
    offer_date = input("What date would you like to offer a ride: ")
    offer_seat = input("How many seats would you like you offer: ")
    offer_price = input("How much for each seat you provide: ")
    offer_lugdes = input ("What is the luggage description: ")
    want_add_car = input("Do you want to add a car number?(Y/N) ")
    if want_add_car.upper() == 'Y':
        add_car(user_email)
    elif want_add_car.upper() == 'N':
        pass
    else:
        print("Please enter y/n.")
        Ins_offer(user_email)
    offer_src = input("What is the source location code: ") 
    if location_check(offer_src):
        offer_src = loc_code_c 
        offer_src_code = offer_src
        offer_dst = input("What is the destination location code: ")
        if location_check(offer_dst):
            offer_dest = loc_code_c
            offer_dest_code = offer_dest
            offer_cno = input("What is your car number: ")
            if check_cno(offer_cno):
                optional_en_loc = input("Would you like to give us your enroute location ?(Y/N)")
                if optional_en_loc.upper() == 'Y':
                    offer_en_loc = input('What is your enroute location code: ')
                    if location_check(offer_en_loc):
                        offer_en_loc = loc_code_c
                        c.execute('insert into enroute values(?,?)',(offer_rno,offer_en_loc))
                        conn.commit()
                        
                else:
                    offer_en_loc = 'null'
                
                c.execute('insert into rides values(?,?,?,?,?,?,?,?,?)',(offer_rno,offer_price,offer_date,offer_seat,offer_lugdes,offer_src_code,offer_dest_code,user_email,offer_cno))
                conn.commit()   
                print("Your offer is posted successfully")
            else:
                print("wrong car number")
                Ins_offer(user_email)
        else:
            print("Wrong location code")
            
    else: 
        print("Wrong Location code!")
        
        
        
def read_instruction(user_name):
    global c, conn, current_email
    user_instruction = input("Log in, what do you want to do next? \n*offer[O]\n*post[P]\n*book[B]\n*quit[Q]\n*search ride[SR]\n*search and delete ride request[SDR]\n*check my profile[CMP]\ninstruction: ")
    if user_instruction.upper() == "O":
        Ins_offer(user_name)
        read_instruction(user_name)
    elif user_instruction.upper() == "P":
        ride()
        read_instruction(user_name)
    elif user_instruction.upper() == "B":
        book()
        read_instruction(user_name)    
    elif user_instruction.upper() == "Q":
        How_login()
        read_instruction(user_name) 
    elif user_instruction.upper() == "SR":
        searchLoc()
        read_instruction(user_name) 
    elif user_instruction.upper() == 'SDR':
        searchReq()
        read_instruction(user_name) 
    elif user_instruction.upper() == 'CMP':
        check_my_profile(user_name)
        read_instruction(user_name) 
        
    else:
        print("Wrong instruction do it again!")
        read_instruction(user_name)
        
        

def regist(users):
    global c, conn, current_email
    new_user_email = input('For registering a new account, please enter your email: ')
    for user_infor in users:
        if new_user_email == user_infor[0]:
            print("Sorry the email already exists, please enter a new one or log in XD")
            return 
        elif new_user_email == ' ':
            print("The email can not be empty")
            return 
        else:
            new_user_name = input("Please enter the user name: ")
            new_user_phone = input("Please enter your phone number: ")
            new_user_password = input("Please enter your password:")
            c.execute('insert into members values(?,?,?,?)',(new_user_email, new_user_name, new_user_phone, new_user_password))
            conn.commit()  
            print("Finshed creating account")
            print("Loading ...")
            read_instruction(new_user_email)
            
            return
        
def email_exit(users,user_email):
    for user_infor in users:
        if user_email == user_infor[0]:   
            return True
    return False
    
def check_pwd(users,pwd,user_email):
    for user in users:
        if user_email == user[0] and str(pwd) == user[3]:
            return True
        
def get_user_name(users,user_email):
    for user in users:
        if user_email == user[0]:
            return user[1]
        
def print_unseen_massage(user_email):
    global c, conn, current_email
    c.execute("select*from inbox;")
    inbox = c.fetchall()
    for i in inbox:
        if user_email == i[0] and i[5] == 'n':
            print(i[3])
    c.execute("update inbox set seen = 'y' where seen ='n' and email = '%s' "%user_email)
    conn.commit()
        

def log_in(users):
    global c, conn, current_email

    user_email = input('For logging in please enter your email: ')
    if email_exit(users, user_email):
        pwd = getpass.getpass("Password: ")
        if check_pwd(users, pwd, user_email):
            user_name = get_user_name(users, user_email)
            current_email = user_email
            print('Sucessfully logged in :)') 
            print_unseen_massage(user_email)
            read_instruction(user_email)
            return
        else:
            print('Sorry Wrong password :(')
            return 
    else:
        print("Your email does not exist, please check again or create an account :D")
        return
            
    

    


def How_login():
    global c, conn, current_email
    # select user infor (email and pwd ) from table members
    c.execute('''select*from members ''')
    
    users = c.fetchall()
    
    #ask user to login 
    logIn_way = input("Want to join us? or already have an account?(register/r)(log_in/l): ")
    # to see wether the user log in successfully 
    log_in_app = False
    
    #if the user already has an account 
    if logIn_way == 'l':
        log_in(users)
       
    #if the user want to create a new account 
    if logIn_way == 'r':
        regist(users)

def check_email(email):
    global c, conn, current_email
    c.execute("select*from requests where '%s'"%current_email)
    tables = c.fetchall()     
    for i in tables:
        if email.lower() == str(i[1]):
            return True
    return False


       
def ride():
    global c, conn, current_email
    rdate = input("date(YYYY-MM-DD)?" )
    pickup = input("Pickup location?" )
    if check_location(pickup):
        dropoff = input("Dropoff location?")
        if check_location(dropoff):
            amount = input("The amount willing to pay per seat?" )
            c.execute("select * from requests")
            rows = c.fetchall()
            new_rid = generate_rno("requests")
            data = ( new_rid,str(current_email) ,rdate ,pickup,dropoff,amount )
            c.execute(" INSERT INTO requests (rid,email,rdate,pickup,dropoff,amount) VALUES (?, ?, ?, ?,?,? ) ", data)
            conn.commit()
            print("Request successful")
        else:
            print("Please enter the right location code\n")
            ride()         
    else:
        print("Please enter the right location code\n")
        ride()
           
            
    
def book():
    global c, conn, current_email
    c.execute("select bno, email, bookings.rno, cost, bookings.seats, pickup, dropoff from bookings, rides  where bookings.rno = rides.rno and driver = '%s';"%current_email)
    result = c.fetchall()
    for x in range(len(result)):
        print (result[x])
    booking_instruction = input("What do you want to do next? (book/cancel/quit)")
    if booking_instruction.lower() == "book":
        booking()
        book()
    elif booking_instruction.lower() == "cancel":
        cancel_booking()
        book()
    elif booking_instruction.lower() == "quit":
        read_instruction(current_email)

def check_bno(cancel_bno):
    global c, conn, current_email
    c.execute("select bno from bookings, rides  where bookings.rno = rides.rno and driver = '%s';"%current_email)
    bnos = c.fetchall()
    for bno in bnos:
        if int(cancel_bno) == bno[0]:
            return True
    return False
        
 
def cancel_booking():
    global c, conn, current_email
    now = datetime.datetime.now()
    cancel_bno = input("Please enter the bno of the booking that you want to cancel:")
    if check_bno(cancel_bno):
        c.execute("select email,rno from bookings where bno = '%s';"%cancel_bno)
        email_rno = c.fetchone()
        data = (str(email_rno[0]),now,str(current_email),"Your booking has been refused",int(email_rno[1]),"n")
        c.execute("INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) values (?,?,?,?,?,?);",data)
        c.execute("delete from bookings where bno = '%s';"%cancel_bno)
        conn.commit()
    else:
        print("Please enter the right rno.\n")
        book()
   
   
def booking():
    global c, conn, current_email
    c.execute("select r.rno, price, rdate, r.seats-b.seats, lugDesc, src, dst, driver from rides r,bookings b where r.rno = b.rno and b.seats < r.seats and r.driver !='%s' limit 5;"%current_email)
    result = c.fetchall()
    for x in range(len(result)):
        print (result[x]) 
    c.execute("select r.rno, price, rdate, r.seats-b.seats, lugDesc, src, dst, driver from rides r,bookings b where r.rno = b.rno and b.seats < r.rno and r.driver != '%s';"%current_email)
    result = c.fetchall()
    if len(result) > 5:
        more_information = input("Do you want more information? (y/n)")
        if more_information.lower() == "y":
            for x in range(len(result)):
                print (result[x])   
        elif  more_information.lower() == "n":
            pass
        else:
            booking()
    else:
        pass
    select_book()

def select_book():
    global c, conn, current_email   
    now = datetime.datetime.now()
    email = input("Please enter the member email that you want to book:")
    seats = input("Please enter the number of seats booked:")
    cost = input("Please enter the cost per seat you are willing to pay:")
    pickup = input("Please enter the pickup location code:")
    dropoff = input("Please enter the drop off location code:")
    bno = generate_rno("bookings")
    data = (email,pickup,dropoff)
    c.execute("select rno, seats from rides where driver =? and src = ? and dst=?;",data)
    result = c.fetchone()
    if result == None:
        print("Please check your informaton")
        booking()
    elif int(result[1]) < int(seats):
        print("Warning: the number of seats booked exceeds the number of seats offered")
        confirm = input("Do you want to continue ?(y/n)")
        if confirm.lower() == "y":
            data = (bno,str(current_email),int(result[0]),int(cost),int(seats),pickup,dropoff)
            c.execute("insert into bookings(bno, email, rno, cost, seats, pickup, dropoff) values (?,?,?,?,?,?,?);",data)
            print("Booking succeed.")
            msg = (email,now,str(current_email),"Your ride has been booked.",int(result[0]),"n")
            c.execute("INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) values (?,?,?,?,?,?);",msg)
            conn.commit()
        elif confirm.lower() == "n":
            booking()
        else:
            print("Please eneter y/n.")
            booking()
    else:   
        data = (bno,str(current_email),result[0],int(cost),int(seats),pickup,dropoff)
        c.execute("insert into bookings(bno, email, rno, cost, seats, pickup, dropoff) values (?,?,?,?,?,?,?);",data)
        print("Booking succeed.")
        msg = (email,now,str(current_email),"Your ride has been booked.",int(result[0]),"n")
        c.execute("INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) values (?,?,?,?,?,?);",msg)
        conn.commit()
    
    
    
def main():
    global c, conn, current_email
    # connecting to the database
    conn = sqlite3.connect("Miniproject.db")
    #c
    c = conn.cursor()     
    How_login()
main()