import sqlite3

# CREATE A DATABASE
db = sqlite3.connect("series-collection.db")

# CREATE A CURSOR TO CONTROL THE DATABASE
cursor = db.cursor()

# CREATE A TABLE
# cursor.execute("CREATE TABLE series (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
#                "NOT NULL, rating FLOAT NOT NULL)")
"""
cursor - This is the mouse pointer in our database that is going to do all the work.

.execute() - This method will tell the cursor to execute an action. 

CREATE TABLE -  This will create a new table in the database. The name of the table comes after this keyword.

series -  This is the name that we've given the new table we're creating.

() -  The parts that come inside the parenthesis after CREATE TABLE books ( ) are going to be the fields in this table.

id INTEGER PRIMARY KEY -  This is the first field, it's a field called "id" which is of data type INTEGER and it will be
the PRIMARY KEY for this table. The primary key is the one piece of data that will uniquely identify this record in the
table.
  
title varchar(250) NOT NULL UNIQUE -  This is the second field, it's called "title" and it accepts a variable-length 
string composed of characters. The 250 in brackets is the maximum length of the text. NOT NULL means it must have a value
and cannot be left empty. UNIQUE means no two records in this table can have the same title.  

author varchar(250) NOT NULL -  A field that accepts variable-length Strings up to 250 characters called author that 
cannot be left empty.

rating FLOAT NOT NULL -  A field that accepts FLOAT data type numbers, cannot be empty and the field is called rating.
"""


# INSERT INTO THE TABLE
# cursor.execute("INSERT INTO series VALUES(4, 'The Originals', 'L.J Smith', '9.6')")
# db.commit()

"""
Before running the code above,comment out the previous line of code where you are created the table called series. 
Otherwise, you'll get sqlite3.OperationalError: table series already exists.
"""

# SELECT (SELECT statements are used to fetch data from a database)
""" SELECT column_name 
    FROM table_name;"""
# cursor.execute("SELECT author FROM series;")

# ALTER TABLE (Allows you to add a column in a database)
"""ALTER TABLE table_name 
   ADD column_name datatype;"""
# cursor.execute("ALTER TABLE series ADD date integer;")

# UPDATE (UPDATE statements allow you to edit rows in a table.)
""" UPDATE table_name
    SET some_column = some_value
    WHERE some_column = some_value;"""
# cursor.execute("UPDATE series SET date = 2013 WHERE id = 3 ;")

# DELETE (DELETE statements are used to remove rows from a table.)
""" DELETE FROM table_name
    WHERE some_column = some_value;"""
# cursor.execute("DELETE FROM series WHERE id = 4;")

# GROUP BY (GROUP BY is a clause in SQL that is only used with aggregate functions. It is used in collaboration with
# the SELECT statement to arrange identical data into groups.
""" SELECT column_name, COUNT(*)
    FROM table_name
    GROUP BY column_name;"""