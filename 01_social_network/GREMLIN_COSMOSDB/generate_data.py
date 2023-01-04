from data_generators import employee_generator, generate_skills_file


if __name__ == '__main__':
    file_path = '../_data/employees.csv'
    employee_skills_path = '../_data/employee_skills.csv'
    # employee_generator(2000, file_path)
    generate_skills_file(file_path, employee_skills_path)
