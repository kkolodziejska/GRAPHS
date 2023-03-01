from data_generators import employee_generator, generate_skills_file, \
    projects_generator, assign_employees_to_projects, save_skills_to_csv, get_employees_without_skills


if __name__ == '__main__':
    file_path = '../_data/employees.csv'
    employee_skills_path = '../_data/employee_skills.csv'
    projects_path = '../_data/projects.csv'
    employees_in_projects_path = '../_data/employee_projects.csv'
    skills_path = '../_data/skills.csv'
    # employee_generator(3000, file_path)
    # generate_skills_file(file_path, employee_skills_path)
    # projects_generator(100, projects_path)
    # assign_employees_to_projects(file_path, projects_path, employees_in_projects_path)
    # save_skills_to_csv(skills_path)

    get_employees_without_skills(file_path, '../_data/employees2.csv')
