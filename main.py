import gitlab
import os

# GitLab private token and project information
PRIVATE_TOKEN = 'private-token-here'
GITLAB_URL = 'https://repo1.dso.mil/'
PROJECT_ID = 'big-bang/bigbang'  # Replace with your project's ID or path
GROUP_ID = 3988

# Directory to save the downloaded files
MD_OUTPUT_DIR = 'md_files'
EPIC_OUTPUT_DIR = 'epic_files'

def download_md_files(gl, project_id):
    project = gl.projects.get(project_id)
    
    md_files = project.repository_tree(recursive=True, ref='master', get_all=True)
    for file in md_files:
        if file['type'] == 'blob' and file['path'].endswith('.md'):
            file_content = project.files.raw(file_path=file['path'], ref='master')
            file_name = os.path.basename(file['path'])
            file_path = os.path.join(MD_OUTPUT_DIR, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as f:
                f.write(file_content)

            print(f'Downloaded: {file_path}')
    

def download_epics(gl, group_id):
    epics = gl.groups.get(group_id).epics.list(get_all=True)

    for epic in epics:
        file_name = os.path.basename("epic_%i" % epic.id)
        file_path = os.path.join(EPIC_OUTPUT_DIR, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        issues = epic.issues.list(get_all=True)
        with open(file_path, 'w') as file:
            file.write(f'start date: %s\n' % epic.start_date)
            file.write(f'due date: %s\n' % epic.due_date)
            file.write(f'epic description: %s\n' % epic.description)

            for issue in issues:
                file.write(f'issue description: %s\n' % issue.description)


if __name__ == "__main__":
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)
    download_md_files(gl, PROJECT_ID)
    download_epics(gl, GROUP_ID)