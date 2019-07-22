/* VIEW1 ; change log.path into slug form */

CREATE VIEW path_to_slug AS
	SELECT REPLACE(path, '/article/','') AS path
	FROM log;

/* VIEW2 ; join view1 and table articles */

CREATE VIEW articles_views AS
	SELECT articles.author, articles.title, COUNT(path_to_slug.path) AS num 
	FROM articles LEFT JOIN path_to_slug 
	ON articles.slug = path_to_slug.path 
	GROUP BY articles.title, articles.slug, articles.author
	ORDER BY num;

/* VIEW3 ; log group by date & status */

CREATE VIEW log_date AS
	SELECT date(time) AS date, status, COUNT(*) as num 
	FROM log 
	GROUP BY date(time), status 
	ORDER BY date(time), status;