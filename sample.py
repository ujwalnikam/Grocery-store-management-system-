# pip install mysql-connector-python
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="2001", database="miniproject")
mycursor = mydb.cursor(buffered=True)
if(mydb):
    print("Connection done successfully")
else:
    print("Connection not done")

dict = {}
############################################


def admin_session():
    print("")
    print("Login successful.")
    print("Admin access")
    while 1:
        print("----------------------------")
        print("1. Add items")
        print("2. Delete items")
        print("3. Veiw users")
        print("4. Block the user")
        print("5. Logout.")
        print("----------------------------")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Add new items")
            it_name = input(str("item name : "))
            it_cost = int(input("item cost : "))
            it_qtt = int(input("item quantity : "))
            query_vals = (it_name, it_cost, it_qtt)

            sqlform = "INSERT into products(name,cost,qtty) values(%s,%s,%s)"
            data = [(it_name, it_cost, it_qtt)]
            mycursor.executemany(sqlform, data)
            mydb.commit()
            print(it_name + " has been added to store ")

        elif user_option == "2":
            print("")
            print("Block User")
            it_name = input(("user name : "))
            sqlform = "delete from unserinfo where name = %s"
            adr = (it_name,)
            mycursor.execute(sqlform, adr)
            mydb.commit()
            print(it_name + " blocked succefully.")

        elif user_option == "3":
            mycursor.execute("SELECT * FROM unserinfo")
            myresult = mycursor.fetchall()
            print("")
            print("Name | Mobile no.")
            print("=========================================")
            for x in myresult:
                print(x[0], "|", x[1])
            print("=========================================")
            print("")

        elif user_option == "4":
            print("")
            print("Delete item")
            it_name = input(("item name : "))
            sqlform = "delete from products where name = %s"
            adr = (it_name,)
            mycursor.execute(sqlform, adr)
            mydb.commit()
            print(it_name + " deleted succefully")

        elif user_option == "5":
            break

        else:
            print("Invalid input")


def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("username : "))
    password = input(str("password : "))
    if username == "ujwal":
        if password == "rdj3000":
            admin_session()
        else:
            print("Incorrect password !")
    else:
        print("Input does not match !")


def user_session():
    print("\nWelcome to user login.")
    print("what you want to purchase ")
    mycursor.execute("SELECT * FROM products")
    myresult = mycursor.fetchall()
    print("")
    print("Items Price Available")
    print("=========================================")
    for x in myresult:
        print(x[0], "|", x[1], "|", x[2])
    print("=========================================")
    print("")
    it_name = input(str("Enter Item name : "))
    it_qtt = int(input("Enter Item quantity : "))

    sql = "select qtty from products where name = %s"
    adr = (it_name,)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchone()
    # mydb.commit()
    for x in myresult:
        available = x
    remain = available - it_qtt
    sql = "UPDATE products SET qtty=%s WHERE name = %s"
    adr = (remain, it_name,)
    mycursor.execute(sql, adr)
    mydb.commit()
    print("You purchase " + it_name + " successfully.")

    sql = "select cost from products where name = %s"
    adr = (it_name,)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchone()
    global dict
    dict[it_name] = myresult[0]
    print("")
    print("Do you want to purchase more items (y/n)")
    user_option = input(str("Option : "))
    if user_option == "y":
        user_session()
    else:
        # print(dict)
        sumt = 0
        print("")
        print("=========================================")
        for i in dict:
            print(" Item : ", i, "Cost : ", dict[i])
            sumt = sumt + dict[i]
        print("=========================================")
        print(" Your Bill : ", sumt)
        print("-----------------------------------------")
        print("\t Thank you . Visit again !")
        print("-----------------------------------------")
        dict.clear()


def auth_user():
    print("")
    print("User Login\n")
    print("1.Sign in / 2.Create account")
    user_option = input(str("Option : "))

    if user_option == "1":
        username = input(str("username : "))
        phone = int(input("phone : "))
        sql = "SELECT * FROM unserinfo where mob = %s"
        adr = (phone,)
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0] == username:
                print("")
                print("Welcome back ", x[0])
                user_session()
            else:
                print("Invalid input")

    elif user_option == "2":
        username = input(str("username : "))
        phone = int(input("phone : "))
        sqlform = "INSERT into unserinfo(name,mob) values(%s,%s)"
        data = [(username, phone)]
        mycursor.executemany(sqlform, data)
        mydb.commit()
        print("Account created successfully !")
        user_session()


def main():
    print("")
    print("=========================================")
    print("------------Welocome to My Shop----------")
    while 1:
        print("")
        print("1. Login as Admin ")
        print("2. Login as User ")
        print("3. End !")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_admin()
        elif user_option == "2":
            auth_user()
        elif user_option == "3":
            break
        else:
            print("Invalid input")


main()
