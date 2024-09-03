import requests
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

username = "rizanB"
repo_url = f"https://api.github.com/users/{username}/repos"

repo_list = requests.get(repo_url).json()

language_data = {}

for repo in repo_list:
    lang_url = repo['languages_url']
    languages = requests.get(lang_url).json()

    for lang, bytes in languages.items():
            if lang in language_data:
                language_data[lang] += bytes
            else:
                language_data[lang] = bytes

language_df = pd.DataFrame(list(language_data.items()), columns=['Language', 'Bytes'])
language_df.sort_values(by='Bytes', ascending=False, inplace=True)


plt.figure(figsize=(10, 6))
sns.barplot(data=language_df, x='Language', y='Bytes')
plt.title('Programming Languages Used on GitHub')
plt.xticks(rotation=45)
plt.ylabel('Bytes of Code')
plt.xlabel('Languages')
plt.tight_layout()
plt.savefig('programming_languages_usage.png', bbox_inches='tight')
