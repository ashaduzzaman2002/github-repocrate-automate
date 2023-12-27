import requests
import base64

# Replace these variables with your own values
github_token = 'your-access-token'
organization_name = 'organization-name'
figma_files = ['figma_file5', 'figma_file6',]
project_names = ['project1', 'project2']
github_accounts = ['pawan-pareek-1', 'ProgrammerAlok' ]

# Create repositories and grant access
for index, (figma_file, github_account, project_name) in enumerate(zip(figma_files, github_accounts, project_names), start=1):
    # Create repository
    # repo_name = f'{project_name}_{github_account}_{index}'
    repo_name = f'techX_project_{index}'
    create_repo_url = f'https://api.github.com/orgs/{organization_name}/repos'
    repo_data = {'name': repo_name, 'private': True}
    
    response = requests.post(create_repo_url, json=repo_data, headers={'Authorization': f'token {github_token}'})
    
    if response.status_code != 201:
        print(f"Failed to create repository {repo_name}: {response.text}")
        continue
    
    print(f"Repository {repo_name} created successfully.")
    
    # Grant write access
    add_collaborator_url = f'https://api.github.com/repos/{organization_name}/{repo_name}/collaborators/{github_account}'
    access_data = {'permission': 'write'}
    
    response = requests.put(add_collaborator_url, json=access_data, headers={'Authorization': f'token {github_token}'})
    
    if response.status_code == 204:
        print(f"Write access granted to {github_account} for repository {repo_name}.")
    else:
        print(f"Failed to grant write access to {github_account} for repository {repo_name}: {response.text}")

    # Create README.md file
    readme_content = f"# TechX Project Setup\n\n" \
                 f"## Instructions\n\n" \
                 f"1. Clone this repository: `git clone https://github.com/{organization_name}/{repo_name}.git`\n" \
                 f"## Figma Link\n\n" \
                 f"Figma Link: `{figma_file}`"


    readme_url = f'https://api.github.com/repos/{organization_name}/{repo_name}/contents/README.md'
    readme_content_bytes = readme_content.encode('utf-8')
    readme_content_base64 = base64.b64encode(readme_content_bytes).decode('utf-8')
    readme_data = {
    'message': f'Initial commit for {repo_name}',
    'content': readme_content_base64,
    'branch': 'main'
    }

    response = requests.put(readme_url, json=readme_data, headers={'Authorization': f'token {github_token}'})

   



    
    if response.status_code == 200:
        print(f"README.md created successfully for repository {repo_name}.")
    else:
        print(f"Failed to create README.md for repository {repo_name}: {response.text}")
