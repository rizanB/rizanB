import requests
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

token = os.environ.get('GITHUB_TOKEN')

headers = {'Authorization': f'token {token}'} if token else {}
repo_url = "https://api.github.com/user/repos?type=all&per_page=100"

if not token:
    print("No token found, using public repos only")
    repo_url = "https://api.github.com/users/rizanB/repos"

repo_list = requests.get(repo_url, headers=headers).json()

language_data = {}
processed_repos = 0
total_repos = len(repo_list)

for repo in repo_list:
    print(f"Processing {repo['name']} ({processed_repos + 1}/{total_repos})")
    lang_url = repo['languages_url']
    
    languages = requests.get(lang_url, headers=headers).json()
    
    for lang, bytes_count in languages.items():
        if lang in language_data:
            language_data[lang] += bytes_count
        else:
            language_data[lang] = bytes_count
    
    processed_repos += 1

language_df = pd.DataFrame(list(language_data.items()), columns=['Language', 'Bytes'])
language_df.sort_values(by='Bytes', ascending=False, inplace=True)

plt.figure(figsize=(12, 8))
sns.barplot(data=language_df, x='Language', y='Bytes', palette='viridis')

title = 'Languages across all my repos' if token else 'Languages on my public repos'
plt.title(title, fontsize=16, fontweight='bold')

plt.xticks(rotation=45, ha='right')
plt.ylabel('bytes', fontsize=12)
plt.xlabel('language', fontsize=12)

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

plt.savefig('programming_languages_usage.png', bbox_inches='tight', dpi=300)
print(f"Chart saved! Processed {len(language_data)} languages from {total_repos} repositories.")