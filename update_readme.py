import os
import requests
import re

username = "Hassan-Raza-Shaikh"
token = os.environ.get("GITHUB_TOKEN")
headers = {}
if token:
    headers["Authorization"] = f"token {token}"

# --- Part 1: Fetch and Auto-Update Projects ---
REPOS = [
    "Hassan-Raza-Shaikh/giki_course_hub-1",
    "hamxa296/ML-Project-hehe",
    "ZainJ5/Plant-Growth-and-Harvesting-Monitoring-System",
    "Hassan-Raza-Shaikh/Projects",
    "Hassan-Raza-Shaikh/Python"
]

REPO_META = {
    "Hassan-Raza-Shaikh/giki_course_hub-1": {
        "title": "GIKI Course Hub",
        "description": "Our university academic resource platform, providing course material sharing and management. Currently live and actively used."
    },
    "hamxa296/ML-Project-hehe": {
        "title": "ML Project",
        "description": "Collaborative machine learning pipeline implementing credit fraud detection and model ensemble comparisons."
    },
    "ZainJ5/Plant-Growth-and-Harvesting-Monitoring-System": {
        "title": "Plant Growth & Harvesting Monitoring System",
        "description": "An IoT and computer vision monitoring system designed for tracking crop health metrics and harvesting cycles."
    },
    "Hassan-Raza-Shaikh/Projects": {
        "title": "Projects",
        "description": "Academic software developments, data structures implementations, and core computational logic systems."
    },
    "Hassan-Raza-Shaikh/Python": {
        "title": "Python Utilities",
        "description": "A curated playground of Python implementations, scripting utilities, and numerical analysis models."
    }
}

repo_data = []
for repo in REPOS:
    url = f"https://api.github.com/repos/{repo}"
    name_split = repo.split("/")
    repo_key = repo
    fallback_title = REPO_META[repo_key]["title"]
    fallback_desc = REPO_META[repo_key]["description"]
    is_contributor = name_split[0] != "Hassan-Raza-Shaikh"
    
    try:
        res = requests.get(url, headers=headers, timeout=5)
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

# Construct HTML Table for Projects
projects_html = """<table>
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
        projects_html += f"""  </tr>
  <tr>
    <td colspan="2" valign="top">
      <b>⚙️ <a href="{repo['url']}">{repo['title']}</a></b>{role}<br/>
      {repo['description']}<br/>
      {lang_badge}
    </td>
  </tr>
"""
    elif i % 2 == 1:
        projects_html += cell + "\n  </tr>\n"
        if i < 3:
            projects_html += "  <tr>\n"
    else:
        projects_html += cell + "\n"

projects_html += "</table>"


# --- Part 2: Scan Repos for Languages & Frameworks ---

# Color-respective badges using official brand colors (style=for-the-badge)
BADGE_MAPPING = {
    # Languages
    "python": "https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white",
    "c++": "https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white",
    "cplusplus": "https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white",
    "c": "https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=white",
    "r": "https://img.shields.io/badge/R-276F40?style=for-the-badge&logo=r&logoColor=white",
    "javascript": "https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black",
    "js": "https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black",
    "typescript": "https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white",
    "ts": "https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white",
    "html": "https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white",
    "html5": "https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white",
    "css": "https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white",
    "css3": "https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white",
    "sql": "https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white",
    "postgresql": "https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white",
    "postgres": "https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white",
    "sqlite": "https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white",
    "mysql": "https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white",
    "latex": "https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white",
    "tex": "https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white",
    "shell": "https://img.shields.io/badge/Shell_Script-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white",
    "bash": "https://img.shields.io/badge/Shell_Script-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white",
    "makefile": "https://img.shields.io/badge/Makefile-000000?style=for-the-badge&logo=gnu&logoColor=white",
    "java": "https://img.shields.io/badge/Java-007396?style=for-the-badge&logo=java&logoColor=white",
    "go": "https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white",
    "rust": "https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white",

    # Frameworks & Libraries
    "react": "https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black",
    "reactjs": "https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black",
    "next.js": "https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white",
    "nextjs": "https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white",
    "node.js": "https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white",
    "nodejs": "https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white",
    "flask": "https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white",
    "fastapi": "https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white",
    "express": "https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white",
    "expressjs": "https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white",
    "tailwind css": "https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white",
    "tailwind": "https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white",
    "bootstrap": "https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white",
    "vite": "https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white",
    "arduino": "https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white",
    "esp32": "https://img.shields.io/badge/ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white",
    "django": "https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white",

    # AI & Data Science
    "pytorch": "https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white",
    "tensorflow": "https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white",
    "scikit-learn": "https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white",
    "sklearn": "https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white",
    "numpy": "https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white",
    "pandas": "https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white",
    "opencv": "https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white",
    "matplotlib": "https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white",
    "seaborn": "https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge&logo=python&logoColor=white",
    "jupyter": "https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white",
    "jupyter notebook": "https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white",
    "xgboost": "https://img.shields.io/badge/XGBoost-1E88E5?style=for-the-badge&logo=python&logoColor=white",
    "lightgbm": "https://img.shields.io/badge/LightGBM-008080?style=for-the-badge&logo=python&logoColor=white",
    "catboost": "https://img.shields.io/badge/CatBoost-F50057?style=for-the-badge&logo=python&logoColor=white",
    "scipy": "https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white",

    # Cloud & Databases
    "firebase": "https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black",
    "aws": "https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white",
    "vercel": "https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white",
    "mongodb": "https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white",
    "heroku": "https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white",

    # Tools & DevOps
    "git": "https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white",
    "github actions": "https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white",
    "docker": "https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white",
    "cmake": "https://img.shields.io/badge/CMake-064F8C?style=for-the-badge&logo=cmake&logoColor=white",
    "quarto": "https://img.shields.io/badge/Quarto-75AADB?style=for-the-badge&logo=quarto&logoColor=white",
}

# Categorize tech mappings
CATEGORIES = {
    "languages": ["python", "c++", "cplusplus", "c", "r", "javascript", "js", "typescript", "ts", "html", "html5", "css", "css3", "sql", "postgresql", "postgres", "sqlite", "mysql", "latex", "tex", "shell", "bash", "makefile", "java", "go", "rust"],
    "frameworks": ["react", "reactjs", "next.js", "nextjs", "node.js", "nodejs", "flask", "fastapi", "express", "expressjs", "tailwind css", "tailwind", "bootstrap", "vite", "arduino", "esp32", "django"],
    "ai_data_science": ["pytorch", "tensorflow", "scikit-learn", "sklearn", "numpy", "pandas", "opencv", "matplotlib", "seaborn", "jupyter", "jupyter notebook", "xgboost", "lightgbm", "catboost", "scipy", "evidently"],
    "cloud_db": ["firebase", "aws", "vercel", "mongodb", "heroku"],
    "tools_devops": ["git", "github actions", "docker", "cmake", "quarto", "pytest", "prefect"]
}

# Standardized names for displaying
TECH_DISPLAY_NAMES = {
    "js": "JavaScript", "javascript": "JavaScript",
    "ts": "TypeScript", "typescript": "TypeScript",
    "python": "Python",
    "c++": "C++", "cplusplus": "C++",
    "c": "C",
    "r": "R",
    "html": "HTML5", "html5": "HTML5",
    "css": "CSS3", "css3": "CSS3",
    "sql": "SQL", "postgresql": "PostgreSQL", "postgres": "PostgreSQL", "sqlite": "SQLite", "mysql": "MySQL",
    "latex": "LaTeX", "tex": "LaTeX",
    "shell": "Shell Script", "bash": "Shell Script",
    "makefile": "Makefile",
    "java": "Java", "go": "Go", "rust": "Rust",
    
    "react": "React", "reactjs": "React",
    "next.js": "Next.js", "nextjs": "Next.js",
    "node.js": "Node.js", "nodejs": "Node.js",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "express": "Express", "expressjs": "Express",
    "tailwind css": "Tailwind CSS", "tailwind": "Tailwind CSS",
    "bootstrap": "Bootstrap",
    "vite": "Vite",
    "arduino": "Arduino", "esp32": "ESP32", "django": "Django",
    
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "scikit-learn": "scikit-learn", "sklearn": "scikit-learn",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "opencv": "OpenCV",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "jupyter": "Jupyter", "jupyter notebook": "Jupyter",
    "xgboost": "XGBoost", "lightgbm": "LightGBM", "catboost": "CatBoost", "scipy": "SciPy",
    
    "firebase": "Firebase", "aws": "AWS", "vercel": "Vercel", "mongodb": "MongoDB", "heroku": "Heroku",
    
    "git": "Git", "github actions": "GitHub Actions", "docker": "Docker", "cmake": "CMake", "quarto": "Quarto",
    "pytest": "Pytest", "prefect": "Prefect", "evidently": "Evidently"
}

detected_tech = set()
detected_tech.add("git") # Always present

# Directories to skip when scanning repos
IGNORED_DIRS = {
    "node_modules", "venv", ".venv", "env", ".git", "dist", "build", 
    "__pycache__", ".next", "target", "out", ".cache", "bower_components"
}

# List of repos to scan
repos_to_scan = []

# Fetch user's own repositories
fetched_repos = False
try:
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    res = requests.get(url, headers=headers, timeout=5)
    if res.status_code == 200:
        repos = res.json()
        for r in repos:
            if not r["fork"]:
                repos_to_scan.append({
                    "owner": username,
                    "name": r["name"],
                    "default_branch": r.get("default_branch", "main"),
                    "language": r.get("language")
                })
        fetched_repos = True
    else:
        print(f"Failed to fetch repositories list: {res.status_code}")
except Exception as e:
    print(f"Error listing user repos: {e}")

if not fetched_repos:
    print("Falling back to local directory listing for user repositories...")
    try:
        # List sibling directories in parent directory (Projects folder)
        parent_dir = ".."
        if os.path.isdir(parent_dir):
            for item in os.listdir(parent_dir):
                item_path = os.path.join(parent_dir, item)
                if os.path.isdir(item_path) and not item.startswith(".") and item != "Hassan-Raza-Shaikh":
                    repos_to_scan.append({
                        "owner": username,
                        "name": item,
                        "default_branch": "main",
                        "language": None
                    })
    except Exception as e:
        print(f"Error scanning local parent directories: {e}")

# Append the external featured contributions
for ext_repo in ["hamxa296/ML-Project-hehe", "ZainJ5/Plant-Growth-and-Harvesting-Monitoring-System"]:
    parts = ext_repo.split("/")
    repos_to_scan.append({
        "owner": parts[0],
        "name": parts[1],
        "default_branch": "main",
        "language": None
    })

# Scan each repository recursively
for repo in repos_to_scan:
    owner = repo["owner"]
    name = repo["name"]
    branch = repo["default_branch"]
    print(f"Scanning {owner}/{name} on branch {branch}...")
    
    # 1. Add repo primary language if exists
    if repo["language"]:
        lang_lower = repo["language"].lower()
        if lang_lower in BADGE_MAPPING:
            detected_tech.add(lang_lower)
            
    # 2. Check name and description for tags
    name_lower = name.lower()
    if "quarto" in name_lower:
        detected_tech.add("quarto")
    if "latex" in name_lower:
        detected_tech.add("latex")
    if "arduino" in name_lower:
        detected_tech.add("arduino")
    if "portfolio" in name_lower or "giki_course_hub" in name_lower:
        detected_tech.add("react")
        detected_tech.add("next.js")
        detected_tech.add("node.js")
        
    # 3. Scan files (either locally if directory exists, or via GitHub API as fallback)
    local_path = f"../{name}"
    scanned_locally = False
    file_paths = []
    has_github_actions = False
    
    if os.path.isdir(local_path):
        print(f"Scanning locally at {local_path}...")
        try:
            for root, dirs, files in os.walk(local_path):
                # prune ignored directories in-place
                dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]
                for file in files:
                    full_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_file_path, local_path)
                    file_paths.append(rel_path)
                    if ".github/workflows" in rel_path:
                        has_github_actions = True
            scanned_locally = True
        except Exception as e:
            print(f"Error scanning local files at {local_path}: {e}")
            
    if not scanned_locally:
        try:
            tree_url = f"https://api.github.com/repos/{owner}/{name}/git/trees/{branch}?recursive=1"
            res = requests.get(tree_url, headers=headers, timeout=5)
            if res.status_code == 200:
                tree_data = res.json()
                tree = tree_data.get("tree", [])
                
                for item in tree:
                    if item["type"] == "blob":
                        path = item["path"]
                        parts = path.split("/")
                        skip = False
                        for p in parts[:-1]:
                            if p in IGNORED_DIRS or p.startswith("."):
                                skip = True
                                break
                        if skip:
                            continue
                            
                        file_paths.append(path)
                        if ".github/workflows" in path:
                            has_github_actions = True
            else:
                print(f"Failed to fetch tree for {owner}/{name}: {res.status_code}")
        except Exception as e:
            print(f"Error scanning tree for {owner}/{name}: {e}")
            
    if has_github_actions:
        detected_tech.add("github actions")
        
    # Scan files (limit package.json/requirements.txt fetches to max 3 per repo to be fast)
    pjs_count = 0
    req_count = 0
    
    for path in file_paths:
        filename = os.path.basename(path)
        filename_lower = filename.lower()
        
        # Check extensions / files
        if filename_lower == "package.json" and pjs_count < 3:
            pjs_count += 1
            if scanned_locally:
                try:
                    import json
                    with open(os.path.join(local_path, path), "r", encoding="utf-8", errors="ignore") as f:
                        pjs = json.load(f)
                        deps = {**pjs.get("dependencies", {}), **pjs.get("devDependencies", {})}
                        deps_lower = {k.lower(): v for k, v in deps.items()}
                        
                        if "react" in deps_lower: detected_tech.add("react")
                        if "next" in deps_lower: detected_tech.add("next.js")
                        if "tailwindcss" in deps_lower: detected_tech.add("tailwind css")
                        if "bootstrap" in deps_lower: detected_tech.add("bootstrap")
                        if "typescript" in deps_lower: detected_tech.add("typescript")
                        if "express" in deps_lower: detected_tech.add("express")
                        if "mongodb" in deps_lower: detected_tech.add("mongodb")
                        if "pg" in deps_lower or "postgres" in deps_lower: detected_tech.add("postgresql")
                        if "mysql" in deps_lower: detected_tech.add("mysql")
                        if "firebase" in deps_lower or "firebase-admin" in deps_lower: detected_tech.add("firebase")
                        if "vite" in deps_lower: detected_tech.add("vite")
                except Exception as e:
                    print(f"Error parsing local package.json: {e}")
            else:
                raw_url = f"https://raw.githubusercontent.com/{owner}/{name}/{branch}/{path}"
                try:
                    pjs_res = requests.get(raw_url, timeout=5)
                    if pjs_res.status_code == 200:
                        pjs = pjs_res.json()
                        deps = {**pjs.get("dependencies", {}), **pjs.get("devDependencies", {})}
                        deps_lower = {k.lower(): v for k, v in deps.items()}
                        
                        if "react" in deps_lower: detected_tech.add("react")
                        if "next" in deps_lower: detected_tech.add("next.js")
                        if "tailwindcss" in deps_lower: detected_tech.add("tailwind css")
                        if "bootstrap" in deps_lower: detected_tech.add("bootstrap")
                        if "typescript" in deps_lower: detected_tech.add("typescript")
                        if "express" in deps_lower: detected_tech.add("express")
                        if "mongodb" in deps_lower: detected_tech.add("mongodb")
                        if "pg" in deps_lower or "postgres" in deps_lower: detected_tech.add("postgresql")
                        if "mysql" in deps_lower: detected_tech.add("mysql")
                        if "firebase" in deps_lower or "firebase-admin" in deps_lower: detected_tech.add("firebase")
                        if "vite" in deps_lower: detected_tech.add("vite")
                except Exception as e:
                    print(f"Error parsing package.json in {owner}/{name}/{path}: {e}")
                    
        elif filename_lower == "requirements.txt" and req_count < 3:
            req_count += 1
            if scanned_locally:
                try:
                    with open(os.path.join(local_path, path), "r", encoding="utf-8", errors="ignore") as f:
                        req_text = f.read().lower()
                        if "numpy" in req_text: detected_tech.add("numpy")
                        if "pandas" in req_text: detected_tech.add("pandas")
                        if "scikit-learn" in req_text or "sklearn" in req_text: detected_tech.add("scikit-learn")
                        if "tensorflow" in req_text: detected_tech.add("tensorflow")
                        if "torch" in req_text or "pytorch" in req_text: detected_tech.add("pytorch")
                        if "xgboost" in req_text: detected_tech.add("xgboost")
                        if "lightgbm" in req_text: detected_tech.add("lightgbm")
                        if "catboost" in req_text: detected_tech.add("catboost")
                        if "opencv-python" in req_text or "opencv" in req_text or "cv2" in req_text: detected_tech.add("opencv")
                        if "matplotlib" in req_text: detected_tech.add("matplotlib")
                        if "seaborn" in req_text: detected_tech.add("seaborn")
                        if "flask" in req_text: detected_tech.add("flask")
                        if "fastapi" in req_text: detected_tech.add("fastapi")
                        if "firebase-admin" in req_text: detected_tech.add("firebase")
                        if "boto3" in req_text: detected_tech.add("aws")
                        if "jupyter" in req_text: detected_tech.add("jupyter")
                        if "prefect" in req_text: detected_tech.add("prefect")
                        if "evidently" in req_text: detected_tech.add("evidently")
                        if "pytest" in req_text: detected_tech.add("pytest")
                        if "scipy" in req_text: detected_tech.add("scipy")
                except Exception as e:
                    print(f"Error parsing local requirements.txt: {e}")
            else:
                raw_url = f"https://raw.githubusercontent.com/{owner}/{name}/{branch}/{path}"
                try:
                    req_res = requests.get(raw_url, timeout=5)
                    if req_res.status_code == 200:
                        req_text = req_res.text.lower()
                        if "numpy" in req_text: detected_tech.add("numpy")
                        if "pandas" in req_text: detected_tech.add("pandas")
                        if "scikit-learn" in req_text or "sklearn" in req_text: detected_tech.add("scikit-learn")
                        if "tensorflow" in req_text: detected_tech.add("tensorflow")
                        if "torch" in req_text or "pytorch" in req_text: detected_tech.add("pytorch")
                        if "xgboost" in req_text: detected_tech.add("xgboost")
                        if "lightgbm" in req_text: detected_tech.add("lightgbm")
                        if "catboost" in req_text: detected_tech.add("catboost")
                        if "opencv-python" in req_text or "opencv" in req_text or "cv2" in req_text: detected_tech.add("opencv")
                        if "matplotlib" in req_text: detected_tech.add("matplotlib")
                        if "seaborn" in req_text: detected_tech.add("seaborn")
                        if "flask" in req_text: detected_tech.add("flask")
                        if "fastapi" in req_text: detected_tech.add("fastapi")
                        if "firebase-admin" in req_text: detected_tech.add("firebase")
                        if "boto3" in req_text: detected_tech.add("aws")
                        if "jupyter" in req_text: detected_tech.add("jupyter")
                        if "prefect" in req_text: detected_tech.add("prefect")
                        if "evidently" in req_text: detected_tech.add("evidently")
                        if "pytest" in req_text: detected_tech.add("pytest")
                        if "scipy" in req_text: detected_tech.add("scipy")
                except Exception as e:
                    print(f"Error parsing requirements.txt in {owner}/{name}/{path}: {e}")
                    
        elif filename_lower == "cmakelists.txt" or filename_lower.endswith(".cmake"):
            detected_tech.add("cmake")
        elif filename_lower == "vercel.json":
            detected_tech.add("vercel")
        elif filename_lower.endswith(".ino") or filename_lower == "platformio.ini":
            detected_tech.add("arduino")
        elif filename_lower.endswith(".qmd") or filename_lower == "_quarto.yml":
            detected_tech.add("quarto")
        elif filename_lower.endswith(".tex"):
            detected_tech.add("latex")
        
        # Extension-based language detection
        if filename_lower.endswith((".py", ".ipynb")):
            if filename_lower.endswith(".py"):
                detected_tech.add("python")
            else:
                detected_tech.add("jupyter")
        elif filename_lower.endswith((".cpp", ".cc", ".cxx", ".h", ".hpp")):
            detected_tech.add("c++")
        elif filename_lower.endswith(".c"):
            detected_tech.add("c")
        elif filename_lower.endswith((".r", ".rmd")):
            detected_tech.add("r")
        elif filename_lower.endswith((".js", ".jsx")):
            detected_tech.add("javascript")
        elif filename_lower.endswith((".ts", ".tsx")):
            detected_tech.add("typescript")
        elif filename_lower.endswith((".html", ".htm")):
            detected_tech.add("html")
        elif filename_lower.endswith(".css"):
            detected_tech.add("css")
        elif filename_lower.endswith(".sql"):
            detected_tech.add("sql")
        elif filename_lower == "makefile" or filename_lower == "gnumakefile" or filename_lower.endswith(".mk"):
            detected_tech.add("makefile")
        elif filename_lower == "dockerfile" or filename_lower.endswith(".dockerfile") or filename_lower in ("docker-compose.yml", "docker-compose.yaml"):
            detected_tech.add("docker")
        elif filename_lower.endswith(".java"):
            detected_tech.add("java")
        elif filename_lower.endswith(".go"):
            detected_tech.add("go")
        elif filename_lower.endswith(".rs"):
            detected_tech.add("rust")
        elif filename_lower.endswith((".sh", ".bash")):
            detected_tech.add("shell")

print(f"Scan complete. Detected technologies: {list(detected_tech)}")

# Read README.md
with open("README.md", "r") as f:
    readme_content = f.read()

# Replace Projects Section
pattern_proj = r"<!-- START_SECTION:projects -->.*?<!-- END_SECTION:projects -->"
replacement_proj = f"<!-- START_SECTION:projects -->\n{projects_html}\n<!-- END_SECTION:projects -->"
readme_content = re.sub(pattern_proj, replacement_proj, readme_content, flags=re.DOTALL)

# Re-categorize and insert badges using skillicons.dev (square icons)
SKILL_ICONS_MAPPING = {
    "python": "py", "c++": "cpp", "cplusplus": "cpp", "c": "c", "r": "r",
    "javascript": "js", "js": "js", "typescript": "ts", "ts": "ts",
    "html": "html", "html5": "html", "css": "css", "css3": "css",
    "postgresql": "postgres", "postgres": "postgres", "sqlite": "sqlite", "mysql": "mysql", "sql": "mysql",
    "latex": "latex", "tex": "latex", "shell": "bash", "bash": "bash",
    "java": "java", "go": "go", "rust": "rust",
    "react": "react", "reactjs": "react", "next.js": "nextjs", "nextjs": "nextjs",
    "node.js": "nodejs", "nodejs": "nodejs", "flask": "flask", "fastapi": "fastapi",
    "express": "express", "expressjs": "express", "tailwind css": "tailwind", "tailwind": "tailwind",
    "bootstrap": "bootstrap", "vite": "vite", "arduino": "arduino", "django": "django",
    "pytorch": "pytorch", "tensorflow": "tensorflow", "scikit-learn": "sklearn", "sklearn": "sklearn",
    "opencv": "opencv",
    "firebase": "firebase", "aws": "aws", "vercel": "vercel", "mongodb": "mongodb", "heroku": "heroku",
    "git": "git", "github": "github", "github actions": "githubactions", "docker": "docker", "cmake": "cmake"
}

FALLBACK_ICONS = {
    "quarto": "md",
    "xgboost": "py",
    "lightgbm": "py",
    "catboost": "py",
    "prefect": "py",
    "evidently": "py",
    "pytest": "py",
    "makefile": "bash",
    "numpy": "py",
    "pandas": "py",
    "jupyter": "py",
    "jupyter notebook": "py"
}

def generate_category_table(cat_keys):
    cat_detected = []
    seen_display_names = set()
    
    for key in cat_keys:
        if key in detected_tech:
            display_name = TECH_DISPLAY_NAMES.get(key, key.capitalize())
            skill_id = SKILL_ICONS_MAPPING.get(key)
            if not skill_id:
                skill_id = FALLBACK_ICONS.get(key, "py")
            if display_name not in seen_display_names:
                seen_display_names.add(display_name)
                cat_detected.append((key, skill_id, display_name))
            
    if not cat_detected:
        return "<i>No technologies detected in this category yet.</i>"
        
    html = '<table>\n  <tr>\n'
    cols_per_row = 8
    
    for i, (tech, skill_id, display_name) in enumerate(cat_detected):
        if i > 0 and i % cols_per_row == 0:
            html += '  </tr>\n  <tr>\n'
            
        html += f'''    <td align="center" width="96" valign="top">
      <img src="https://skillicons.dev/icons?i={skill_id}" width="48" height="48" alt="{display_name}" /><br/>
      <sub><b>{display_name}</b></sub>
    </td>\n'''
        
    html += '  </tr>\n</table>'
    return html

# Generate and replace for each category
for cat_name, cat_keys in CATEGORIES.items():
    badges_html = generate_category_table(cat_keys)
    
    pattern_cat = f"<!-- START_SECTION:{cat_name} -->.*?<!-- END_SECTION:{cat_name} -->"
    replacement_cat = f"<!-- START_SECTION:{cat_name} -->\n{badges_html}\n<!-- END_SECTION:{cat_name} -->"
    readme_content = re.sub(pattern_cat, replacement_cat, readme_content, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(readme_content)

print("README.md updated successfully with dynamic projects and categorized large tech badges!")
