import json

# Here we can add data to append the new profile to json file

with open ('profiles.json', 'r') as file:
    profiles = json.load(file)
    cnt = profiles[-1]['id']

profile = {
    'id': cnt+1,
    'user_data_dir': r'C:\Users\USER\AppData\Local\Google\Chrome\User Data\Profile 2',
    'proxy': 'http://117.54.114.33:80',
    'stealth': {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'languages': ["en-US", "en"],
        'vendor': "Google Inc.",
        'platform': "Win32",
        'webgl_vendor': "Intel Inc.",
        'renderer': "Intel Iris OpenGL Engine",
        'fix_hairline': True
    }
}

profiles.append(profile)

with open ('profiles.json', 'w') as file:
    json.dump(profiles, file, indent=2)

