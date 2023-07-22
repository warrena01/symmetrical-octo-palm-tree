
/*
FIRST LOOK AT THE DATABASE 
primary keys: location, date
continent field contains null values, location becomes the continent/world for subaggregates in original dataset
*/
-- select COUNT(distinct(location))
select 
	location,date,new_cases,total_cases,new_deaths,total_deaths
from Portfolio_Project_1..covid_deaths

/*
DRILL DOWN: CONTINENTAL SCALE
Q1: How many total deaths are there per continent?
Q2: How many total infections are there been per continent?
*/
-- Q1
select continent, max(cast(total_deaths as int)) as 'total deaths'
from Portfolio_Project_1..covid_deaths
where continent is not null
group by continent 

-- Q2
select continent, max(total_cases) as 'total cases'
from Portfolio_Project_1..covid_deaths
where continent is not null
group by continent

/*
-- DRILL DOWN: INTERNATIONAL SCALE
Q1: How many total deaths are there per country?
Q2: How many total infections are there per country?
*/
-- Q1
select location, max(cast(total_deaths as int)) as 'total deaths'
from Portfolio_Project_1..covid_deaths
where continent is not null
group by location

-- Q2
select location, max(cast(total_cases as int)) as 'total cases'
from Portfolio_Project_1..covid_deaths
where continent is not null
group by location

/* 
-- DRILL DOWN: NATIONAL SCALE
Q1: How many deaths are there in country x? (where x is a user-defined variable)
Q2: How many infections have there been in the UK? 
Q3: When was the day with the highest number of infected people in the UK?
Q4: How many cases have there been as a percentage of the population for the UK over time?
Q5: What has been the death rate per total cases in the UK over time?
Q6: What has been the vaccination rate as a percentage of the population in the UK?

-- Use go before a statement to ensure it is seperated from any code you may have above it
*/

-- Q1
drop procedure if exists deaths_per_country
go
create procedure deaths_per_country
@location nvarchar(255) 
as 
	select location, max(cast(total_deaths as int)) as 'total deaths'
	from Portfolio_Project_1..covid_deaths
	where continent is not null
	and location = @location
	group by location

exec deaths_per_country
@location = 'United Kingdom'

-- Q2
select location, max(total_cases) as 'total cases'
from Portfolio_Project_1..covid_deaths
where continent is not null 
and location = 'United Kingdom'
group by location

-- Q3
go
with uk_hpr as (
select 
	location, max(positive_rate) as highest_positive_rate
from Portfolio_Project_1..covid_vaccinations
where continent is not null and location = 'United Kingdom'
group by location
)
select location, date, positive_rate
from Portfolio_Project_1..covid_vaccinations
where continent is not null
and positive_rate = (select highest_positive_rate from uk_hpr)
and location = 'United Kingdom'

-- Q4
select location, date, total_cases, population,
       round((total_cases/population)*100, 2) as infected_population_perc
from Portfolio_Project_1..covid_deaths
where location = 'United Kingdom'
and continent is not null

-- Q5
select location, date, cast(total_deaths as int), 
       total_cases, round((total_deaths/total_cases)*100, 2) as deaths_per_cases_perc
from Portfolio_Project_1..covid_deaths
where continent is not null
and location = 'United Kingdom'

-- Q6
select dea.location, dea.date, 
       cast(vac.total_vaccinations as int) as 'total_vaccinations', dea.population,
	   round((vac.total_vaccinations/dea.population)*100, 2) as 'perc_pop_vaccinated'
from Portfolio_Project_1..covid_deaths as dea
join Portfolio_Project_1..covid_vaccinations as vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.location = 'United Kingdom'

