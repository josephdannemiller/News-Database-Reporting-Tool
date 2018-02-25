#! /usr/bin/env python2
import psycopg2
DBNAME = 'news'


def run_query(query):
    '''Connects to the database and runs the query that is provided
    as an argument. Returns the result of the query.'''
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close
    return results


def top_3_articles():
    '''Prints the top 3 articles by view count'''
    query = 'select * from viewcount limit 3'
    results = run_query(query)
    print('Most viewed articles of all time:')
    for title, views in results:
        print title + ' -- ' + str(views) + " views"
    print


def total_views():
    '''Prints the total views each author has achieved'''
    query = 'select * from views_by_author'
    results = run_query(query)
    print('Total views by author:')
    for name, views in results:
        print name + ' -- ' + str(views)
    print


def report_errors():
    '''Prints the date and error percentage if greater than 1 percent'''
    query = 'select * from connections'
    results = run_query(query)
    print('Days in which more than 1 percent of requests led to errors:')
    for date, good, bad in results:
        total_connections = good + bad
        error = ((bad*1.0)/total_connections)
        if error >= .01:
            print('{0:%B %d, %Y} -- {1:.2%} errors'.format(date, error))

if __name__ == '__main__':
    top_3_articles()
    total_views()
    report_errors()
