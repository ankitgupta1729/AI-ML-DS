1. Create a Connection to the database:

A. Open DBeaver
B. Click on New Connection Wizard button on the toolbar
C. Select your databses. DBeaver supports lots of databases. Here we will connect to a Postgres database.

DBeaver is just a client; it cannot work unless a PostgreSQL server is installed and listening on port 5432.

So, first install postgresql then make connection and test connection and then finish it.

2. Now, to write SQL queries, click on sql editor button on the top.
Write the query and run it.

create table mytable (
somevalue varchar(20)
);

insert into mytable(somevalue) values ('Hello');

select * from mytable; 

3. we can create multiple tabs for writing sql script from top sql dropdown menu.

