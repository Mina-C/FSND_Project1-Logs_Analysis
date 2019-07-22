# Reporting Tool

This project sets up a mock PostgreSQL database for a fictional news website. The provided Python script uses the psycopg2 library to query the database and produce a report that answers the following three questions:
    1. What are the most popular three articles of all time?
    2. Who are the most popular article authors of all time?
    3. On which days did more than 1% of requests lead to errors?

## How to run

You need PostgreSQL, Python(ver 3.7) program and Linux-based virtual machine environment(Vagrant and VirtualBox).
    1. To make the virtual machine(VM) online, use the commands "vagrant up". Then log on it with "vagrant ssh".
    2. Please download "newsdata.sql", "report.py" "Vagrantfile". Then put this file into a shared directory.
    (How to make shared directory? - https://www.howtogeek.com/189974/how-to-share-your-computers-files-with-a-virtual-machine/)
    3. To load the data, "cd" into the shared directory and use the command "psql -d news -f newsdata.sql".
    4. To create views for this program, please run "psql -d news -f create_views.sql" to import the views from the "news" database.
    5. Please run the code with "python report.py".

## Program's Design
    
Database contains three tables; articles, authors and log.
Before the python code run, you should create view with "create_view.sql". (Detail is in ##How to run #4) Kindly find the detail of view as below.

## Veiw Detail
1. VIEW1 : edit row log.path into slug form (row : path)
    CREATE VIEW path_to_slug AS
    SELECT REPLACE(path, '/article/','') AS path
    FROM log;
2. VIEW2 : join VIEW1 and table article (row : author, title, num)
    CREATE VIEW articles_views AS
	SELECT articles.author, articles.title, COUNT(path_to_slug.path) AS num 
	FROM articles LEFT JOIN path_to_slug 
	ON articles.slug = path_to_slug.path 
	GROUP BY articles.title, articles.slug, articles.author
	ORDER BY num;
3. VIEW3 : edit table log group by date and status (row : date, status, num)
    CREATE VIEW log_date AS
	SELECT date(time) AS date, status, COUNT(*) as num 
	FROM log 
	GROUP BY date(time), status 
	ORDER BY date(time), status;