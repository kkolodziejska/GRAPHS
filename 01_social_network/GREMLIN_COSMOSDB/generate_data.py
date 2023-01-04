from data_generators import employee_generator


if __name__ == '__main__':
    file_path = '../_data/employees.csv'
    employee_generator(2000, file_path)
