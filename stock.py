import os
import sys
import mysql.connector
from pathlib import Path

global database,username,password,hostname
database=username=password=hostname=""
global total
total=1

def conn(database, hostname, username, password):
    mydb = mysql.connector.connect(host=hostname,user=username,password=password,database=database)
    return mydb

def entry(x):
    try:
        #dbobj=conn(database,hostname,username,password)
        print("\n--Enter Details of Product--")
        if x==1:
            pcode=input("Product Code: ")
            pinfo=input("Product Information: ")
            pmrp=float(input("Product MRP: "))
            pcp=float(input("Product Cost Price: "))
            psp=float(input("Product Selling Price: "))
            gstc=input("GST HSN Code:")
            gst=int(input("GST in %: "))
            qt=int(input("Quantity in stock: "))
            cursor1=dbobj.cursor()
            cursor1.execute("INSERT INTO stock_inventory (product_code,product_info,product_mrp,product_cp,product_sp,gstcode,gst,quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(pcode,pinfo,pmrp,pcp,psp,gstc,gst,qt))
            dbobj.commit()
            cursor1.close()
            print("Inventory Added!\n")
        elif x==2:
            pcode=input("Product Code: ")
            qt=int(input("Quantity to increment: "))
            cursor1=dbobj.cursor()
            cursor1.execute("SELECT quantity FROM stock_inventory WHERE product_code='%s'"%(pcode))
            print(qt)
            result=cursor1.fetchone()
            quantity=result[0]
            quantity+=qt
            cursor2=dbobj.cursor()
            cursor2.execute("UPDATE stock_inventory SET quantity='%s' WHERE product_code='%s'"%(quantity,pcode))
            dbobj.commit()
            cursor1.close()
            cursor2.close()
            print("Inventory Incremented!\n")
        elif x==3:
            pcode=input("Product Code: ")
            qt=int(input("Quantity of Sale: "))
            cursor1=dbobj.cursor()
            cursor1.execute("SELECT * FROM stock_inventory WHERE product_code='%s'"%(pcode))
            result=cursor1.fetchone()
            n=cursor1.rowcount
            if n>=1:
                pinfo=result[2]
                pmrp=result[3]
                pcp=result[4]
                psp=result[5]
                gstcode=result[6]
                gst=result[7]
                quantity=result[8]
                sold=result[9]
                if qt<=quantity:
                    cursor2=dbobj.cursor()
                    cursor2.execute("INSERT INTO stock_sales (product_code,product_info,product_mrp,product_cp,product_sp,gstcode,gst,quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(pcode,pinfo,pmrp,pcp,psp,gstcode,gst,qt))
                    quantity-=qt
                    sold+=qt
                    cursor3=dbobj.cursor()
                    cursor3.execute("UPDATE stock_inventory SET quantity='%s',sold='%s' WHERE product_code='%s'"%(quantity,sold,pcode))
                    dbobj.commit()
                    cursor2.close()
                    cursor3.close()
                    print("Sale Record Added!")
                else:
                    print("Quantity in stock(%d) is lower than sale quantity(%d)!"%(quantity,qt))
                dbobj.commit()
                cursor1.close()
        else:
            print("Something went wrong!")
    except Exception as e:
        print("Exception Error! Something went wrong! "+str(e))
    return

def edit():
    try:
        pcode=input("Product Code of record to edit: ")
        cursor1=dbobj.cursor()
        cursor1.execute("SELECT * FROM stock_inventory WHERE product_code='%s'"%(pcode))
        cursor1.fetchall()
        n=cursor1.rowcount
        if n>=1:
            print("--Select option to edit--")
            print("1) Product Information")
            print("2) Product MRP")
            print("3) Product CP")
            print("4) Product SP")
            print("5) GST/HSN CODE")
            print("6) GST %")
            print("7) Quantity in stock")
            print("8) Sold Quantity")
            x=int(input("Input your choice: "))
            y=input("Input new value of selected option: ")
            if x==1:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET product_info='%s' WHERE product_code='%s'"%(str(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            elif x==2:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET product_mrp='%s' WHERE product_code='%s'"%(float(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            elif x==3:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET product_cp='%s' WHERE product_code='%s'"%(float(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            elif x==4:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET product_sp='%s' WHERE product_code='%s'"%(float(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            elif x==5:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET gstcode='%s' WHERE product_code='%s'"%(str(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            elif x==6:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET gst='%s' WHERE product_code='%s'"%(int(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            elif x==7:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET quantity='%s' WHERE product_code='%s'"%(int(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            elif x==8:
                cursor2=dbobj.cursor()
                cursor2.execute("UPDATE stock_inventory SET sold='%s' WHERE product_code='%s'"%(int(y),pcode))
                dbobj.commit()
                cursor2.close()
                print("Record Updated!")
            else:
                print("Invalid Option/Value Input!")
        else:
            print("No such record found")
        #dbobj.close()
        cursor1.close()
    except Exception as e:
        print("Exception Error! Something Went Wrong! "+str(e)+"\n")
    return

def delete():
    try:
        print("\n--Select the record to delete--")
        print("1) Delete Entire Inventory record")
        print("2) Delete Entire Sales record")
        print("3) Delete specific Inventory record")
        d=input("Enter your choice: ")
        if d=="1":
            cursor1=dbobj.cursor()
            cursor1.execute("DELETE FROM stock_inventory WHERE 1")
            dbobj.commit()
            cursor1.close()
            print("Delete Operation Committed")
        elif d=="2":
            cursor1=dbobj.cursor()
            cursor1.execute("DELETE FROM stock_sales WHERE 1")
            dbobj.commit()
            cursor1.close()
            print("Delete Operation Committed")
        elif d=="3":
            pcode=str(input("Product Code of entry to delete: "))
            cursor1=dbobj.cursor()
            cursor1.execute("DELETE FROM stock_inventory WHERE product_code='%s'"%(pcode))
            dbobj.commit()
            cursor1.close()
            print("Delete Operation Committed")
        else:
            print("Invalid Input!")
        #dbobj.close()
    except Exception as e:
        print("Exception Error! Something went wrong! "+str(e)+"\n")
    return

def view(x):
    #dbobj=conn(database,hostname,username,password)
    if x==1:
        print("\n--Inventory Record--")
        print("Serial | Code | Product Info | MRP | CP | SP | HSN Code | GST% | Quantity | Sold Q.")
        cursor1=dbobj.cursor()
        cursor1.execute("SELECT * FROM stock_inventory WHERE 1")
        result=cursor1.fetchall()
        for z in result:
            strz=""
            for y in z:
                strz=strz+str(y)+" | "
            print(strz+"\n")
        cursor1.close()
    elif x==2:
        print("\n--Sales Record--")
        print("Serial | Code | Product Info | MRP | CP | SP | HSN Code | GST% | Quantity | Total")
        cursor1=dbobj.cursor()
        cursor1.execute("SELECT * FROM stock_sales WHERE 1")
        result=cursor1.fetchall()
        for z in result:
            ctr=0
            total=1
            strz=""
            for y in z:
                strz=strz+str(y)+" | "
                if ctr==5 or ctr==8:
                    total*=y
                ctr+=1
            print(strz+str(total))
        cursor1.close()
    else:
        print("Something went wrong!")
    return

print ("Welcome to Stock Management Python 3.9 CLI") #Greetings
print ("Developed by Reebal Javed Khan a.k.a Zokemore") # Program Info
try:
    print("Kindly provide directory to store databaseinfo file on prompt")
    print("Make sure directory is accessible and have proper permissions")
    print("On GNU+Linux/Unix: /home/user/.config/zetatech/ is recommended ")
    print("On Ms Windows: c:\\Users\\username\\zetatech\\ is recommended ")
    user_dir=input("Enter the directory address: ")
    my_dir = Path(user_dir)
    if not my_dir.is_dir():
        os.makedirs(my_dir)
    my_file = Path(user_dir+"databaseinfo")
    if not my_file.is_file():
        print("MySql Database Information required!")
        #database name, hostname,  username, password input is taken from user for creating MySQL Connection
        #get information from user if it does not exists
        hostname=input("Enter the hostname: ")
        database=input("Enter the database name: ")
        username=input("Enter the username: ")
        password=input("Enter the password: ")
        #database information will be stored in c:/users/public/database/databaseinfo
        file_object=open(my_file,"w")
        file_object.write(database+"\n")
        file_object.write(hostname+"\n")
        file_object.write(username+"\n")
        file_object.write(password+"\n")
        file_object.close()
    else:
        print("Reading Database Info")
        file_object=open(my_file,"r")
        database=str(file_object.readline()).rstrip('\n')
        hostname=str(file_object.readline()).rstrip('\n')
        username=str(file_object.readline()).rstrip('\n')
        password=str(file_object.readline()).rstrip('\n')
        file_object.close()
        #check if database information if database information exists

    print("Connecting to Database")
    #print(database+" "+hostname+" "+username+" "+password)
    global dbobj
    dbobj=conn(database,hostname,username,password)
    #create required tables named "inventory" and "sales" if they do not exist
    mycursor=dbobj.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS stock_inventory (serial INT AUTO_INCREMENT,product_code TEXT NOT NULL,product_info TEXT NOT NULL,product_mrp FLOAT NOT NULL,product_cp FLOAT NOT NULL,product_sp FLOAT NOT NULL,gstcode TEXT NOT NULL,gst INT NOT NULL,quantity INT NOT NULL,sold INT DEFAULT 0,PRIMARY KEY(serial))")
    dbobj.commit()
    mycursor.close()
    mycursor2=dbobj.cursor()
    mycursor2.execute("CREATE TABLE IF NOT EXISTS stock_sales (serial INT AUTO_INCREMENT,product_code TEXT NOT NULL,product_info TEXT NOT NULL,product_mrp FLOAT NOT NULL,product_cp FLOAT NOT NULL,product_sp FLOAT NOT NULL,gstcode TEXT NOT NULL,gst INT NOT NULL,quantity INT NOT NULL,PRIMARY KEY(serial))")
    dbobj.commit()
    mycursor2.close()
except Exception as e:
    print("Initialiazation Failed! Something went wrong "+str(e)+"\n")
    exit()
#init() #Initializing files and databases
while True:
    print ("--Choose from options below--")
    print ("1) Add New Inventory")
    print ("2) Increment Quantity of Existing Inventory")
    print ("3) Edit an Inventory Record")
    print ("4) View Inventory")
    print ("5) Register a Sale")
    print ("6) View Sales Data")
    print ("7) Delete Record")
    print ("8) Exit the Software")
    z=input("Enter your Choice: ")
    if z=="1":
        entry(1)
    elif z=="2":
        entry(2)
    elif z=="3":
        edit()
    elif z=="4":
        view(1)
    elif z=="5":
        entry(3)
    elif z=="6":
        view(2)
    elif z=="7":
        delete()
    elif z=="8":
        break
    else:
        print("Invalid Input!\n")
print ("Exiting.... Have a nice day!")
