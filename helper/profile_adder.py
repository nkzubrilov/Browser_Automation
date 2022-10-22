import json

# Here we can add data to append the new profile to json file

with open ('profiles.json', 'r') as file:
    profiles = json.load(file)
    try:
        cnt = profiles[-1]['id']
    except IndexError:
        cnt = None

profile = {
    'id': cnt+1 if cnt else 1,
    'user_data_dir': r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Profile 6',
    'id folder': rf'\id {cnt+1}' if cnt else r'\id 1',
    'proxy ip': '107.181.187.195:11052',
    'proxy username': 'andykaufseo',
    'proxy pass': 'HXcWZxe83t'
}

profiles.append(profile)

with open ('profiles.json', 'w') as file:
    json.dump(profiles, file, indent=2)

print('Profile', profile['id'], 'added!')
