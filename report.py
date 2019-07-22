#! /usr/bin/env python3

import psycopg2
import datetime


def db_connect():
    try:
        db = psycopg2.connect("dbname=news")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return db.cursor()


def execute_query(q):
    c = db_connect()
    c.execute(q)
    return c.fetchall()


# 1. extract top 3 popular articles
def print_top_articles():
    query = """
            SELECT title, num
            FROM articles_views
            ORDER BY num DESC
            LIMIT 3;
            """
    results = execute_query(query)
    print("Report:")
    print("1. The Most Popular Articles TOP 3")
    for article in results:
        print("  - {} : {} views").format(article[0], article[1])


# 2. rank authors by popularity
def print_top_authors():
    query = """
            SELECT authors.name, SUM(articles_views.num) AS sum
            FROM authors
            LEFT JOIN articles_views
            ON authors.id = articles_views.author
            GROUP BY authors.name
            ORDER BY sum DESC
            """
    results = execute_query(query)
    print("2. The Most Popular Authors")
    for author in results:
        print("  - {} : {} views").format(author[0], author[1])


# 3. extract the date which has more than 1% error
def print_errors_over_one():
    query = """
            SELECT date, error_rate
            FROM (SELECT date,
                ROUND(SUM(CASE WHEN status = '404 NOT FOUND'
                    THEN num ELSE 0 END) * 100 / SUM(num), 1) AS error_rate
                FROM log_date
                GROUP BY date) AS new_table
            WHERE error_rate > 1;
            """
    results = execute_query(query)
    print("3. The date with errors more than 1%")
    for log in results:
        print("  - {:%B %d, %Y} : {}% errors").format(log[0], log[1])


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_errors_over_one()
