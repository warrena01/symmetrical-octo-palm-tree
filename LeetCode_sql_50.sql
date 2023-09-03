
-- SELECT 

            -- Question 1:
            select product_id
            from Products
            where low_fats = 'y' and recyclable = 'y'
            
            -- Question 2:
            select name
            from customer
            where referee_id != 2 or 
                  referee_id is null
            
            -- Question 3:
            select name, population, area
            from World
            where area >= 3000000 
                  or population >= 25000000 
            
            -- Question 4:
            select distinct(author_id) as id
            from Views
            where author_id = viewer_id
            order by author_id asc
            
            -- Question 5:
            select tweet_id
            from Tweets
            where len(content) > 15

-- BASIC JOINS

            -- Question 6:
            select u.unique_id, e.name
            from Employees e
            left join EmployeeUNI u
            on e.id = u.id
            
            -- Question 7:
            select p.product_name, s.year, s.price
            from  product p
            inner join sales s
            on p.product_id = s.product_id
            
            -- Question 8:
            select v.customer_id, count(v.visit_id) as count_no_trans
            from visits v
            left join transactions t
              on v.visit_id = t.visit_id
            where t.amount is null
            group by v.customer_id
            
            -- Question 9:
            select w1.id
            from Weather w1
            join Weather w2 on
            --            yesterday         today       = today - yesteday
            datediff(day, w2.recordDate, w1.recordDate) = 1 
            and w1.temperature > w2.temperature
            
            -- Question 10:
            select a1.machine_id, 
                   round(avg(a2.timestamp - a1.timestamp), 3) as processing_time
            from activity a1
            join activity a2 on
                a1.activity_type = 'start' and a2.activity_type = 'end'
                and a1.machine_id = a2.machine_id and a1.process_id = a2.process_id
            group by a1.machine_id
            
            -- Question 11:
            select e.name, b.bonus
            from Employee e
            left join Bonus b on
              e.empID = b.empID
            where bonus < 1000 or bonus is null
            
            -- Question 12:
            select s.student_id, s.student_name, sj.subject_name, 
                   count(e.subject_name) as attended_exams
            from students as s
            cross join subjects as sj -- gets a table of every student and every subject
            left join examinations as e on -- adds in the examinations data, where:
                s.student_id = e.student_id and -- student_id is the same
                sj.subject_name = e.subject_name -- and where the subject is the same
            group by s.student_id, s.student_name, sj.subject_name
            order by s.student_id, student_name
            
            -- Question 13:
            with find_managerid as (
            select managerid
            from employee
            group by managerid
            having count(managerid) >= 5
            )
            select name
            from employee e
            inner join find_managerid f
            on e.id = f.managerid
            
            -- Question 14: 
            select s.user_id,
                    round(
                    avg(case 
                      when c.action = 'confirmed' then 1.0
                      else 0
                    end),
                     2) as confirmation_rate
            from signups s
            left join confirmations c on
              s.user_id = c.user_id
            group by s.user_id

-- BASIC AGGREGATE FUNCTIONS
            
            -- Question 15:
            select id, movie, description, rating
            from Cinema 
            where id % 2 <> 0 and -- <> 0 for odds, = 0 for evens.
                  description != 'boring'
            order by rating desc
            
            -- Question 16:
            select p.product_id, 
                   round(cast(sum(p.price * us.units) as decimal) 
                        /cast(sum(us.units) as decimal), 2) as average_price
            from prices as p
            join unitssold as us
              on p.product_id = us.product_id 
              and us.purchase_date >= p.start_date 
              and us.purchase_date <= p.end_Date
            group by p.product_id 
            
            -- Question 17:
            select p.project_id,
                   round(avg(cast(e.experience_years as decimal)), 2) as average_years
            from project p
            join employee e on
              p.employee_id = e.employee_id
            group by p.project_id
            
            -- Question 18:
            select p.project_id, 
                   round((avg(cast(e.experience_years as decimal))), 2) as average_years
            from project as p
            left join employee as e on
              p.employee_id = e.employee_id
            group by p.project_id
            
            -- Question 19:
            select  r.contest_id, 
                    round((count(u.user_id*1.0)/
                    (select count(user_id)*1.0 from users)
                    *100), 2) as percentage
            from register r
            join users u on 
                r.user_id = u.user_id
            group by r.contest_id
            order by percentage desc, contest_id asc
            
            -- Question 20:
            select    format(trans_date, 'yyyy-MM') as 'month',
                      country,
                      count(trans_date) as trans_count, 
                      count(iif(state='approved', 1, null)) as approved_count,
                      sum(amount) as trans_total_amount,
                      sum(iif(state='approved', amount, 0)) as approved_total_amount
            from transactions
            group by format(trans_date, 'yyyy-MM'), country

            -- Question 21:
            with cte as (
              select *,
              case 
                when order_date = customer_pref_delivery_Date then 1.0
                else 0.0
              end as order_type,
              first_value(order_date) over (partition by customer_id order by order_date) as first_order
              from delivery
            ),
            -- this refines the table to date that we need
            cte_2 as (
              select * 
              from cte
              where first_order = order_date
            )
            select round(sum(order_type) * 100 / count(customer_id)*1.0, 2) as immediate_percentage
            from cte_2

            -- Question 22:
            with first_date as (
              select player_id, min(event_date) as first_date
              from activity
              group by player_id
            ),
            played_next_day as (
              select cast(count(a.player_id) as decimal) as next_day_count
              from activity a
              join first_date fd on
                a.player_id = fd.player_id
                and datediff(day, fd.first_date, a.event_date) = 1
            ),
            total_players as (
              select cast(count(distinct(player_id)) as decimal) as total_players_count
              from activity
            )
            select round(next_day_count / total_players_count, 2) as fraction
            from played_next_day, total_players

-- SORTING AND GROUPING 
            
            -- Question 23:
            select  query_name,
                    round(avg(rating*1.0/position*1.0), 2) as quality,
                    round((sum(case when rating < 3 then 1 else 0 end)*1.0 / count(*)*1.0 * 100), 2) as poor_query_percentage
            from queries
            group by query_name
            
            -- Question 24:
            select activity_date as day, 
            count(distinct(user_id)) as active_users
            from activity 
            where datediff(day, activity_date, '2019-07-27') between 0 and 29
            group by activity_date
            
            -- QUESTION 25
            select product_id, year as first_year, quantity, price
            from (
                  select *,
                  rank() over (partition by product_id order by year asc) as ranked_years
                  from sales
                  ) 
                  as get_years_ranked
            where ranked_years = 1
                  
            -- Question 26:
            select class
            from courses 
            group by class
            having count(student) >= 5
            
            -- Question 27:
            select user_id, 
                   count(distinct(follower_id)) as followers_count
            from followers
            group by user_id
            
            -- Question 28:
            with unique_num as (
            select num
            from mynumbers
            group by num
            having count(num) < 2
            )
            select 
            case
            when (select count(*) from unique_num) < 1 then null
            when (select count(*) from unique_num) >= 1 then max(num)
            end as num
            from unique_num

            -- Question 29:
            with cte as (
            select count(product_key) as n_of_products
            from product)
            select customer_id
            from customer 
            group by customer_id
            having count(distinct(product_key)) = (select * from cte)

-- ADVANCED SELECT AND JOINS

            -- Question 30:
            select  e2.employee_id, e2.name, 
                    count(e1.employee_id) as reports_count,
                    round((avg(e1.age*1.0)), 0) as average_age
            from employees e1
            join employees e2 on
                e1.reports_to = e2.employee_id
            group by e2.employee_id, e2.name
            order by e2.employee_id asc
            
            -- Question 31:
            with cte as (
              select employee_id, department_id, primary_flag,
              count(department_id) over (partition by employee_id) as department_count
              from employee
            )
            select employee_id, department_id
            from cte
            where primary_flag = 'Y' or department_count = 1
            
            -- Question 32:
            /* Triangle Inequality Theorem: the sum of two side lengths of a 
            triangle is always greater than the third side */
            select *, 
                  iif(x+y > z and x+z > y and y+z > x, 'Yes', 'No') as triangle
            from triangle
            
            -- Question 33:
            select distinct(l1.num) as consecutivenums
            from
            (logs l1
            join logs l2 on
              l1.id = l2.id-1 and
              l1.num = l2.num)
            join logs l3 on
              l2.id = l3.id-1 and
              l1.num = l3.num

            -- Question 34:
            with get_cum_weight as (
                   select person_id, person_name, weight, turn, 
                          sum(weight) over (order by turn) as 'total_weight'
                   from queue 
                   group by person_id, person_name, weight, turn),
            included_people as (
                   select *,
                   case
                     when total_weight <= 1000 then 'Y'
                     else 'N'
                   end as fits_or_no
                   from get_cum_weight),
            rank_ppl as (
                   select *,
                   rank() over (order by total_weight desc) as rank_ppl
                   from included_people
                   where fits_or_no = 'Y'
            )
            select person_name
            from rank_ppl
            where rank_ppl = 1

            -- Question 35: 
            select 'Low Salary' as category, 
            sum(if(income < 20000, 1, 0)) as accounts_count
            from accounts
            
            union all
            
            select 'Average Salary' as category, 
            sum(if(income between 20000 and 50000, 1, 0)) as accounts_count
            from accounts
            
            union all
            
            select 'High Salary' as category, 
            sum(if(income > 50000, 1, 0)) as accounts_count
            from accounts


            
            

 