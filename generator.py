import random
from datetime import datetime
import requests
import linecache
import uuid
import string 

class LocalRandomProfile():

    def generate_local_profile(self):
        cities_lines = sum(1 for line in open('data/FR/cities.txt'))
        streets_lines = sum(1 for line in open('data/FR/street.txt'))
        male_first_names_lines = sum(1 for line in open('data/FR/male_first.txt'))
        female_first_names_lines = sum(1 for line in open('data/FR/female_first.txt'))
        last_names_lines = sum(1 for line in open('data/FR/last.txt'))

        title = 'mr' if random.choice([True, False]) else 'ms'
        first_name_file = 'data/FR/male_first.txt' if title == 'mr' else 'data/FR/female_first.txt'
        first_name_lines = male_first_names_lines if title == 'mr' else female_first_names_lines

        first_name = linecache.getline(first_name_file, random.randint(1, first_name_lines)).strip()
        last_name = linecache.getline('data/FR/last.txt', random.randint(1, last_names_lines)).strip()

        profile_data = {
            'gender': 'male' if title == 'mr' else 'female',
            'name': {
                'title': title,
                'first': first_name,
                'last': last_name
            },
            'location': {
                'street': {
                    'name': linecache.getline('data/FR/street.txt', random.randint(1, streets_lines)).strip(),
                    'number': random.randint(1, 100)
                },
                'city': linecache.getline('data/FR/cities.txt', random.randint(1, cities_lines)).strip(),
                'state': 'France',
                'country': 'France',
                'postcode': str(random.randint(10000, 99999)),
                'coordinates': {
                    'latitude': str(random.uniform(-90, 90)),
                    'longitude': str(random.uniform(-180, 180))
                }
            },
            'email': f"{first_name}.{last_name}@example.com",
            'login': {
                'uuid': str(uuid.uuid4()),
                'username': f"{first_name}{random.randint(100, 999)}",
                'password': ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
                'salt': ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            },
            'dob': {
                'date': str(datetime(random.randint(1950, 2000), random.randint(1, 12), random.randint(1, 28)).date())
            }
        }

        return profile_data
    
    def generate_online_profile(self, country): 
        api_url = f'https://randomuser.me/api/?nat={country}'
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch user data. Status Code: {response.status_code}")
            return None
 
    
    def include_fields(self, include_list, profile_data, field_name, field_value):
        if field_name in include_list:
            profile_data[field_name] = field_value() if callable(field_value) else field_value

    def generate_id(self, profile_data):
        dob_date = datetime.strptime(profile_data['dob']['date'].split('T')[0], "%Y-%m-%d")
        gender = 1 if profile_data['gender'] == 'male' else 2
        year = dob_date.year
        month = dob_date.month
        random_num = random.randint(10000000, 99999999)
        cc = (97 - (int(f"{gender}{year}{month}{random_num}") % 97))

        return {
            'name': 'INSEE',
            'value': f"{gender}{year}{month}{random_num} {str(cc).zfill(2)}"
        }