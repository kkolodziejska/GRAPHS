// show all hierarchies in company
MATCH p=(start_employee:Employee)-[:REPORTS_TO*]->(end_employee:Employee)
WHERE NOT ()-[:REPORTS_TO]->(start_employee)
AND NOT (end_employee)-[:REPORTS_TO]->()
RETURN p

// find all employees that report to employee with id 1179
MATCH p=(e: Employee)-[:REPORTS_TO]->(: Employee {employee_id: 1179}) RETURN p

// find all employees with specialisation
MATCH p=(e: Employee)-[:WORKS_AS|IN_SPECIALISATION*]->(s: Specialisation {name: 'Big Data'}) RETURN p

// find all employees working on a project with id 33
MATCH p=(e:Employee)-[:WORKS_ON]->(:Project {id: 33})
MATCH k=(e)-[:WORKS_AS|IN_SPECIALISATION*]->(s:Specialisation)
RETURN p, k

// find employees for new project
MATCH
(e:Employee)-[:WORKS_AS]->(j:Job_title)-[:IN_SPECIALISATION*]->(s:Specialisation {name: 'Big Data'})
WHERE e.performance_score > 150
MATCH (e)-[:HAS_SKILL]->(t:Skill)
WHERE t.name IN ['Python', 'Spark', 'AWS']
OPTIONAL MATCH p=(e:Employee)-[:WORKS_ON]->(:Project)<-[:WORKS_ON]-(r:Employee {employee_id: 0})
RETURN e as Employee, j.name as Position, collect(t.name) as Skills,
(CASE
WHEN p IS NULL THEN False
ELSE True
END) as is_referenced
ORDER BY size(Skills) DESC, Employee.performance_score DESC, is_referenced DESC;

// find all managers and mean of performance score of people that report to them
MATCH (e:Employee)-[:REPORTS_TO]->(m: Employee)
WITH m as Manager, collect(e.performance_score) as performance
WHERE size(performance) > 2
RETURN Manager, reduce(acc=0,score in performance|acc+score)/size(performance) as mean_performance_score
ORDER BY mean_performance_score DESC;

// find juniors with best performance score in each specialisation
MATCH (e: Employee)-[:WORKS_AS]->(j:Job_title)-[:IN_SPECIALISATION]->(s:Specialisation)
WHERE j.name STARTS WITH 'Junior'
WITH s AS Specialisation, e as Employee, e.performance_score as Performance
WITH Specialisation, apoc.agg.maxItems(Employee, Performance) as Best
RETURN Specialisation, Best['value'] as Best_Performance_Score, Best['items'] as Employees