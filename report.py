import psycopg2, datetime

VIEW1 = "path_to_slug"
VIEW2 = "articles_views"
VIEW3 = "log_date"

db = psycopg2.connect("dbname=news")
c = db.cursor()

# make view1 ; change log.path into slug form
query_view1 = "create view " + VIEW1 + " as select path from log;"
c.execute(query_view1)
query_view1_1 = "update " + VIEW1 + " set path = replace(path,'/article/','');"
c.execute(query_view1_1)

# make view2 ; join view1 and table articles
query_view2 = "create view " + VIEW2 + " as select articles.author, articles.title, count(" + VIEW1 + ".path) as num from articles left join " + VIEW1 + " on articles.slug = " + VIEW1 + ".path group by articles.title, articles.slug, articles.author order by num;"
c.execute(query_view2)

# 1. extract top 3 popular articles
query1 = "select title, num from " + VIEW2 + " order by num desc limit 3;"
c.execute(query1)
pop_article = c.fetchall()

# 2. rank authors by popularity
query2 = "select authors.name, sum(" + VIEW2 + ".num) as sum from authors left join " + VIEW2 + " on authors.id = " + VIEW2 + ".author group by authors.name order by sum desc"
c.execute(query2)
rank_author = c.fetchall()

# make view3 ; log group by date & status
query_view3 = "create view " + VIEW3 + " as select date(time) as date, status, count(*) as num from log group by date(time), status order by date(time), status;"
c.execute(query_view3)

# 3. extract the date which has more than 1% error
query3 = "select date, sum(case when status = '200 OK' then num else 0 end) ok, sum(case when status = '404 NOT FOUND' then num else 0 end) error from " + VIEW3 + " group by date;"
c.execute(query3)
log_status = c.fetchall()

print "Report:"
print "1. The Most Popular Articles TOP 3"
for article in pop_article:
    print "  - ", article[0], " : ", article[1], "views"
print "2. The Most Popular Authors"
for author in rank_author:
    print "  - ", author[0], " : ", author[1], "views"
print "3. The date with errors more than 1%"
for log in log_status:
    rate = log[2]/log[1]*100
    if rate > 1:
        print "  - ", log[0].strftime("%B %d, %Y"), " : {}%".format(round(rate,1)), "errors"


db.close()