//load specialisations and job titles
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/job_titles.csv' AS row
MERGE (s: Specialisation {name: row.specialisation})
MERGE (j: Job_title {name: row.job_title})
RETURN *

//link job_titles with specialisation
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/job_titles.csv' AS row
MATCH (spec: Specialisation {name: row.specialisation})
MATCH (j: Job_title {name: row.job_title})
MERGE (j)-[:IN_SPECIALISATION]->(spec)
RETURN *

//load skills
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/skills.csv' AS row
MERGE (s: Skill {name: row.skill})
RETURN s

//link skills with specialisation
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/skills.csv' AS row
MATCH (s: Skill {name: row.skill})
MATCH (sp: Specialisation {name: row.specialisation})
MERGE (s)-[:IN_SPECIALISATION]->(sp)
RETURN *


//load employees
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/employees.csv' AS row
MERGE (e: Employee {
employee_id: toInteger(row.id),
surname: row.surname,
name: row.name,
gender: row.gender,
birthday: date(row.birthday),
phone: row.phone,
email: row.email,
hire_date: date(row.hire_date),
performance_score: toInteger(row.performance_score)})
RETURN e;

//add job_titles
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/employees.csv' AS row
MATCH (e: Employee {employee_id: toInteger(row.id)})
MATCH (j: Job_title {name: row.job_title})
MERGE (e)-[:WORKS_AS]->(j)

//add managers
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/employees.csv' AS row
MATCH (e: Employee {employee_id: toInteger(row.id)})
MATCH (m: Employee {employee_id: toInteger(row.manager)})
MERGE (e)-[:REPORTS_TO]->(m)

//assign skills
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/employee_skills.csv' AS row
MATCH (e: Employee {employee_id: toInteger(row.employee_id)})
MATCH (s: Skill {name: row.skill})
MERGE (e)-[:HAS_SKILL]->(s)

//load projects
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/projects.csv' AS row
MERGE (p: Project {id: toInteger(row.id), name: row.name, client: row.client, status: row.status})
RETURN p

//add employees to projects
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/kkolodziejska/GRAPHS/main/01_social_network/_data/employee_projects.csv' AS row
MATCH (e: Employee {employee_id: toInteger(row.employee_id)})
MATCH (p: Project {id: toInteger(row.project_id)})
CREATE (e)-[:WORKS_ON {start_date: date(row.start_date), end_date: date(row.end_date)}]->(p)
