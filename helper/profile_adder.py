import json

# Here we can add data to append the new profile to json file

with open ('profiles.json', 'r') as file:
    profiles = json.load(file)
    cnt = profiles[-1]['id']

profile = {
    'id': cnt+1,
    'user_data_dir': r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Profile 2',
    'proxy': '51.15.242.202:8888'
}

profiles.append(profile)

with open ('profiles.json', 'w') as file:
    json.dump(profiles, file, indent=2)

