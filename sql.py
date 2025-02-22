import sqlite3

#connect the database
connection = sqlite3.connect ("student.db")

##Create a cursor object to insert records , create table , retrive
cursor = connection.cursor()

#Create the table
table_info= """
    create table STUDENT(NAME varchar(25) , 
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT );
"""
cursor.execute(table_info)
##Insert some more records
cursor.execute("""Insert into STUDENT values('Krish','DS','A',90)""")
cursor.execute("INSERT INTO STUDENT VALUES ('Krish', 'DS', 'A', 90)")
cursor.execute("INSERT INTO STUDENT VALUES ('Rohan', 'CS', 'B', 85)")
cursor.execute("INSERT INTO STUDENT VALUES ('Sneha', 'IT', 'A', 88)")
cursor.execute("INSERT INTO STUDENT VALUES ('Aisha', 'AI', 'C', 92)")
cursor.execute("INSERT INTO STUDENT VALUES ('Rahul', 'ML', 'B', 80)")
cursor.execute("INSERT INTO STUDENT VALUES ('Neha', 'Cyber', 'A', 89)")

#Display the records
print("The inserted records are:")

data = cursor.execute('''select * from STUDENT''')

for row in data:
    print(row)

#close the connection
connection.commit()
connection.close()
