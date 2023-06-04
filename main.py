import os
from git import Repo

COMMITS_TO_PRINT=2

def print_commit(commit):
    print('-----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str("count: {} and size: {}".format(commit.count(),
                                              commit.size)))
    
def print_repository(repo):
    print('Repo descriptionL {}'.format(repo.description))
    print('Repo active branch is {}'.format(repo.active_branch))
    for remote in repo.remotes:
        print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
    print('Last commit for repo is {}'.format(str(repo.head.commit.hexsha)))

def get_commit_contents(commit):

    try:
        commit_contents = {}

        # Retrieve commit message
        commit_contents['message'] = commit.message

        # Retrieve file changes
        changes = commit.diff()

        file_changes = []
        for change in changes:
            file_change = {}

            # Retrieve file path
            file_change['path'] = change.a_path

            print(f"{change.a_blob}")
            # Retrieve file content
            file_content = change.a_blob.data_stream.read().decode('utf-8')
            file_change['content'] = file_content

            file_changes.append(file_change)

        commit_contents['file_changes'] = file_changes

        return commit_contents

    except Exception as e:
        print(f"Error retrieving commit contents: {e}")



if __name__ == "__main__":
    repo_path = os.getenv('GIT_REPO_PATH')
    # Repo object used to programmatically interact with Git repositories
    repo = Repo(repo_path)
    # check that the repository loaded correctly
    if not repo.bare:
        print('Repo at {} successfully loaded'.format(repo_path))
        print_repository(repo)
        # create list of commits then print some of them to stdout
        commits = list(repo.iter_commits('main'))[:COMMITS_TO_PRINT]
        for commit in commits:
            print_commit(commit)

            commit_contents = get_commit_contents(commit)

            # Print commit message
            print(f"Commit Message: {commit_contents['message']}")

            # Print file changes
            print("printing changes...")
            for change in commit_contents['file_changes']:
                print(f"File Path: {change['path']}")
                print(f"File Content:\n{change['content']}\n")
            pass
    else:
        print('Could not load repository at {}'.format(repo_path))