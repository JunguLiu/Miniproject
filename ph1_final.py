from bsddb3 import db
import re
import os
def main():
    inputfile= input("Enter name of source file\n")
    fr = open(inputfile,'r')
    fterms = open('terms.txt','w')
    fpdates = open('pdates.txt','w')
    fprices = open('prices.txt','w')
    fads = open('ads.txt','w')
 
    for line in fr:
            newline1 = line.replace('&#039;',"")
            newline2 = newline1.replace('&#034;','')
            newline3 = newline2.replace('&amp;',"&")
            newline4 = newline3.replace('&#[0-9]+',"") 
            reline = re.findall("[0-9a-zA-Z_-]+", newline4)
            if  reline[0] == 'ad':
                ID =  reline[2]
                date = reline[5]+"/"+reline[6]+"/"+reline[7]
                location =""
                category = ""
                swich =0
                time = 0
                for i in range(len(reline)):   
                    if swich ==1 and reline[i]!="loc" and time ==0:
                        location += reline[i] 
                        time += 1 
                    
                    if swich ==1 and reline[i+1]!="loc" and reline[i+1] != "cat" and time > 0 and reline[i].endswith("-") and reline[i+1].startswith("-"):
                        location += "/"
                        location += reline[i+1]
                        time = 1
                        reline[i] = reline[i+1]
                        continue
                        
                    if swich ==1 and reline[i+1]!="loc" and reline[i+1] != "cat" and time > 0 :
                        location += "."
                        location += reline[i+1] 
                        time += 1 
                        
                    if (reline[i]=="loc"):
                        if swich ==1:
                            swich =0
                        else:
                            swich =1
                            
                   
                               
                for i in range(len(reline)):     
                    if swich ==1 and reline[i]!="cat":
                        category+=reline[i]    
                    if (reline[i]=="cat"):
                        if swich ==1:
                            swich =0
                        else:
                            swich =1
                            

                price = reline[-3]
                
                fpdates.write(date+":"+ID+","+ category+"," + location +"\n")
                fprices.write(price.rjust(12)+":"+ID+","+ category+"," + location +"\n")
                fads.write(ID+ ":"+line )
                switch =0
                for i in range(len(reline)):
                    if reline[i] == "ti" and reline[i-1] == "cat":
                        switch = 1
                    if reline[i] == "desc" and reline[i+1] == "price":
                        switch = 0   
                    if switch == 1:
                        if reline[i] != "desc" and len(reline[i]) >2  and reline[i]!= "cat" :
                            fterms.write(reline[i].lower()+":"+ ID + "\n")
                
                
            
main()

            