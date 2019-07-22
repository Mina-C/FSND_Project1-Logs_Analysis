#! /usr/bin/env python3

import psycopg2
import datetime

try:
    db = psycopg2.connect("dbname=news")
except (Exception, psycopg2.DatabaseError) as error:
    print(error)

c = db.cursor()

# 1. extract top 3 popular articles
query1 = """
        SELECT title, num
        FROM articles_views
        ORDER BY num DESC
        LIMIT 3;
        """
c.execute(query1)
pop_article = c.fetchall()

# 2. rank authors by popularity
query2 = """
        SELECT authors.name, SUM(articles_views.num) AS sum
        FROM authors
        LEFT JOIN articles_views
        ON authors.id = articles_views.author
        GROUP BY authors.name
        ORDER BY sum DESC
        """
c.execute(query2)
rank_author = c.fetchall()

# 3. extract the date which has more than 1% error
query3 = """
        SELECT date, error_rate
        FROM (SELECT date,
            ROUND(SUM(CASE WHEN status = '404 NOT FOUND'
                THEN num ELSE 0 END) * 100 / SUM(num), 1) AS error_rate
            FROM log_date
            GROUP BY date) AS new_table
        WHERE error_rate > 1;
        """
c.execute(query3)
log_status = c.fetchall()

print("Report:")
print("1. The Most Popular Articles TOP 3")
for article in pop_article:
    print("  - {} : {} views").format(article[0], article[1])
print "2. The Most Popular Authors"
for author in rank_author:
    print("  - {} : {} views").format(author[0], author[1])
print "3. The date with errors more than 1%"
for log in log_status:
    print("  - {:%B %d, %Y} : {}% errors").format(log[0], log[1])

db.close()
