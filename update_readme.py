import os
import requests
import re

# Repositories to fetch and feature on your profile
REPOS = [
    "Hassan-Raza-Shaikh/giki_course_hub-1",
    "hamxa296/ML-Project-hehe",
    "ZainJ5/Plant-Growth-and-Harvesting-Monitoring-System",
    "Hassan-Raza-Shaikh/Projects",
    "Hassan-Raza-Shaikh/Python"
]

# Custom professional fallback descriptions and clean display titles
REPO_META = {
    "Hassan-Raza-Shaikh/giki_course_hub-1": {
        "title": "GIKI Course Hub",
        "description": "A public resource hub built for sharing and accessing university course materials."
    },
    "hamxa296/ML-Project-hehe": {
        "title": "ML Project",
        "description": "Collaborating on machine learning models, data analysis pipelines, and evaluation metrics."
    },
    "ZainJ5/Plant-Growth-and-Harvesting-Monitoring-System": {
        "title": "Plant Growth & Harvesting Monitoring System",
        "description": "An IoT and computer vision monitoring system for tracking crop health and growth cycles."
    },
    "Hassan-Raza-Shaikh/Projects": {
        "title": "Projects",
        "description": "A collection of personal software implementations and academic assignments."
    },
    "Hassan-Raza-Shaikh/Python": {
        "title": "Python Utilities",
        "description": "A repository of Python scripts, utility tools, and developmental playground tests."
    }
}

token = os.environ.get("GITHUB_TOKEN")
headers = {}
if token:
    headers["Authorization"] = f"token {token}"

repo_data = []
for repo in REPOS:
    url = f"https://api.github.com/repos/{repo}"
    name_split = repo.split("/")
    repo_key = repo
    fallback_title = REPO_META[repo_key]["title"]
    fallback_desc = REPO_META[repo_key]["description"]
    is_contributor = name_split[0] != "Hassan-Raza-Shaikh"
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            repo_data.append({
                "title": fallback_title,
                "url": data["html_url"],
                "description": data["description"] or fallback_desc,
                "language": data["language"] or "Markdown",
                "is_contributor": is_contributor
            })
            continue
    except Exception as e:
        print(f"Error fetching {repo}: {e}")
        
    repo_data.append({
        "title": fallback_title,
        "url": f"https://github.com/{repo}",
        "description": fallback_desc,
        "language": "Python" if "ML" in fallback_title or "Plant" in fallback_title or "Python" in fallback_title else "C++" if "Projects" in fallback_title else "JavaScript",
        "is_contributor": is_contributor
    })

# Construct HTML Table
html = """<table>
  <tr>
"""

for i, repo in enumerate(repo_data):
    role = " <i>(Contributor)</i>" if repo["is_contributor"] else ""
    lang_badge = f"<code>{repo['language']}</code>"
    
    # Choose clean emojis
    emoji = "🌱" if "Plant" in repo["title"] else "🤖" if "ML" in repo["title"] else "📚" if "GIKI" in repo["title"] else "📁"
    
    cell = f"""    <td width="50%" valign="top">
      <b>{emoji} <a href="{repo['url']}">{repo['title']}</a></b>{role}<br/>
      {repo['description']}<br/>
      {lang_badge}
    </td>"""
    
    if i == 4:  # Last item takes full row
        html += f"""  </tr>
  <tr>
    <td colspan="2" valign="top">
      <b>⚙️ <a href="{repo['url']}">{repo['title']}</a></b>{role}<br/>
      {repo['description']}<br/>
      {lang_badge}
    </td>
  </tr>
"""
    elif i % 2 == 1:
        html += cell + "\n  </tr>\n"
        if i < 3:
            html += "  <tr>\n"
    else:
        html += cell + "\n"

html += "</table>"

# Update README.md
with open("README.md", "r") as f:
    content = f.read()

pattern = r"<!-- START_SECTION:projects -->.*?<!-- END_SECTION:projects -->"
replacement = f"<!-- START_SECTION:projects -->\n{html}\n<!-- END_SECTION:projects -->"
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(new_content)

print("Projects section updated successfully with clean metadata!")
