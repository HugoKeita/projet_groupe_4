import argparse
import json
import os
import urllib.request
import shutil
import glob
import random
from generator import LocalRandomProfile


def generate_random_profile(country):
    instance_random_profile = LocalRandomProfile()

    if country == 'FR':
        online_profile = instance_random_profile.generate_online_profile(country)
        if online_profile is not None:
            response = instance_random_profile.generate_local_profile()
        else:
            response = None
    else:
        response = instance_random_profile.generate_online_profile(country)

    if response and country == 'FR':
        return {'results': [response]}
    elif response and country != 'FR':
        return response
    else:
        print(f"Error: Unable to fetch user data.")
        return None

def display_user_profile_local(user_profile):
    if not user_profile:
        return "Failed to generate user profile."

    profile = user_profile['results'][0]
    profile_string = f"Generated User Profile:\n"
    profile_string += f"Gender:\n  {profile['gender']}\n"
    profile_string += f"Name:\n  Title: {profile['name']['title']}\n  First Name: {profile['name']['first']}\n  Last Name: {profile['name']['last']}\n"
    profile_string += f"Location:\n  Street: {profile['location']['street']['name']}\n  Number: {profile['location']['street']['number']}\n  City: {profile['location']['city']}\n  State: {profile['location']['state']}\n  Country: {profile['location']['country']}\n  Postcode: {profile['location']['postcode']}\n  Coordinates: {profile['location']['coordinates']['latitude']}, {profile['location']['coordinates']['longitude']}\n"
    profile_string += f"Identifier:\n  UUID: {profile['login']['uuid']}\n"
    profile_string += f"Email:\n  {profile['email']}\n"
    profile_string += f"Date of Birth:\n  {profile['dob']['date'].split('T')[0]}\n"
    profile_string += f"Username:\n  {profile['login']['username']}\n"
    profile_string += f"Password:\n  {profile['login']['password']}\n"
    profile_string += f"Salt:\n  {profile['login']['salt']}\n"

    return profile_string


def display_user_profile_online(user_profile):
    profile_string = json.dumps(user_profile, indent=4)
    return profile_string

def save_profile_to_file_online(user_profile):
    if not user_profile:
        raise ValueError("Failed to generate user profile.")
    profile_string = display_user_profile_online(user_profile)
    first_name = user_profile['results'][0]['name']['first']
    last_name = user_profile['results'][0]['name']['last']
    filename = f"Generated_profiles/{first_name}.{last_name}_online.json"
    if not os.path.exists("Generated_profiles"):
        os.makedirs("Generated_profiles")
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(profile_string)

    print(f"Profile saved to file: {filename}")
    return profile_string



def save_profile_to_file_local(user_profile):
    if not user_profile:
        raise ValueError("Failed to generate user profile.")

    profile = user_profile['results'][0]
    first_name = profile['name']['first']
    last_name = profile['name']['last']
    filename = f"Generated_profiles/{first_name}.{last_name}.json"

    if not os.path.exists("Generated_profiles"):
        os.makedirs("Generated_profiles")

    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(user_profile, file, indent=4)

    print(f"Profile saved to file: {filename}")


def main():
    parser = argparse.ArgumentParser(description='Generate a random user profile.')
    parser.add_argument('-l', '--country', default=None,
                        help='Specify the country code for the user profile FR, AU, BR, CA, CH, DE, DK, ES, FI, GB, IE, IN, IR, MX, NL, NO, NZ, RS, TR, UA, US')
    args = parser.parse_args()

    available_countries = ['FR', 'AU', 'BR', 'CA', 'CH', 'DE', 'DK', 'ES', 'FI', 'GB', 'IE', 'IN', 'IR', 'MX', 'NL', 'NO',
                           'NZ', 'RS', 'TR', 'UA', 'US']

    if args.country is None:
        raise ValueError("Country not specified.")

    if args.country not in available_countries and args.country is not None:
        raise ValueError("Country not available yet.")

    user_profile = generate_random_profile(args.country)
    
    if user_profile:
        print("Resume of the generated profile, the complete version can be found in profile folder :" + "\n")
        
        if args.country == 'FR':
            profile_string = display_user_profile_local(user_profile)
            print(profile_string)
            save_profile_to_file_local(user_profile)
        else:
            profile_string = display_user_profile_online(user_profile)
            print(profile_string)
            save_profile_to_file_online(user_profile)

        first_name = user_profile['results'][0].get('name', {}).get('first', '')
        last_name = user_profile['results'][0].get('name', {}).get('last', '')
        image_filename = f"Generated_profiles/{first_name}.{last_name}.jpg"

        if args.country == 'FR':
            gender = user_profile['results'][0]['gender']
            image_folder = f"data/FR/{gender}"
            image_files = glob.glob(f"{image_folder}/*.jpg")
            selected_image = random.choice(image_files)
            shutil.copy(selected_image, image_filename)
            print(f"Image selected successfully: {image_filename}")
        else:
            image_url = user_profile['results'][0]['picture']['large']
            try:
                urllib.request.urlretrieve(image_url, image_filename)
                print(f"Image downloaded successfully: {image_filename}")
            except Exception as e:
                print(f"Error downloading image: {str(e)}")

if __name__ == "__main__":
    main()
