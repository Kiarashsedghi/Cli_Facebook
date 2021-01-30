import pymssql
from sys import argv


def facebookDbConnection():
    server_properties = {
        'host': '127.0.0.1',
        'database': 'Facebook',
        'user': 'SA',
        'password': '@1378Alisajad'
    }

    conn = pymssql.connect(**server_properties)
    conn.autocommit(True)
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=.\SQL2019;'
                      'Database=Facebook;'
                      'Trusted_Connection=yes;')
    return conn

def show(tableName, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ' + tableName)

    print("Content of "+tableName)
    for row in cursor:
        print(row)
    print("\n")

def profileHlep():
    print("0.Exit")
    print("1.Colleges")
    print("2.Hobbies")
    print("3.Liked")
    print("4.Schools")
    print("5.SocialLinks")
    print("6.WorkPlaces")
    return

def likedTables():
    print("0.Exit")
    print("1.LikedArtists")
    print("2.LikedAthletes")
    print("3.LikedBooks")
    print("4.LikedMovies")
    print("5.LikedSportTeams")
    print("6.LikedTVShows")
    return

def showCommands():
    print("0.Exit\n1.Add\n2.Edit\n3.Delete\n")
    return

def operateColleges(command, userId, conn):

    cursor = conn.cursor()
    collegeName = ""
    concentration = ""
    Graduated = 0
    StartDate = ""



    if command == 1: # 1 -> Add

        columnNames = "UserID"
        columnValues = ""

        collegeName = input("College Name: ")
        columnNames = columnNames + ",Name"
        columnValues = columnValues + "\'" + collegeName + "\'"

        ans = int(input("do you want enter Concentration? \n0.no\n1.yes\n"))
        if ans == 1:
            concentration = input("Concentration: ")
            columnNames = columnNames + "," + "Concentration"
            columnValues = columnValues + "," + "\'" + concentration + "\'"

        ans = int(input("do you want enter Graduated? \n0.no\n1.yes\n"))
        if ans == 1:
            Graduated = input("Graduated: \n0.no\n1.yes\n")
            columnNames = columnNames + "," + "Graduated"
            columnValues = columnValues + "," + str(Graduated)

        ans = int(input("do you want enter Start Date? \n0.no\n1.yes\n"))
        if ans == 1:
            StartDate = input("date format is yyyy-mm-dd\n")
            columnNames = columnNames + "," + "StartDate"
            columnValues = columnValues + "," + "\'" + StartDate + "\'"
        query = "INSERT INTO Colleges (" + columnNames + ") VALUES (" + userId +","+ columnValues + ")"
        print(query)
        cursor.execute(query)
        conn.commit()

    elif command == 2: # 2 -> Edit
        show("Colleges", conn)
        Id = input("Enter Id: ")
        columns = ""

        ans = int(input("do you want edit College Name? \n0.no\n1.yes\n"))
        if ans == 1:
            collegeName = input("College Name: ")
            columns = columns + "Name = " + "\'" + collegeName + "\'" + ','

        ans = int(input("do you want edit Concentration? \n0.no\n1.yes\n"))
        if ans == 1:
            concentration = input("Concentration: ")
            columns = columns + "Concentration = " + "\'" + concentration + "\'" + ','


        ans = int(input("do you want edit Graduated? \n0.no\n1.yes\n"))
        if ans == 1:
            Graduated = input("Graduated: \n0.no\n1.yes\n")
            columns = columns + "Graduated = " + str(Graduated) + ','

        ans = int(input("do you want edit Start Date? \n0.no\n1.yes\n"))
        if ans == 1:
            StartDate = input("date format is yyyy-mm-dd\n")
            columns = columns + "StartDate = " + "\'" + StartDate + "\'"
        
        #last character of a string
        if columns[-1]==',':
            columns = columns[:-1]

        query = 'UPDATE Colleges SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()

    elif command == 3: # 3 -> Delete
        show("Colleges", conn)
        Id = input("Enter Id: ")
        query = 'DELETE FROM Colleges WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()
    return

def operateSchools(command, userId, conn):

    cursor = conn.cursor()
    schoolName = ""
    classYear = ""

    if command == 1: # 1 -> Add

        columnNames = "UserID"
        columnValues = ""
        schoolName = input("School Name: ")
        columnNames = columnNames + ",Name"
        columnValues = columnValues + "\'" + schoolName + "\'"

        ans = int(input("do you want enter classYear? \n0.no\n1.yes\n"))
        if ans == 1:
            classYear = input("Class Year: ")
            columnNames = columnNames + "," + "ClassYear"
            columnValues = columnValues + "," + "\'" + classYear + "\'"
        
        query = 'INSERT INTO Schools (' + columnNames + ') VALUES ('+ userId + ',' + columnValues + ')'
        print(query)
        cursor.execute(query)
        conn.commit()

    elif command == 2: # 2 -> Edit
        show("Schools",conn)
        Id = input("Enter Id:")

        columns = ""

        ans = int(input("do you want edit School Name? \n0.no\n1.yes\n"))
        if ans == 1:
            schoolName = input("School Name: ")
            columns = columns + "Name = " + "\'" + schoolName + "\'" + ','

        
        ans = int(input("do you want edit Class Year? \n0.no\n1.yes\n"))
        if ans == 1:
            classYear = input("Class Year")
            columns = columns + "ClassYear = " + "\'" + classYear + "\'"
        
        #last character of a string
        if columns[-1]==',':
            columns = columns[:-1]

        
        query = 'UPDATE Schools SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()

    elif command == 3: # 3 -> Delete
        show("Schools",conn)
        Id = input("Enter Id: ")

        query = 'DELETE FROM Schools WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()

    return

def operateHobbies(command, userId, conn):
    cursor = conn.cursor()
    
    if command == 1: # 1 -> Add
        Name = input("Enter a name: ")
        query = 'INSERT INTO Hobbies (UserID,Name) VALUES ( ' + userId + ',' + "\'" + Name + "\'" + ' )'
        print(query)
        cursor.execute(query)
        conn.commit()
    elif command == 2: # 2 -> Edit
        show("Hobbies",conn)
        Id = input("Enter Id: ")
        Name = input("Enter new name: ")
        query = 'UPDATE Hobbies SET Name = ' + "\'" + Name + "\'" + ' WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query) 
        conn.commit()
    elif command == 3: # 3 -> Delete
        show("Hobbies",conn)
        Id = input("Enter Id: ")
        query = 'DELETE FROM Hobbies WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()

    return 

def operateLikes(command, tableName, userId, conn):

    cursor = conn.cursor()
    
    if command == 1: # 1 -> Add
        Name = input("Enter a name: ")
        query = 'INSERT INTO ' + tableName + ' (UserID,Name) VALUES ( ' + userId + ',' + "\'" + Name + "\'" + ' )'
        print(query)
        cursor.execute(query)
        conn.commit()
    elif command == 2: # 2 -> Edit
        show(tableName,conn)
        Id = input("Enter Id:")
        Name = input("Enter new name:")
        query = 'UPDATE '+ tableName + ' SET Name = ' + "\'" + Name + "\'" + ' WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query) 
        conn.commit()
    elif command == 3: # 3 -> Delete
        show(tableName,conn)
        Id = input("Enter Id:")
        query = 'DELETE FROM ' + tableName + ' WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()
    return

def operateSocialLinks(command, userId, conn):

    cursor = conn.cursor()
    socialNetwork = ""
    accountName = ""
    WebAddr = ""


    if command == 1: # 1 -> Add

        columnNames = "UserID"
        columnValues = ""

        socialNetwork = input("Social Network Name: ")
        columnNames = columnNames + ",SocialNetwork"
        columnValues = columnValues + "\'" + socialNetwork + "\'"

        accountName = input("Account Name: ")
        columnNames = columnNames + "," + "AccountName"
        columnValues = columnValues + "," + "\'" + accountName + "\'"

        ans = int(input("do you want enter Website Address? \n0.no\n1.yes\n"))
        if ans == 1:
            WebAddr = input("Website Address: ")
            columnNames = columnNames + "," + "WebsiteAddress"
            columnValues = columnValues + "," + "\'" + WebAddr + "\'"
        
        query = 'INSERT INTO SocialLinks (' + columnNames + ') VALUES (' + userId + ',' + columnValues + ')'
        print(query)
        cursor.execute(query)
        conn.commit()

    elif command == 2: # 2 -> Edit
        show('SocialLinks', conn)
        Id = input("Enter Id:")

        columns = ""

        ans = int(input("do you want edit Social Network Name? \n0.no\n1.yes\n"))
        if ans == 1:
            socialNetwork = input("Social Network Name: ")
            columns = columns + "socialNetwork = " + "\'" + socialNetwork + "\'" + ','

       
        ans = int(input("do you want edit Account Name? \n0.no\n1.yes\n"))
        if ans == 1:
            accountName = input("Account Name")
            columns = columns + "," + "AccountName = " + "\'" + accountName + "\'" + ','
        
       
        ans = int(input("do you want edit Website Address? \n0.no\n1.yes\n"))
        if ans == 1:
            WebAddr = input("Website Address")
            columns = columns + "," + "WebsiteAddress = " + "\'" + WebAddr + "\'" + ','
        
        #last character of a string
        if columns[-1]==',':
            columns = columns[:-1]
        
        query = 'UPDATE SocialLinks SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()
    elif command == 3: # 3 -> Delete
        show('SocialLinks', conn)
        Id = input("Enter Id:")

        query = 'DELETE FROM SocialLinks WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()
    return

def operateWorkPlaces(command, userId, conn):
    cursor = conn.cursor()
    workPlaceName = ""
    jobTitle = ""
    location = ""
    Description = ""
    StartDate = ""


    if command == 1: # 1 -> Add

        columnNames = "UserID"
        columnValues = ""

        workPlaceName = input("Work Place Name: ")
        columnNames = columnNames + ",Name"
        columnValues = columnValues + "\'" + workPlaceName + "\'"
        
        ans = int(input("do you want enter Job Title? \n0.no\n1.yes\n"))
        if ans == 1:
            jobTitle = input("Job Title: ")
            columnNames = columnNames + "," + "JobTitle"
            columnValues = columnValues + "," + "\'" + jobTitle + "\'"
        
        
        ans = int(input("do you want enter Location? \n0.no\n1.yes\n"))
        if ans == 1:
            location = input("Location: ")
            columnNames = columnNames + "," + "Location"
            columnValues = columnValues + "," + "\'" + location + "\'"
           
        ans = int(input("do you want enter Description? \n0.no\n1.yes\n"))
        if ans == 1:
            Description = input("Description: ")
            columnNames = columnNames + "," + "Description"
            columnValues = columnValues + "," + "\'" + Description + "\'"
            
        ans = int(input("do you want enter StartDate? \n0.no\n1.yes\n"))
        if ans == 1:
            StartDate = input("date format is yyyy-mm-dd\n")
            columnNames = columnNames + "," + "StartDate"
            columnValues = columnValues + "," + "\'" + StartDate + "\'"
        
        query = 'INSERT INTO WorkPlaces (' + columnNames + ') VALUES ('+ userId + ',' + columnValues + ')'
        print(query)
        cursor.execute(query)
        conn.commit()
    elif command == 2: # 2 -> Edit
        show('WorkPlaces', conn)
        Id = input("Enter Id:")

        columns = ""

        
        ans = int(input("do you want edit Work Place Name? \n0.no\n1.yes\n"))
        if ans == 1:
            workPlaceName = input("Work Place Name: ")
            columns = columns + "Name = " + "\'" + workPlaceName + "\'" + ','

        
        ans = int(input("do you want edit Job Title? \n0.no\n1.yes\n"))
        if ans == 1:
            jobTitle = input("Job Title: ")
            columns = columns + "JobTitle = " + "\'" + jobTitle + "\'" + ','

        
        ans = int(input("do you want edit Location? \n0.no\n1.yes\n"))
        if ans == 1:
            location = input("Location: ")
            columns = columns + "Location = " + "\'" + location + "\'" + ','

        
        ans = int(input("do you want edit Descriptions? \n0.no\n1.yes\n"))
        if ans == 1:
            Description = input("Description: ")
            columns = columns + "Description = " + "\'" + Description + "\'" + ','

        
        ans = int(input("do you want edit Start Date? \n0.no\n1.yes\n"))
        if ans == 1:
            StartDate = input("date format is: yyyy-mm-dd")
            columns = columns + "StartDate = " + "\'" +  StartDate + "\'" + ','
        
        #last character of a string
        if columns[-1]==',':
            columns = columns[:-1]

        query = 'UPDATE WorkPlaces SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()

    elif command == 3: # 3 -> Delete
        show('WorkPlaces', conn)
        Id = input("Enter Id:")
        query = 'DELETE FROM WorkPlaces WHERE ID = ' + Id + ' AND UserID = ' + userId
        print(query)
        cursor.execute(query)
        conn.commit()
    return


command = 1
conn = facebookDbConnection()
userId = argv[1]

print("------------------------------")

while command>0:
    viewData = 0
    profileHlep()
    print("------------------------------")
    command = int(input("Enter command number: "))
    if command == 0: # Exit
        print("Exiting from profile")
        break
    elif command == 1: # Colleges
        show("Colleges", conn)
        
        while command > 0:
            print("------------------------------")
            showCommands()
            command = int(input("Enter command number: "))
            if command != 0:
                operateColleges(command, userId, conn)
                viewData = int(input("show data?\n0.no\n1.yes\n"))
                if viewData == 1:
                    show("Colleges",conn)
            
        command = 20
    elif command == 2: # Hobbies
        show("Hobbies", conn)
       
        while command > 0:
            print("------------------------------")
            showCommands()
            command = int(input("Enter command number: "))
            if command != 0:
                operateHobbies(command, userId, conn)
                viewData = int(input("show data?\n0.no\n1.yes\n"))
                if viewData == 1:
                    show("Hobbies",conn)
        command = 20

    elif command == 3: # Liked
        
        while command>0:
            likedTables()
            print("------------------------------")
            command = int(input("Enter command number: "))

            if command == 1: # LikedArtists
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    if command != 0:
                        operateLikes(command, "LikedArtists", userId, conn)
                        viewData = int(input("show data?\n0.no\n1.yes\n"))
                        if viewData == 1:
                            show("LikedArtists",conn)
                command = 20
            elif command == 2: # LikedAthletes
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    if command != 0:
                        operateLikes(command, "LikedAthletes", userId, conn)
                        viewData = int(input("show data?\n0.no\n1.yes\n"))
                        if viewData == 1:
                            show("LikedAthletes",conn)
                command = 20
            elif command == 3: # LikedBooks
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    if command != 0:
                        operateLikes(command, "LikedBooks", userId, conn)
                        viewData = int(input("show data?\n0.no\n1.yes\n"))
                        if viewData == 1:
                            show("LikedBooks",conn)
                command = 20
            elif command == 4: # LikedMovies
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    if command != 0:
                        operateLikes(command, "LikedMovies", userId, conn)
                        viewData = int(input("show data?\n0.no\n1.yes\n"))
                        if viewData == 1:
                            show("LikedMovies",conn)
                command = 20
            elif command == 5: # LikedSportTeams
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    if command != 0:
                        operateLikes(command, "LikedSportTeams", userId, conn)
                        viewData = int(input("show data?\n0.no\n1.yes\n"))
                        if viewData == 1:
                            show("LikedSportTeams",conn)
                command = 20
            elif command == 6: # LikedTVShows
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    if command != 0:
                        operateLikes(command, "LikedTVShows", userId, conn)
                        viewData = int(input("show data?\n0.no\n1.yes\n"))
                        if viewData == 1:
                            show("LikedTVShows",conn)
                command = 20
            
    elif command == 4: # Schools
        show("Schools", conn)
        while command > 0:
            print("------------------------------")
            showCommands()
            command = int(input("Enter command number: "))
            if command != 0:
                operateSchools(command, userId, conn)
                viewData = int(input("show data?\n0.no\n1.yes\n"))
                if viewData == 1:
                    show("Schools",conn)
        command = 20
    elif command == 5: # SocialLinks
        show("SocialLinks", conn)
        while command > 0:
            print("------------------------------")
            showCommands()
            command = int(input("Enter command number: "))
            if command != 0:
                operateSocialLinks(command, userId, conn)
                viewData = int(input("show data?\n0.no\n1.yes\n"))
                if viewData == 1:
                    show("SocialLinks",conn)
        command = 20
    elif command == 6: # WorkPlaces
        show("WorkPlaces", conn)
        while command > 0:
            print("------------------------------")
            showCommands()
            command = int(input("Enter command number: "))
            if command != 0:
                operateWorkPlaces(command, userId, conn)
                viewData = int(input("show data?\n0.no\n1.yes\n"))
                if viewData == 1:
                    show("WorkPlaces",conn)
        command = 20
    else:
        print("Invalid command number!\n")
