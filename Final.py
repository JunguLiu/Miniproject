from bsddb3 import db
import sqlite3
import time
import datetime 

        
    
def get_queries(old_query):
    queries_list =[]
    query = old_query.replace(" ","") 
    for i in range(len(query)):
        if query[i] == '%':
            f_part = query[0:i]
            operator = query[i]
            queries_list.append("term")
            queries_list.append (operator)
            queries_list.append(f_part)
            
        
        elif query[i] == '<':
            if query[i+1] == '=':
                f_part = query[0:i]
                operator = query[i:i+2]
                queries_list.append(f_part)
                queries_list.append (operator)
                queries_list.append(query[i+2:])
                break
                
            else:
                f_part = query[0:i]
                operator = query[i]
                queries_list.append(f_part)
                queries_list.append (operator)
                queries_list.append(query[i+1:])
                
        elif query[i] == '>':
            if query[i+1] == '=':
                f_part = query[0:i]
                operator = query[i:i+2]
                queries_list.append(f_part)
                queries_list.append (operator)
                queries_list.append(query[i+2:])
                break
                             
            else:
                f_part = query[0:i]
                operator = query[i]
                queries_list.append(f_part)
                queries_list.append (operator)
                queries_list.append(query[i+1:])                
                
        elif query[i] == '=':
            f_part = query[0:i]
            operator = query[i]
            queries_list.append(f_part)
            queries_list.append(operator)
            queries_list.append(query[i+1:])
            
    if not queries_list:
        queries_list.append("term")
        queries_list.append("")
        queries_list.append(query)
    
        
    return queries_list
    

def find_loc(db_f,queries_lis):
    #do stuff
    cur = db_f.cursor()
    data = cur.first()
    result_list = []
    loc_info = queries_lis[2].lower()
    loc_info = loc_info.capitalize()
    while data: # aid, cat, loc
        a, b, c = data[1].split(",")
        c = c.lower()
        c = c.capitalize()
        file_loc = c.decode("utf-8")
        if loc_info == file_loc:
            result_list.append(a)
            data = cur.next()
        else:
            data = cur.next()
            
    cur.close()
    return result_list

def find_term(db_f, queries_lis):
    cur = db_f.cursor()
    data = cur.first()
    result_lis = []
    
    if queries_lis[1]=="%":
        term_info = queries_lis[2].lower()
        while data:
            file_data = data[0]
            if file_data[0:len(term_info)]==term_info:
                result_lis.append(data[1])
                data = cur.next()
            else:
                data = cur.next()
            
    else:
        term_info = queries_lis[2].lower()
        while data: 
            file_term = data[0]
            if term_info == file_term:
                result_lis.append(data[1])
                data = cur.next()
            else:
                data = cur.next()
    cur.close()
    return result_lis



def find_date(db_f,queries_lis):
    cur = db_f.cursor()
    data= cur.first()
    result_lis =[]
    date_info = queries_lis[2]
    date_info = time.strptime(date_info,"%Y/%m/%d")
    if queries_lis[1]=='=':
        while data:
            file_date = time.strptime(data[0].decode("utf-8"),"%Y/%m/%d")
            if date_info == file_date:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()
                
    elif queries_lis[1] == '>':
        while data:
            file_date = time.strptime(data[0].decode("utf-8"),"%Y/%m/%d") 
            if file_date > date_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()
                
    elif queries_lis[1] == '<':
        while data:
            file_date = time.strptime(data[0].decode("utf-8"),"%Y/%m/%d") 
            if file_date < date_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next() 
                
    elif queries_lis[1] == '<=':
        while data:
            file_date = time.strptime(data[0].decode("utf-8"),"%Y/%m/%d") 
            if file_date < date_info or file_date == date_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()
                
    elif queries_lis[1] == '>=':
        while data:
            file_date = time.strptime(data[0].decode("utf-8"),"%Y/%m/%d") 
            if file_date > date_info or file_date == date_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()    
    cur.close()
    return result_lis
    

def find_price(db_f,queries_lis):
    cur = db_f.cursor()
    data= cur.first()
    result_lis =[]
    price_info = queries_lis[2].rjust(12)
    
    if queries_lis[1]=='=':
        while data:
            if str(data[0].decode("utf-8")[0:len(price_info)]) == price_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next() 
                
    elif queries_lis[1] == '>':
        while data: 
            if str(data[0].decode("utf-8"))>price_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()
                
    elif queries_lis[1] == '<':
        while data: 
            if str(data[0].decode("utf-8"))<price_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()    
                
    elif queries_lis[1] == '<=':
        while data:   
            if str(data[0].decode("utf-8")) < price_info or str(data[0].decode("utf-8")) == price_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()
                
    elif queries_lis[1] == '>=':
        while data: 
            if str(data[0].decode("utf-8")) > price_info or str(data[0].decode("utf-8")) == price_info:
                ID,cat,city = data[1].split(",")
                result_lis.append(ID)
                data = cur.next()
            else:
                data = cur.next()    
    cur.close()
    return result_lis


def find_cat(db_f,queries_lis):
    cur = db_f.cursor()
    data= cur.first()
    result_lis =[]
    cat_info = queries_lis[2]
    while data:
        file_date = data[0]
        ID,cat,city = data[1].split(",")
        if cat_info == cat:
            ID,cat,city = data[1].split(",")
            result_lis.append(ID)
            data = cur.next()
        else:
            data = cur.next()
                
    cur.close()
    return result_lis


def get_title (t_string):
    f,ti = t_string.split('<ti>') 
    title,b = ti.split('</ti>')
    return title


def delet_space(string):
    str_lis = []
    string1=""
    for i in string:
        str_lis.append(i)
    for i in range(len(str_lis)):
        if str_lis[i] == '>'or  str_lis[i] =='=' or  str_lis[i] =='<':
            for j in range(i+1,len(str_lis)):
                if str_lis[j] !=" ":
                    break
                if str_lis[j] == " ":
                    str_lis[j] = ""
                
            for k in reversed(range(0,i)):
                if str_lis[k] !=" ":
                    break
                if str_lis[k] == " ":
                    str_lis[k] = ""  
                
    for i in str_lis:
        string1 += i
    
    
    return string1
        
    
def main():
    query_input = raw_input("Enter the query: ");
    query_input = delet_space(query_input)
    
    old_queries = query_input.split(" ") 
    queries=[]
    
    for i in old_queries:
        if i != '':
            queries.append(i)
        
    
    final_result = []
    print_result = []
    delete_lis = []
    
    for j in range(len(queries)):
        queries_lis = get_queries(queries[j])            
        db_f = db.DB()
        if (queries_lis[0] == 'date'):
            db_f.open('da.idx')
            date_result = find_date(db_f,queries_lis)
            final_result.append(date_result)
           
                
        elif (queries_lis[0] == 'price'):
            db_f.open('pr.idx')
            price_result = find_price(db_f,queries_lis)
            final_result.append(price_result)
            
        
        elif(queries_lis[0] == 'location'):
            db_f.open('pr.idx')
            loc_result = find_loc(db_f,queries_lis)
            final_result.append(loc_result)
        
        elif(queries_lis[0] == 'cat'):
            db_f.open('pr.idx')
            cat_result = find_cat(db_f,queries_lis)
            final_result.append(cat_result) 
                
            
        elif(queries_lis[0] == 'term'):
            db_f.open('te.idx')
            term_result = find_term(db_f,queries_lis)
            final_result.append(term_result) 
                                 
        else:
            print("error")
            
    
            
    if len(final_result) ==0:
        print("sorry no vaild result :(")
        
    else:
        smallest = final_result[0]
        for result in final_result:
            if len(result) < len(smallest):
                smallest = result
        
        
        
        for p_result in smallest:
            for i in final_result:
                if p_result in i :
                    pass
                else:
                    delete_lis.append(p_result)
                    break
                    
        for i in delete_lis:
            smallest.remove(i)
   
        db_f = db.DB()
        db_f.open('ad.idx')        
        cur = db_f.cursor()
        for print_e in smallest:
            data= cur.first()
            while data:
                file_data = data[0].decode("utf-8")
                if file_data == print_e:
                    title = get_title(data[1])
                    print (data[0]+":"+title)
                    data = cur.next()
                else:
                    data = cur.next()
        cur.close()            
            
                    
                    
    
    while 1:
        inst = raw_input("\n1)Change format[output=full(of)/output=brief(ob)] \n2)Quit[Q] \nEnter instruction: ")
        
        if inst.lower() == 'of' or inst.lower()=='output=full':
            db_f = db.DB()
            db_f.open('ad.idx')        
            cur = db_f.cursor()
            for print_e in smallest:
                data= cur.first()
                while data:
                    file_data = data[0].decode("utf-8")
                    if file_data == print_e:
                        print(data[0]+':'+data[1])
                        data = cur.next()
                    else:
                        data = cur.next()
            cur.close()
            print('\n')
            
        elif inst.lower() == 'ob' or inst.lower()=='output=brief':
            db_f = db.DB()
            db_f.open('ad.idx')        
            cur = db_f.cursor()
            for print_e in smallest:
                data= cur.first()
                while data:
                    file_data = data[0].decode("utf-8")
                    if file_data == print_e:
                        title = get_title(data[1])
                        print (data[0]+":"+title)
                        data = cur.next()
                    else:
                        data = cur.next()
            cur.close() 
            print('\n')
            
        elif inst.lower() == 'q':
            return
            
        
main()