import json
from github import Github

workflow_files = ('pylint.yml', 'pytest.yml')
file_name = 'names.json'
user_github_pseudo = "Charon1449"
repo_name = 'Scrapping_demo443'
repo_description = "skill tool test description"
access_token = "7878"


def create_workflows(workflow_files, repo):
    for workflow in workflow_files:
        workflow_path = '.github/workflows/' + workflow
        repo.create_file(workflow_path, "adding workflow", open(workflow).read())


def add_collaborators(file_name, repo):
    json_data = json.loads(open(file_name).read())
    for condidat in json_data:
        repo.add_to_collaborators(condidat['Github'], "push")


def create_branchs(file_name, repo):
    json_data = json.loads(open(file_name).read())
    source_branch = 'main'
    for condidat in json_data:
        target_branch = "branch_of_" + condidat['Name'].replace(' ', '_')
        sb = repo.get_branch(source_branch)
        repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)


g = Github(access_token)
user = g.get_user()
repo = g.get_repo(user_github_pseudo + '/' + repo_name )

# repo = user.create_repo(repo_name, private=False, description=repo_description)
# create_workflows(workflow_files, repo)
# add_collaborators(file_name, repo)
# create_branchs(file_name, repo)

print("Repo name : " + repo.name)
print("Owner : " + user.name)
print("Pending invitations :")
users = repo.get_pending_invitations()
for pending in users:
    print("     *Github pseudo : " + pending.invitee.login + '  Name : ' + str(pending.invitee.name) )
print("Branch list :")
for branch in list(repo.get_branches()): print("     -" + branch.name)
