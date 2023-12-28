# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import psycopg2
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import sys 



def connect_to_db():
    connection = psycopg2.connect(user='postgres', password='Prashik@786',
                                  host = 'localhost',
                                  port=5432,
                                  database = 'employeedb')
    
    return connection

connection = connect_to_db()
df = pd.read_sql_query("""select * from employees.salary""",connection)
print(sys.getsizeof(df))    

connection = connect_to_db()
df2 = pd.read_sql_query("""select d.dept_name as department,avg(s.amount) as salary from employees.department as d
join employees.department_employee as de 
on d.id = de.department_id 
join employees.salary as s
on de.employee_id = s.employee_id
where extract(year from s.to_date)= 9999
group by d.dept_name""",connection)
print(df2)


sns.barplot(data=df2,x='department',y='salary')
plt.xlabel('department')
plt.ylabel('salary')
plt.title('Department wise average salary')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


connection = connect_to_db()
df3 = pd.read_sql_query("""select t.title as title, avg(s.amount) as avg_salary from employees.title as t
join employees.salary as s
on t.employee_id = s.employee_id 
group by title""",connection)
print(df3)

sns.barplot(data=df3,x='title',y='avg_salary')
plt.xlabel('title')
plt.ylabel('salary')
plt.title('title wise average salary')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


query = """select title, sum(amount) as amount from employees.title 
            inner join employees.salary 
            on employees.title.employee_id = employees.salary.employee_id
            group by title;"""

connection = connect_to_db()
df4 = pd.read_sql_query(query,connection)
connection.close()  

plt.pie(df4['amount'], labels=df4['title'], autopct='%1.1f%%')
plt.title("Title-wise Salary Distribution")
plt.axis('equal')  
plt.tight_layout()
plt.show()



query = """select dept_name,sum(s.amount) as salary from employees.department as d
           inner join employees.department_employee as de
           on d.id = de.department_id 
           inner join employees.salary as s 
           on de.employee_id = s.employee_id
           group by dept_name;"""

connection = connect_to_db()
df5 = pd.read_sql_query(query,connection)
connection.close()  

plt.pie(df5['salary'], labels=df5['dept_name'], autopct='%1.1f%%')
plt.title("Department-wise Salary Distribution")
plt.axis('equal')  
plt.tight_layout()
plt.show()


connection = connect_to_db()
df6 = pd.read_sql_query("""select dept_name,count(dm.employee_id) as count from employees.department_manager as dm 
join employees.department d 
on d.id = dm.department_id 
where extract(year from to_date) = 9999
group by dept_name""",connection)
print(df6)

sns.barplot(data=df6,x='dept_name',y='count')
plt.xlabel('dept_name')
plt.ylabel('count')
plt.title('active manager department wise')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()



connection = connect_to_db()
df7 = pd.read_sql_query("""select d.dept_name as department,t.title as title,count(de.employee_id)  as count from employees.department as d
join employees.department_employee as de
on d.id = de.department_id
join employees.title as t
on de.employee_id = t.employee_id
group  by d.dept_name,t.title""",connection)
print(df7)

sns.barplot(data=df7,x='department',y='count',hue = 'title')
plt.xlabel('department')
plt.ylabel('count')
plt.title('Distribution of Title- Department wise')
plt.legend(title='Titles', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


connection = connect_to_db()
df8 = pd.read_sql_query("""select d.dept_name as department,t.title as title from employees.department as d
join employees.department_employee as de
on d.id = de.department_id
join employees.title as t
on de.employee_id = t.employee_id""",connection)
print(df8)


sns.countplot(data=df8,x='title',hue = 'department')
plt.xlabel('Titles')
plt.ylabel('count')
plt.xticks(rotation = 90)
plt.title('Distribution of  Department title-wise')
plt.legend(title='Titles', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


connection = connect_to_db()
df9 = pd.read_sql_query("""select dept_name,sum(s.amount) as salary from employees.department_manager as dm 
join employees.department d 
on d.id = dm.department_id 
join employees.salary s 
on dm.employee_id = s.employee_id
where extract(year from dm.to_date) = 9999
group by dept_name
order by salary desc""",connection)
print(df9)

sns.barplot(data=df9,x='dept_name',y='salary')
plt.xlabel('dept_name')
plt.ylabel('salary')
plt.title('active manager salary')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


connection = connect_to_db()
df10 = pd.read_sql_query("""select t.title from employees.title as t
inner join employees.department_manager as dm
on t.employee_id = dm.employee_id
where extract(year from dm.to_date) = 9999
limit 5""",connection)
print(df10)



query = """select dept_name, sum(s.amount) as salary from employees.department as d 
join employees.department_manager as  dm
on d.id = dm.department_id 
join employees.salary as s 
on  dm.employee_id = s.employee_id 
where extract(year from  dm.to_date) = 9999 and extract(year from s.to_date) = 9999
group by dept_name"""


connection = connect_to_db()
df11 = pd.read_sql_query(query,connection)
print(df11)
connection.close()

sns.barplot(data=df11,x='dept_name',y='salary')
plt.xlabel('dept_name')
plt.ylabel('salary')
plt.title('Salaries of Manager across Department')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


query = """select id, amount,
                EXTRACT(YEAR FROM employees.salary.to_date) AS year
                from  employees.employee 
                inner join employees.salary on
                employees.employee.id = employees.salary.employee_id
                where EXTRACT(year FROM employees.salary.to_date) != 9999
                    """

connection = connect_to_db()
df12 = pd.read_sql_query(query,connection)
connection.close() 

sns.lineplot(data = df12, x = "year",y = "amount")
plt.xlabel("Year")
plt.ylabel("salary")
plt.title("salaries of employees")
plt.xticks(rotation=90)  
plt.tight_layout()  
plt.show()



connection = connect_to_db()
df13 = pd.read_sql_query("""select t.title as title, avg(extract(year from t.to_date) - extract(year from e.hire_date)) as avg_year
from employees.title as t 
join employees.employee as e
on t.employee_id = e.id 
where date_part('year',t.to_date) != 9999
group by t.title""",connection)
print(df13)

sns.barplot(data=df13,x='title',y='avg_year')
plt.xlabel('title')
plt.ylabel('avg_year')
plt.title('avg_year before leaving')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


connection = connect_to_db()
df14 = pd.read_sql_query("""select d.dept_name as department, avg(extract(year from de.to_date) - extract(year from e.hire_date)) as avg_year
from employees.department_employee as de 
join employees.employee as e
on de.employee_id = e.id 
join employees.department as d 
on d.id = de.department_id
where date_part('year',de.to_date) != 9999
group by d.dept_name""",connection)
print(df14)

sns.barplot(data=df14,x='department',y='avg_year')
plt.xlabel('department')
plt.ylabel('avg_year')
plt.title('avg_year before leaving Department wise')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


connection = connect_to_db()
df15 = pd.read_sql_query("""SELECT
    d.dept_name AS department,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (s.amount / EXTRACT(YEAR FROM s.to_date) - EXTRACT(YEAR FROM s.from_date))) AS median_increment
FROM
    employees.department d
JOIN
    employees.department_manager dm ON d.id = dm.department_id
JOIN
    employees.salary s ON dm.employee_id = s.employee_id
WHERE
    (EXTRACT(YEAR FROM s.to_date) - EXTRACT(YEAR FROM s.from_date)) > 0
GROUP BY
    d.dept_name;""",connection)
print(df15)

sns.barplot(data=df15,x='department',y='median_increment')
plt.xlabel('department')
plt.ylabel('median_increment')
plt.title('Median annual salary increment department wise')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()



