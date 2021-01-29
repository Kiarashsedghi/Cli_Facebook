import pyodbc

def facebookDbConnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=.\SQL2019;'
                      'Database=Facebook;'
                      'Trusted_Connection=yes;')
    return conn

def show(tableName, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ' + tableName)

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
    print("2.LikedAthlites")
    print("3.LikedBooks")
    print("4.LikedMovies")
    print("5.LikedSportTeams")
    print("6.LikedTVShows")
    return

def showCommands():
    print("1.Add\n2.Edit\n3.Delete")
    return

def showCollegesCommands():
    print("0.Exit")
    print("1.College Name")
    print("2.Concentration")
    print("3.Graduated")
    print("4.Start Date")
    return

def operateColleges(command, userId, conn):

    cursor = conn.cursor()
    collegeName = ""
    concentration = ""
    Graduated = ""
    StartDate = ""

    showCollegesCommands()

    if command == 1: # 1 -> Add
        showCollegesCommands()
        hasValue = 0

        columnsDic = dict()
        columnNames = ""
        columnValues = ""

        while command>0:
            print("Please Enter command number: ")
            command = input()
            if command == 0 and collegeName == "" and hasValue:
                print("College Name can't be empty\n")
                command = 20
            elif command == 1: # College Name
                collegeName = input()
                columnsDic["Name"] = collegeName
            elif command == 2: # Concentration
                concentration = input()
                columnsDic["Concentration"] = concentration
                hasValue = 1
            elif command == 3: # Graduated
                print("0.no\n1.yes\n")
                Graduated = input()
                columnsDic["Graduated"] = Graduated
                hasValue = 1
            elif command == 4: # Start Date
                print("date format is: yyyy-mm-dd")
                StartDate = input()
                columnsDic["StartDate"] = StartDate
                hasValue = 1
        
        for key in columnsDic:
            if columnsDic[key] != "":
                columnNames = columnNames + key + ","
                columnValues = columnValues + columnsDic[key] + ","
        
        #removing last comma
        columnNames = columnNames[:-1]
        columnValues = columnValues[:-1]

        cursor.execute('INSERT INTO Colleges (' + columnNames + ') VALUES (' + columnValues + ') WHERE UserID = ' + userId)
        conn.commit()
    elif command == 2: # 2 -> Edit
        print("Enter Id: ")
        Id = input()

        showCollegesCommands()
        columnsDic = dict()
        columns = ""

        while command>0:
            print("Please Enter command number: ")
            command = input()

            if command == 1: # College Name
                collegeName = input()
                columnsDic["Name"] = collegeName
            elif command == 2: # Concentration
                concentration = input()
                columnsDic["Concentration"] = concentration

            elif command == 3: # Graduated
                print("0.no\n1.yes\n")
                Graduated = input()
                columnsDic["Graduated"] = Graduated

            elif command == 4: # Start Date
                print("date format is: yyyy-mm-dd")
                StartDate = input()
                columnsDic["StartDate"] = StartDate
        
        for key in columnsDic:
            if columnsDic[key] != "":
                columns = columns + key + ' = ' + columnsDic[key] + ','
        
        #removing last comma
        columns = columns[:-1]

        cursor.execute('UPDATE Colleges SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()

    elif command == 3: # 3 -> Delete
        print("Enter Id:")
        Id = input()

        cursor.execute('DELETE FROM Colleges WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()
    return

def showSchoolsCommands():
    print("0.Exit")
    print("1.School Name")
    print("2.Class Year")
    return

def operateSchools(command, userId, conn):

    cursor = conn.cursor()
    schoolName = ""
    classYear = ""

    showCollegesCommands()

    if command == 1: # 1 -> Add
        showSchoolsCommands()
        hasValue = 0

        columnsDic = dict()
        columnNames = ""
        columnValues = ""

        while command>0:
            print("Please Enter command number:")
            command = input()
            if command == 0 and schoolName == "" and hasValue:
                print("School Name can't be empty")
                command = 20
            elif command == 1: # School Name
                schoolName = input()
                columnsDic["Name"] = schoolName
            elif command == 2: # Class Year
                classYear = input()
                columnsDic["ClassYear"] = classYear
                hasValue = 1
        
        for key in columnsDic:
            if columnsDic[key] != "":
                columnNames = columnNames + key + ","
                columnValues = columnValues + columnsDic[key] + ","
        
        #removing last comma
        columnNames = columnNames[:-1]
        columnValues = columnValues[:-1]

        cursor.execute('INSERT INTO Schools (' + columnNames + ') VALUES (' + columnValues + ') WHERE UserID = ' + userId)
        conn.commit()
    elif command == 2: # 2 -> Edit
        print("Enter Id:")
        Id = input()

        showSchoolsCommands()
        columnsDic = dict()
        columns = ""

        while command>0:
            print("Please Enter command number:")
            command = input()

            if command == 1: # School Name
                schoolName = input()
                columnsDic["Name"] = schoolName
            elif command == 2: # Class Year
                classYear = input()
                columnsDic["ClassYear"] = classYear

        
        for key in columnsDic:
            if columnsDic[key] != "":
                columns = columns + key + ' = ' + columnsDic[key] + ','
        
        #removing last comma
        columns = columns[:-1]

        cursor.execute('UPDATE Schools SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()

    elif command == 3: # 3 -> Delete
        print("Enter Id:")
        Id = input()

        cursor.execute('DELETE FROM Schools WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()

    return

def operateHobbies(command, userId, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Hobbies')
    
    if command == 1: # 1 -> Add
        print("Enter a name:")
        Name = input()
        cursor.execute('INSERT INTO Hobbies (Name) VALUES ( ' + Name + ' ) WHERE UserID = ' + userId)
        conn.commit()
    elif command == 2: # 2 -> Edit
        print("Enter Id:")
        Id = input()
        print("Enter new name:")
        Name = input()
        cursor.execute('UPDATE Hobbies SET Name = '+ Name + ' WHERE ID = ' + Id + ' AND UserID = ' + userId) 
        conn.commit()
    elif command == 3: # 3 -> Delete
        print("Enter Id:")
        Id = input()
        cursor.execute('DELETE FROM Hobbies WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()
    cursor.execute('SELECT * FROM Hobbies')
    return 

def operateLikes(command, tableName, userId, conn):

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ' + tableName)
    
    if command == 1: # 1 -> Add
        print("Enter a name: ")
        Name = input()
        query = 'INSERT INTO ' + tableName + ' (Name) VALUES ( ' + Name + ' ) WHERE UserID = ' + userId
        cursor.execute(query3)
        conn.commit()
    elif command == 2: # 2 -> Edit
        print("Enter Id:")
        Id = input()
        print("Enter new name:")
        Name = input()
        cursor.execute('UPDATE '+ tableName + ' SET Name = '+ Name + ' WHERE ID = ' + Id + ' AND UserID = ' + userId) 
        conn.commit()
    elif command == 3: # 3 -> Delete
        print("Enter Id:")
        Id = input()
        cursor.execute('DELETE FROM ' + tableName + ' WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()
    cursor.execute('SELECT * FROM ' + tableName)
    return

def showSocialLinksCommands():
    print("0.Exit")
    print("1.Social Network Name")
    print("2.Account Name")
    print("3.Website Address")
    return

def operateSocialLinks(command, userId, conn):

    cursor = conn.cursor()
    socialNetwork = ""
    accountName = ""
    WebAddr = ""

    showSocialLinksCommands()

    if command == 1: # 1 -> Add
        showCollegesCommands()
        hasValue = 0

        columnsDic = dict()
        columnNames = ""
        columnValues = ""

        while command>0:
            print("Please Enter command number:")
            command = input()
            if command == 0 and socialNetwork == ""  and accountName == "" and hasValue:
                print("social Network Name or account Name can't be empty")
                command = 20
            elif command == 1: # Social Network Name
                collegeName = input()
                columnsDic["Name"] = collegeName
            elif command == 2: # Account Name
                accountName = input()
                columnsDic["AccountName"] = accountName
            elif command == 3: # Website Address
                WebAddr = input()
                columnsDic["WebsiteAddress"] = WebAddr
                hasValue = 1
        
        for key in columnsDic:
            if columnsDic[key] != "":
                columnNames = columnNames + key + ","
                columnValues = columnValues + columnsDic[key] + ","
        
        #removing last comma
        columnNames = columnNames[:-1]
        columnValues = columnValues[:-1]

        cursor.execute('INSERT INTO SocialLinks (' + columnNames + ') VALUES (' + columnValues + ') WHERE UserID = ' + userId)
        conn.commit()
    elif command == 2: # 2 -> Edit
        print("Enter Id:")
        Id = input()

        showSocialLinksCommands()
        columnsDic = dict()
        columns = ""

        while command>0:
            print("Please Enter command number:")
            command = input()

            if command == 1: # Social Network Name
                socialNetwork = input()
                columnsDic["Name"] = socialNetwork
            elif command == 2: # Account Name
                accountName = input()
                columnsDic["AccountName"] = accountName

            elif command == 3: # Website Address
                WebAddr = input()
                columnsDic["WebsiteAddress"] = WebAddr
        
        for key in columnsDic:
            if columnsDic[key] != "":
                columns = columns + key + ' = ' + columnsDic[key] + ','
        
        #removing last comma
        columns = columns[:-1]

        cursor.execute('UPDATE SocialLinks SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()

    elif command == 3: # 3 -> Delete
        print("Enter Id:")
        Id = input()

        cursor.execute('DELETE FROM SocialLinks WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()
    return

def showWorkPlacesCommands():
    print("0.Exit")
    print("1.Work Place Name")
    print("2.Job Title")
    print("3.Location")
    print("4.Description")
    print("5.Start Date")
    return

def operateWorkPlaces(command, userId, conn):
    cursor = conn.cursor()
    workPlaceName = ""
    jobTitle = ""
    location = ""
    Description = ""
    StartDate = ""

    showWorkPlacesCommands()

    if command == 1: # 1 -> Add
        showWorkPlacesCommands()
        hasValue = 0

        columnsDic = dict()
        columnNames = ""
        columnValues = ""

        while command>0:
            print("Please Enter command number:")
            command = input()
            if command == 0 and workPlaceName == "" and hasValue:
                print("Work Place Name can't be empty")
                command = 20
            elif command == 1: # Work Place Name
                workPlaceName = input()
                columnsDic["Name"] = workPlaceName
            elif command == 2: # Job Title
                jobTitle = input()
                columnsDic["JobTitle"] = jobTitle
                hasValue = 1
            elif command == 3: # Location
                location = input()
                columnsDic["Location"] = location
                hasValue = 1
            elif command == 4: # Description
                Description = input()
                columnsDic["Description"] = Description
            elif command == 5: # Start Date
                print("date format is: yyyy-mm-dd")
                StartDate = input()
                columnsDic["StartDate"] = StartDate
                hasValue = 1
        
        for key in columnsDic:
            if columnsDic[key] != "":
                columnNames = columnNames + key + ","
                columnValues = columnValues + columnsDic[key] + ","
        
        #removing last comma
        columnNames = columnNames[:-1]
        columnValues = columnValues[:-1]

        cursor.execute('INSERT INTO WorkPlaces (' + columnNames + ') VALUES (' + columnValues + ') WHERE UserID = ' + userId)
        conn.commit()
    elif command == 2: # 2 -> Edit
        print("Enter Id:")
        Id = input()

        showWorkPlacesCommands()
        columnsDic = dict()
        columns = ""

        while command>0:
            print("Please Enter command number:")
            command = input()

            if command == 1: # Work Place Name
                workPlaceName = input()
                columnsDic["Name"] = workPlaceName
            elif command == 2: # Job Title
                jobTitle = input()
                columnsDic["JobTitle"] = jobTitle

            elif command == 3: # Location
                location = input()
                columnsDic["Location"] = location
            elif command == 4: # Descriptions
                Description = input()
                columnsDic["Description"] = Description
            elif command == 5: # Start Date
                print("date format is: yyyy-mm-dd")
                StartDate = input()
                columnsDic["StartDate"] = StartDate
        
        for key in columnsDic:
            if columnsDic[key] != "":
                columns = columns + key + ' = ' + columnsDic[key] + ','
        
        #removing last comma
        columns = columns[:-1]

        cursor.execute('UPDATE WorkPlaces SET ' + columns + ' WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()

    elif command == 3: # 3 -> Delete
        print("Enter Id:")
        Id = input()

        cursor.execute('DELETE FROM WorkPlaces WHERE ID = ' + Id + ' AND UserID = ' + userId)
        conn.commit()
    return


command = 1
conn = facebookDbConnection()
userId = 1

while command>0:
    viewData = 0
    profileHlep()
    command = int(input("Enter command number: "))
    if command == 1: # Colleges
        show("Colleges", conn)
        
        while command > 0:
            print("------------------------------")
            showCommands()
            command = int(input("Enter command number: "))
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
            operateHobbies(command, userId, conn)
            viewData = int(input("show data?\n0.no\n1.yes\n"))
            if viewData == 1:
                show("Hobbies",conn)
        command = 20

    elif command == 3: # Liked
        likedTables()
        
        while command>0:
            print("------------------------------")
            command = int(input("Enter command number: "))

            if command == 1: # LikedArtists
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    operateLikes(command, "LikedArtists", userId, conn)
                    viewData = int(input("show data?\n0.no\n1.yes\n"))
                    if viewData == 1:
                        show("LikedArtists",conn)
                command = 20
            elif command == 2: # LikedAthlites
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number: "))
                    operateLikes(command, "LikedAthlites", userId, conn)
                    viewData = int(input("show data?\n0.no\n1.yes\n"))
                    if viewData == 1:
                        show("LikedAthlites",conn)
                command = 20
            elif command == 3: # LikedBooks
                
                while command>0:
                    print("------------------------------")
                    showCommands()
                    command = int(input("Enter command number"))
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
                    operateLikes(command, "LikedTVShows", userId, conn)
                    viewData = int(input("show data?\n0.no\n1.yes\n"))
                    if viewData == 1:
                        show("LikedTVShows",conn)
                command = 20
            else:
                print("Invalid command!\n")  
            
    elif command == 4: # Schools
        show("Schools", conn)
        while command > 0:
            print("------------------------------")
            showCommands()
            command = int(input("Enter command number: "))
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
            operateWorkPlaces(command, userId, conn)
            viewData = int(input("show data?\n0.no\n1.yes\n"))
            if viewData == 1:
                show("WorkPlaces",conn)
        command = 20
    else:
        print("Invalid command number!\n")