/*	
	THIS WILL SHOW A COMPLETE WORKFLOW OF SKILLS I HAVE LEARNT FROM SQL COURSES, INCLUDING:
	CREATING TABLES, ADDING RECORDS, DELETING RECORDS, UPDATING RECORDS
	WHERE STATEMENTS
	GROUP BY STATEMENTS
	JOINS
	CASE STATEMENTS
	HAVING CLAUSE
	CTEs
	STRING FUNCTIONS
	NUMERIC FUNCTIONS
	STORED PROCEDURES
	WINDOW FUNCTIONS
	
	THIS WILL KEEP THINGS SIMPLE SO THAT ALL EXAMPLES ARE EASY TO FLOW
	THIS INCLUDES DATA I CREATED ABOUT THE NETFLIX SERIES 'NARCOS'
*/

--- Create Database
drop database if exists narcos_data
create database narcos_data

--- Create tables
drop table if exists narcos_data..protagonists --- this deletes any table with the same name if there is one
create table narcos_data..protagonists ( --- create table command, followed by database_name..table_name, in this case 'narcos_data..protagonists'
	id int not null, --- name of the column, in this case 'id', and the data type it will receive and say if this column can be null or no
	first_name varchar(100),
	surname varchar(100),
	nationality varchar(100),
	country_of_residence varchar(100),
	city varchar(100),
	birth_date date,
	primary key (id) --- set the primary key for the table
)

drop table if exists narcos_data..arrests_and_deaths
create table narcos_data..arrests_and_deaths ( 
	id int not null, 
	living_status varchar(100),
	previous_convictions varchar(100),
	death_date date,
	primary key (id)
)

drop table if exists narcos_data..salaries
create table narcos_data..salaries ( 
	id int not null, 
	first_name varchar(100),
	surname varchar(100),
	job varchar(200),
	organisation varchar(100),
	estimated_salary_$ int,
	primary key (id)
)

--- Input Data

insert into narcos_data..protagonists (id, first_name, surname, nationality, country_of_residence, city, birth_date)
			--- [database]..[table_name] (column1, column2, column...)
values 
--- (the value corresponding to the index placer for the columns as listed above), 
--- this is repeated multiple times with each added record seperated by a comma
(1, 'Pablo', 'Escobar', 'Colombian', 'Colombia', 'Medellin', '1949-12-01'),
(2, 'Gustavo', 'Gaviria', 'Colombian', 'Colombia', 'Medellin', '1949-12-12'),
(3, 'Jorge', 'Ochoa', 'Colombian', 'Colombia', 'Medellin', '1949-09-30'),
(4, 'Fabio', 'Ochoa', 'Colombian', 'Colombia', 'Medellin', '1947-09-02'),
(5, 'Gonzales', 'Rodriguez Gacha', 'Colombian', 'Colombia', 'Medellin', '1947-05-14'),
(6, 'Gilberto', 'Rodriguez Orejuela', 'Colombian', 'Colombia', 'Cali', '1939-01-30'),
(7, 'Miguel', 'Rodriguez Orejuela', 'Colombian', 'Colombia', 'Cali', '1943-08-15'),
(8, 'Pacho', 'Herrera', 'Colombian', 'Colombia', 'Cali', '1951-1-1'),
(9, 'Steve', 'Murphy', 'American', 'Colombia', 'Medellin', '1957-05-18'),
(10, 'Javier', 'Pena', 'American', 'Colombia', 'Medellin', '1948-07-12'),
(11, 'Jose', 'Luis Herrera', 'Colombian', 'Colombia', 'Medellin', null),
(12, 'Fernando', 'Del Valle', 'Colombian', 'Colombia', 'Medellin', null),
(13, 'Dandeny', 'Dandeny', 'Colombian', 'Colombia', 'Medellin', '1953-11-11'),
(14, 'Jhon Jairo', 'Velasquez Vasquez', 'Colombian', 'Colombia', 'Medellin', '1962-02-15')

insert into narcos_data..arrests_and_deaths (id, living_status, previous_convictions, death_date)
values
(1, 'deceased', 'arrested', '1993-12-02'),
(2, 'deceased', null, '1990-08-12'),
(3, 'alive', 'arrested', null),
(4, 'alive', 'arrested', null),
(5, 'deceased', null, '1989-12-15'),
(6, 'alive', 'arrested', null),
(7, 'alive', 'arrested', null),
(8, 'deceased', null, '1998-01-01'),
(9, 'alive', null, null),
(10, 'alive', null, null),
(11, 'alive', null, null),
(12, 'alive', null, null),
(13, 'deceased', null, '1993-06-06'),
(14, 'alive', 'arrested', null)

insert into narcos_data..salaries(id, first_name, surname, job, organisation, estimated_salary_$)
values
(1, 'Pablo', 'Escobar', 'Head of Medelling Cartel', 'Medellin Cartel', 200000000),
(2, 'Gustavo', 'Gaviria', 'High Ranking Medellin Cartel Member', 'Medellin Cartel', 9000000),
(3, 'Jorge', 'Ochoa', 'High Ranking Medellin Cartel Member', 'Medellin Cartel', 5000000),
(4, 'Fabio', 'Ochoa',  'High Ranking Medellin Cartel Member', 'Medellin Cartel', 6000000),
(5, 'Gonzales', 'Rodriguez Gacha', 'High Ranking Medellin Cartel Member', 'Medellin Cartel', 4000000),
(6, 'Gilberto', 'Rodriguez Orejuela', 'Head of Cali Cartel', 'Cali Cartel', 2000000),
(7, 'Miguel', 'Rodriguez Orejuela', 'High Ranking Cali Cartel Member', 'Cali Cartel', 1000000),
(8, 'Pacho', 'Herrera', 'High Ranking Cali Cartel Member', 'Cali Cartel', 900000),
(9, 'Steve', 'Murphy', 'DEA Agent', 'Cali Cartel', 35000),
(10, 'Javier', 'Pena', 'DEA Agent', 'US Government', 40000),
(11, 'Jose', 'Luis Herrera','Security Officer', 'Colombian National Police', 400),
(12, 'Fernando', 'Del Valle','Accountant', 'Medellin Cartel', 100000),
(13, 'Dandeny', 'Dandeny','Sicario', 'Medellin Cartel', 300000),
(14, 'Jhon Jairo', 'Velasquez Vasquez','Sicario', 'Medellin Cartel', 300000),
(15, 'Joaquin', 'Guzman', 'Leader', 'Sinaloa Cartel', 450000000)

--- Now that all data is in place, take an initial look at the data

select *
from narcos_data..arrests_and_deaths

select *
from narcos_data..salaries

select *
from narcos_data..protagonists

/* Upon analysis, I find that there are some errors in the data
(1) Steve Murphy's organisation is set to the Cali Cartel
	To resolve this we need to update this record 
(2) There is a record for someone in teh Sinaloa Cartel which shouldnt be in this dataset
	To resolve this, we need to delete this record 
*/

--- Updating and Deleting records

update narcos_data..salaries --- choose which table to update
set organisation = 'US Government' -- chose which column to update and which value to change it to
where id = 9 -- define which records to change

delete from narcos_data..salaries --- choose which table to delete from
where id = 15

--- Group By, lets have a look at the total amounts earned per organisation

select organisation, sum(estimated_salary_$) as total_salary -- anything not aggregated must be in grouped by
from narcos_data..salaries
group by organisation

--- Where, lets have a look at the total amount earned just for the Cali Cartel

select organisation, sum(estimated_salary_$) as total_salary --- anything not aggregated must be in grouped by
from narcos_data..salaries
where organisation = 'Cali Cartel' --- where statements come before group by statementsm we use the = sign for an exact answer
group by organisation

--- Where, lets have a look at the total amount earned for the Cali Cartel or Medellin Cartel

select organisation, sum(estimated_salary_$) as total_salary -- anything not aggregated must be in grouped by
from narcos_data..salaries
where organisation = 'Cali Cartel' 
or organisation = 'US Government' -- we  can use the 'or' to allow for multiple choices in the same column
group by organisation

-- Where, lets have a look for people whose surnames start with a R, or whose first names end in o, or if they have an a in their name, and are from colombia

select id, first_name, surname, nationality
from narcos_data..protagonists
where (first_name like 'r%' --- we can use a like operator to show we dont know the whole name, and a % to show that after the r the character doesnt matter
or surname like '%o' --- same as before but the % goes before to show it doesnt matter what was before but the input must end in o
or first_name like '%a%') --- same but with an a anywhere in the first_name 
and nationality = 'Colombian' --- and operator to allow any of the first three parameters, which is why brackets were included, AND their nationality is colombian


--- Joins, lets have a look at the nationality of people arrested in our dataset, their jobs and if they have been arrested

select a_d.id, prot.first_name, prot.surname, prot.nationality, sal.job, a_d.previous_convictions --- select from which table each column will come from
from narcos_data..arrests_and_deaths a_d --- collect data from our first table as normal and give it an alias
inner join narcos_data..protagonists prot --- choose which kind of join we want and define to which table, giving it an alias
on a_d.id = prot.id --- define on which key the data can be connected
inner join narcos_data..salaries sal
on a_d.id = sal.id



--- Case Statements, lets define a column showing us the good and bad guys based upon a persons organisation

select first_name, surname, organisation,
case 
	when organisation = 'US Government' then 'Good Guys'
	when organisation = 'Colombian National Police' then 'Good Guys'
	else 'Bad Guys'
end 'good_or_bad'
from narcos_data..salaries

--- Having Statements, lets look at the organisations with a total income > 1000

select organisation, sum(estimated_salary_$) as total_salary --- anything not aggregated must be in grouped by
from narcos_data..salaries
group by organisation
having sum(estimated_salary_$) > 100000 --- this is like the where statement, but is the syntax for when we filter based on aggregate functions

--- CTEs, these allow us to reference an answer instead of making a nested query, so that our code is more readable, lets find the person still alive who had the highest salary

with 
still_alive as ( --- open our query using with and give it a name
	select id, living_status
	from narcos_data..arrests_and_deaths
	where living_status = 'Alive' --- this finds all the people who are still alive
	),
max_salary as ( --- for a second query it isnt necessary to use a with statement.
	select max(estimated_salary_$) as top_sal --- this finds the top salary
	from narcos_data..salaries
	where id in (select id from still_alive) --- filters data to just those alive as per previous query
	)
select prot.first_name, prot.surname
from narcos_data..protagonists as prot
inner join narcos_data..salaries as sal
on prot.id = sal.id
where sal.estimated_salary_$ = (select top_sal from max_salary) --- oen expression that summarises all the CTE above

--- String Functions 

select first_name, surname,
	   concat(first_name, ' ', surname) as full_name, --- the concat function joins two columns strings together with a delimeter as defined in the middle
	   upper(first_name) as all_caps, --- turns all letters into upper case
	   lower(surname) as all_lower, --- turns all letters into lower case
	   ltrim(first_name) as remove_space_to_left, --- removes all space ot the left for the this column (if any)
	   rtrim(first_name) as remove_space_to_right --- removes all space ot the right for the this column (if any)
from narcos_data..protagonists


--- Stored Procedures, these remove the need to continually rewrite the same query

go --- this fixes the error 'must be the only statement in the batch'
create procedure name_of_procedure as --- use this syntax to create the procedure (normally they would be more complex to make it worth creating a procedure)
select *
from narcos_data..protagonists

exec name_of_procedure --- now any time you want to run this query, you just need to run this single line of code

--- Window Functions, these are used to give us ranking of different kinds within our data

select concat(first_name, ' ', surname) as name, city,
   --- window function to show a new column with the value as the first value in the each partition (ordered by the orodered by)
	   first_value(first_name) over (partition by city order by surname) as first_value_in_field --- the order by can be anything
from narcos_data..protagonists
---
select concat(first_name, ' ', surname) as name, organisation, 
       --- window function to show a new column with the value as the average salary for the organisation the person is in
	   avg(estimated_salary_$) over (partition by organisation) as organisation_avg_salary
from narcos_data..salaries 
---
select concat(first_name, ' ', surname) as name, organisation, estimated_salary_$,
       --- window function to show a new column showing the salary in percentiles as percentiles based on number of items
       ntile(7) over (order by estimated_salary_$ desc) as organisation_avg_salary
from narcos_data..salaries 
---
select concat(first_name, ' ', surname) as name, organisation, estimated_salary_$,
   --- window function to show a new column with a rank of all values in the dataset
	   rank() over (order by estimated_salary_$) as rank_all_data
   --- rank() over (order by values_that_define_ranking)
from narcos_data..salaries
---
select concat(first_name, ' ', surname) as name, organisation, estimated_salary_$,
   --- window function to show a new column with the value as the first value in the each partition (ordered by the orodered by)
	   rank() over (partition by organisation order by estimated_salary_$)  as rank_per_organisation
   --- rank() over (partition by subgroups_to_be_ranked order by values_that_define_ranking)
from narcos_data..salaries
---
select concat(first_name, ' ', surname) as name, organisation, estimated_salary_$,
   --- window function to show a new column with the value as the value of the person one row below
	   lead(estimated_salary_$, 1) over (partition by organisation order by estimated_salary_$ asc)  as salary_of_next_highest_person
   --- lead(field, number of places below) over (partition by subgroups_to_be_ranked order by values_that_define_ranking)
from narcos_data..salaries
---
select concat(first_name, ' ', surname) as name, organisation, estimated_salary_$,
   --- window function to show a new column with the value as the value of the person two row above
	   lag(estimated_salary_$, 2) over (partition by organisation order by estimated_salary_$ asc)  as salary_of_person_2_below
   --- lag(field, number of places above) over (partition by subgroups_to_be_ranked order by values_that_define_ranking)
from narcos_data..salaries

