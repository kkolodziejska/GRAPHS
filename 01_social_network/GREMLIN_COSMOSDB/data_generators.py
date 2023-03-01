import csv
import random

from faker import Faker
from datetime import date


def specialisation_generator() -> list:
    specialisations = [
        'Big Data',
        'UI',
        'Data Analysis',
        'Backend',
        'Mobile',
        'QA',
        'DevOps',
    ]

    return specialisations


def job_title_generator() -> dict:
    job_titles = {
        'Big Data': [
            'Junior Big Data Engineer',
            'Big Data Engineer',
            'Senior Big Data Engineer',
            'Staff Big Data Engineer',
            ],
        'UI': [
            'Junior UI Developer',
            'UI Developer',
            'Senior UI Developer',
            'Staff UI Developer'
        ],
        'Data Analysis': [
            'Junior Data Analyst',
            'Data Analyst',
            'Senior Data Analyst',
            'Staff Data Analyst',
        ],
        'Backend': [
            'Junior Backend Developer',
            'Backend Developer',
            'Senior Backend Developer',
            'Staff Backend Developer'
        ],
        'Mobile': [
            'Junior Mobile Developer',
            'Mobile Developer',
            'Senior Mobile Developer',
            'Staff Mobile Developer'
        ],
        'QA': [
            'Junior QA Engineer',
            'QA Engineer',
            'Senior QA Engineer',
            'Staff QA Engineer'
        ],
        'DevOps': [
            'Junior DevOps Engineer',
            'DevOps Engineer',
            'Senior DevOps Engineer',
            'Staff DevOps Engineer'
        ]
    }

    return job_titles


def skills_generator() -> dict:
    skills = {
        'Big Data': [
            'AWS',
            'Java',
            'Python',
            'Scala',
            'Spark',
            'Hadoop',
            'NoSQL databases',
            'relational databases',
            'SQL',
            'Microsoft Azure',
            'Google Cloud',
        ],
        'UI': [
            'Javascript',
            'Typescript',
            'React',
            'Angular',
            'AWS',
            'Microsoft Azure',
            'Google Cloud',
            'HTML/CSS',
        ],
        'Data Analysis': [
            'Tableau',
            'SQL',
            'AWS',
            'Microsoft Azure',
            'Google Cloud',
            'Firebase',
            'Microsoft Power BI',
        ],
        'Backend': [
            'Java',
            'Python',
            'AWS',
            'Microsoft Azure',
            'Google Cloud',
            'relational databases',
        ],
        'Mobile': [
            'Kotlin',
            'Android',
            'IOS',
            'Flutter',
            'Xamarin',
            'React Native',
        ],
        'QA': [
            'Python',
            'Java',
            'PyRestTest',
            'Postman',
            'JUNIT',
            'Spock',
        ],
        'DevOps': [
            'AWS',
            'Google Cloud',
            'Microsoft Azure',
            'Docker',
            'Kubernetes',
            'Puppet',
            'Chef',
            'Docker Compose',
            'Terraform'
        ]
    }

    return skills


def employee_generator(n: int, file_name: str = None) -> None:

    employees = dict()

    specialisations = specialisation_generator()
    job_titles = job_title_generator()
    skills = skills_generator()

    managers = {spec: list() for spec in specialisations}

    spec_len = len(specialisations) - 1

    fake = Faker()
    Faker.seed(0)

    for i in range(n):

        gender = random.randint(1, 2)

        employee_data = {
            'id': i,
            'surname': fake.last_name_female() if gender == 1
            else fake.last_name_male(),
            'name': fake.first_name_female() if gender == 1
            else fake.first_name_male(),
            'gender': 'female' if gender == 1 else 'male',
            'birthday': fake.date_between(date(1980, 1, 1), date(1998, 1, 1)),
            'phone': fake.phone_number(),
            'hire_date': fake.date_between(date(2016, 1, 1), date(2022, 1, 1)),
            'fire_date': None,
            'specialisation': specialisations[random.randint(0, spec_len)],
            'performance_score': random.randint(100, 200),
            'manager': None
        }

        # set email from employee name and surname
        employee_data['email'] = employee_data.get('surname').lower().replace(" ", "") + \
                                 employee_data.get('name').lower().replace(" ", "") + \
                                 '@example.org'

        employee_specialisation = employee_data.get('specialisation')

        # set job title and check if employee can be manager
        job_title = job_titles[employee_specialisation][random.randint(0, 3)]
        employee_data['job_title'] = job_title

        if job_title.startswith('Senior') or job_title.startswith('Staff'):
            managers[employee_specialisation].append(i)

        # set employee skills
        employee_data['skills'] = list(set([
            skills[employee_specialisation][random.randint(
                0, len(skills[employee_specialisation])) - 1]
            for i in range(random.randint(3, 7))]))

        # add employee to dict
        employees[i] = employee_data

    # add head of company
    ceo_data = {
        'id': n,
        'surname': fake.last_name_female(),
        'name': fake.first_name_female(),
        'gender': 'female',
        'birthday': fake.date_between(date(1980, 1, 1), date(1998, 1, 1)),
        'phone': fake.phone_number(),
        'hire_date': date(2016, 1, 1),
        'fire_date': None,
        'specialisation': None,
        'performance_score': 200,
        'manager': None,
        'job_title': "CEO",
        'skills': None
    }

    ceo_data['email'] = ceo_data.get('surname').lower().replace(" ", "") + \
                        ceo_data.get('name').lower().replace(" ", "") + \
                        '@example.org'

    employees[n] = ceo_data

    # assign managers
    for employee_id, data in employees.items():

        if not data.get('job_title').startswith('Staff') \
                and not data.get('job_title') == "CEO":
            print(data)
            specialisation = data.get('specialisation')
            possible_managers = managers[specialisation]
            number_of_managers = len(possible_managers)

            if number_of_managers == 0:
                data['manager'] = n
            elif number_of_managers == 1 and employee_id in possible_managers:
                data['manager'] = n
            elif number_of_managers == 2 and employee_id in possible_managers:
                possible_managers.remove(employee_id)
                another_manager = possible_managers[0]
                if employees[another_manager]['manager'] == employee_id:
                    data['manager'] = n
                else:
                    data['manager'] = another_manager
            else:
                manager_id = employee_id

                while manager_id == employee_id \
                        or employees[manager_id]['manager'] == employee_id:
                    manager_id = possible_managers[
                        random.randint(0, number_of_managers - 1)]

                data['manager'] = manager_id

        elif data.get('job_title').startswith('Staff'):
            data['manager'] = n

    # write to file or output
    if not file_name:
        for employee_id, data in employees.items():
            print(employee_id, data)
    else:
        with open(file_name, 'w', newline='') as f:
            fieldnames = [
                'id',
                'surname',
                'name',
                'gender',
                'birthday',
                'phone',
                'email',
                'hire_date',
                'fire_date',
                'specialisation',
                'job_title',
                'skills',
                'performance_score',
                'manager'
                ]
            csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
            csvwriter.writeheader()

            for employee_id, data in employees.items():
                csvwriter.writerow(data)


def generate_skills_file(source_file: str, sink_file: str = None) -> None:

    with open(source_file, 'r') as source:
        with open(sink_file, 'w') as sink:
            csvreader = csv.DictReader(source)
            csvwriter = csv.DictWriter(sink, fieldnames=['employee_id', 'skill'])
            csvwriter.writeheader()
            for row in csvreader:
                employee_id = int(row['id'])
                skills = row['skills'].strip('[]').replace('\'', '').split(', ')
                for skill in skills:
                    csvwriter.writerow({
                        'employee_id': employee_id,
                        'skill': skill
                    })


def projects_generator(n: int, file_name: str = None) -> None:
    projects = list()

    fake = Faker()
    Faker.seed(0)

    statuses = ['in preparation', 'finished'] + ['ongoing'] * 5

    for i in range(n):
        project_data = {
            'id': i,
            'name': fake.uuid4(),
            'client': fake.company(),
            'status': statuses[random.randint(0, 6)]
        }

        projects.append(project_data)

    if not file_name:
        for project in projects:
            print(project)
    else:
        with open(file_name, 'w') as f:
            fieldnames = ['id', 'name', 'client', 'status']
            csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
            csvwriter.writeheader()

            for project in projects:
                csvwriter.writerow(project)


def get_projects(file_name: str) -> list:

    projects = list()

    with open(file_name, 'r') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            projects.append({
                'id': row['id'],
                'status': row['status']
            })

    return projects


def assign_employees_to_projects(employees_file: str,
                                 projects_file: str,
                                 sink_file: str) -> None:

    projects = get_projects(projects_file)
    last_index = len(projects) - 1

    fake = Faker('pl_PL')
    Faker.seed(0)

    with open(employees_file, 'r') as source:
        with open(sink_file, 'w') as sink:
            csvreader = csv.DictReader(source)

            fieldnames = ['employee_id', 'project_id', 'start_date', 'end_date']
            csvwriter = csv.DictWriter(sink, fieldnames=fieldnames)
            csvwriter.writeheader()

            for row in csvreader:
                if row['job_title'] != "CEO":
                    project_id = random.randint(0, last_index)
                    while projects[project_id]['status'] == 'finished':
                        data = {
                            'employee_id': row['id'],
                            'project_id': project_id,
                            'start_date': fake.date_between(
                                date.fromisoformat(row['hire_date']),
                                date(2022, 1, 1))
                        }
                        data['end_date'] = fake.date_between(
                            data['start_date'],
                            date(2022, 1, 1)
                        )
                        csvwriter.writerow(data)
                        project_id = random.randint(0, last_index)

                    data = {
                        'employee_id': row['id'],
                        'project_id': project_id,
                        'start_date': fake.date_between(
                            date.fromisoformat(row['hire_date']),
                            date(2022, 1, 1))
                    }
                    csvwriter.writerow(data)


def save_skills_to_csv(file_path: str) -> None:

    all_skills = skills_generator()
    labels = ['skill', 'specialisation']

    with open(file_path, 'w') as f:
        csvwriter = csv.DictWriter(f, fieldnames=labels)
        csvwriter.writeheader()

        for specialisation, skills in all_skills.items():
            for skill in skills:
                csvwriter.writerow({
                    'skill': skill,
                    'specialisation': specialisation}
                )


def get_employees_without_skills(source_path: str, sink_path: str) -> None:

    with open(source_path, 'r') as source:
        with open(sink_path, 'w') as sink:

            csvreader = csv.DictReader(source)

            fieldnames = [
                'id',
                'surname',
                'name',
                'gender',
                'birthday',
                'phone',
                'email',
                'hire_date',
                'specialisation',
                'job_title',
                'performance_score',
                'manager'
            ]

            csvwriter = csv.DictWriter(sink, fieldnames=fieldnames)
            csvwriter.writeheader()

            for row in csvreader:
                row.pop('skills')
                row.pop('fire_date')
                csvwriter.writerow(row)
