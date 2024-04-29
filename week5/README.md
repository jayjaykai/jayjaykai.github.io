"# Task 2: Create database and table in your MySQL server" 
"Create a new database named website." 
![alt text](image.png)
"Create a new table named member, in the website database, designed as below:" 
![alt text](image-1.png)

"Task 3: SQL CRUD" 
"INSERT a new row to the member table where name, username and password mustbe set to test. INSERT additional 4 rows with arbitrary data." 
![alt text](image-2.png)

"SELECT all rows from the member table." 
![alt text](image-3.png)
"SELECT all rows from the member table, in descending order of time." 
![alt text](image-4.png)
"SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4." 
![alt text](image-5.png)
"SELECT rows where username equals to test." 
![alt text](image-6.png)
"SELECT rows where name includes the es keyword." 
![alt text](image-7.png)
"SELECT rows where both username and password equal to test." 
![alt text](image-8.png)
"UPDATE data in name column to test2 where username equals to test." 
![alt text](image-9.png)

"Task 4: SQL Aggregation Functions" 
"SELECT how many rows from the member table." 
![alt text](image-10.png)
"SELECT the sum of follower_count of all the rows from the member table." 
![alt text](image-11.png)
"SELECT the average of follower_count of all the rows from the member table." 
![alt text](image-12.png)
"SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table." 
![alt text](image-13.png)

"Task 5: SQL JOIN" 
"Create a new table named message, in the website database. designed as below:" 
![alt text](image-14.png)
"SELECT all messages, including sender names. We have to JOIN the member table to get that." 
![alt text](image-19.png)
"SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that." 
![alt text](image-20.png)
"Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test." 
![alt text](image-17.png)
"Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username." 
![alt text](image-18.png)
