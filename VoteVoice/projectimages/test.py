import mysql.connector

#connecting to the Database
db = mysql.connector.connect(
    host="sql3.freemysqlhosting.net",
    user="sql3355866",
    passwd="zQfhdzzy2f",
    db="sql3355866"
)

#Creating a cursor that will write SQL code and interact with the databse
global cursor
cursor = db.cursor()

sql="UPDATE posts SET rownum = 1 WHERE subject = 'b'"

cursor.execute(sql)

db.commit()


#get_posts_left = "SELECT COUNT(*) FROM posts"
#cursor.execute(get_posts_left)
#posts_string = str(cursor.fetchall())
#posts1 = posts_string.replace("'", "")
#posts2 = posts1.replace("[", "")
#posts3 = posts2.replace("]", "")
#posts4 = posts3.replace("(", "")
#posts5 = posts4.replace(")", "")
#posts6 = posts5.replace(",", "")
#posts_left = int(posts6)


#while posts_left >= 0:

#updating posts left at the end of each cycle
#get_posts_left = "SELECT COUNT(*) FROM posts"
