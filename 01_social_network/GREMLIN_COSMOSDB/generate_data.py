from data_generators import employee_generator, generate_skills_file, \
    projects_generator, assign_employees_to_projects


if __name__ == '__main__':
    file_path = '../_data/employees.csv'
    employee_skills_path = '../_data/employee_skills.csv'
    projects_path = '../_data/projects.csv'
    employees_in_projects_path = '../_data/employee_projects.csv'
    # employee_generator(2000, file_path)
    # generate_skills_file(file_path, employee_skills_path)
    # projects_generator(500, projects_path)
    assign_employees_to_projects(file_path, projects_path, employees_in_projects_path)
