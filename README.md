# Database Reporting Tool Project
This project sets up a mock PostgreSQL database for a fictional news website. The psycopg2 library is used to query the database to provide the following information:
* The top 3 most viewed articles
* The total number of views each author has achieved
* Which days more than 1% of requests led to errors

## Installing the Virtual Machine & VirtualBox
1. Install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the _platform package_ for your operating system.
2. Install [Vagrant](https://www.vagrantup.com/downloads.html). Install the correct version for your operating system. (if vagrant is properly installed you will be able to run `vagrant --version` in your terminal to see the version number)
3. Download the [VM configuration](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip). Download and unzip the file - it will give you a directory called FSND-Virtual-Machine which may be located in your Downloads folder.
4. From your terminal navigate to the FSND-Virtual-Machine directory. Once there `cd vagrant` to navigate to the vagrant directory.
5. Start the Virtual Machine - Run the command `vagrant up` this will download the Linux OS and install it.
6. Once `vagrant up` has finished use the command `vagrant ssh` to log into your VM.
7. Once logged into your VM `cd /vagrant`. This directory is shared between your computer and the virtual machine.

## Setting up the news database
#### If you are using Vagrant and followed the above steps:
* The news database is already set up for you but the **[data still needs to be downloaded](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).** Put the newsdata.sql file into your vagrant directory (the one shared with your VM).
* To load the data into your database use the following command: `psql -d news -f newsdata.sql`

#### If you are not using Vagrant
* Create the news database with the following two commands:
- `psql`
- `create database news;`
- **[Download the data for the news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).** Put the newsdata.sql file into the proper directory
- To load the data into your database use the following command: `psql -d news -f newsdata.sql`

## Running the program
To run the program simply execute the python file reporting_tool.py from the command line.  Be sure to create the views listed below or the program will not work.

`$ python reporting_tool.py`

## Required Views
The following views are required to be added to the news database for the program to work properly.<br>
**Some views rely on other views so they must be created in this order:**
```sql
create view viewcount as select title, count(*) as num
  from articles, log
  where ('/article/' || articles.slug) = log.path
  group by articles.title
  order by num desc;

create view name_title as select name, title
  from authors, articles
  where articles.author = authors.id;

create view name_title_views as select name, viewcount.title, num as views
  from name_title, viewcount
  where viewcount.title = name_title.title;

create view views_by_author as select name, sum(views) as total_views
  from name_title_views
  group by name
  order by total_views desc;

create view good_connections as select time::date
  from log
  where status = '200 OK';

create view good_connections_by_date as select time, count(*) as num
  from good_connections
  group by time;

create view bad_connections as select time::date
  from log
  where status != '200 OK';

create view bad_connections_by_date as select time, count(*) as num
  from bad_connections
  group by time;

create view connections as select good_connections_by_date.time,
  good_connections_by_date.num as good,
  bad_connections_by_date.num as bad
  from good_connections_by_date, bad_connections_by_date
  where good_connections_by_date.time = bad_connections_by_date.time;
```
