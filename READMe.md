# Reporting Tool

Reporting Tool prints out a report based on the data in the "news" database.
This reporting tool is a Python program using the psycopg2 module to connect to the database.

## How to run

You need database, python program and Linux-based virtual machine environment.
Please download database here ; https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip.
Please run python code in Linux-based virtual machine where the PostgreSQL database is located.

## Program's Design

Database contains three tables; articles, authors and log.

This program returns below questions based on the data in the database:
1. What are the most popular three articles of all time? (query1)
2. Who are the most popular article authors of all time? (query2)
3. On which days did more than 1% of requests lead to errors? (query3)

Three views will be created during the program.
Please find the detail in the following information.

## Veiw Detail
1. VIEW1 : edit row log.path into slug form (row : path)
2. VIEW2 : join VIEW1 and table article (row : author, title, num)
3. VIEW3 : edit table log group by date and status (row : date, status, num)