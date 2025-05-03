import os
import traceback

from subprocess import Popen, PIPE
from pathlib import Path
from typing import Optional, Union
from github import Github, Auth
from dotenv import load_dotenv


load_dotenv()  # take environment variables


def parse_input() -> dict:
    gh_input = {
        "username": "Scientific-Python-Translations",
        # Provided by organization secrets
        "token": os.environ["TOKEN"],
        # Provided by user action input
        "translations_repo": os.environ["INPUT_TRANSLATIONS-REPO"],
        "translations_ref": os.environ["INPUT_TRANSLATIONS-REF"],
        # Provided by gpg action based on organization secrets
        "name": os.environ["GPG_NAME"],
        "email": os.environ["GPG_EMAIL"],
        "run_local": os.environ.get("RUN_LOCAL", "False").lower() == "true",
    }
    return gh_input


def run(
    cmds: list[str], cwd: Optional[Union[str, Path]] = None
) -> tuple[str, str, int]:
    """Run a command in the shell and print the standard output, error and return code.

    Parameters
    ----------
    cmds : list
        List of commands to run.
    cwd : str, optional
        Current working directory to run the command in. If None, use the current working directory.

    Returns
    -------
    out : str
        Output of the command.
    err : str
        Error of the command.
    rc : int
        Return code of the command.
    """
    p = Popen(cmds, stdout=PIPE, stderr=PIPE, cwd=cwd)
    out, err = p.communicate()
    stdout = out.decode()
    stderr = err.decode()
    print("\n\n\nCmd: \n" + " ".join(cmds))
    print("Cwd: \n", cwd or os.getcwd())
    print("Out: \n", stdout)
    print("Err: \n", stderr)
    print("Code: \n", p.returncode)
    return stdout, stderr, p.returncode


def configure_git_and_checkout_repos(
    username: str,
    token: str,
    translations_repo: str,
    translations_ref: str,
    name: str,
    email: str,
) -> None:
    """
    Configure git information and checkout repositories.

    Parameters
    ----------
    username : str
        Username of the source repository.
    token : str
        Personal access token of the source repository.
    translations_repo : str
        .
    translations_ref : str
        .
    name : str
        Name of the bot account.
    email : str
        Email of the bot account.
    """
    os.environ["GITHUB_TOKEN"] = token
    print("\n\n### Configure git information and checkout repositories")

    base_path = Path(os.getcwd())
    base_translations_path = base_path / translations_repo.split("/")[-1]

    print("\n\nBase path:\n", base_path)
    print("\n\nBase translations path:\n", base_translations_path)

    if translations_ref:
        cmds = [
            "git",
            "clone",
            "-b",
            translations_ref,
            f"https://{username}:{token}@github.com/{translations_repo}.git",
        ]
    else:
        cmds = [
            "git",
            "clone",
            f"https://{username}:{token}@github.com/{translations_repo}.git",
        ]

    run(cmds, cwd=base_path)

    # Configure git information
    for path in [base_translations_path]:
        run(["git", "config", "user.name", f'"{name}"'], cwd=path)
        run(["git", "config", "user.email", f'"{email}"'], cwd=path)


def clean_up_branches(
    token: str,
    translations_repo: str,
):
    """
    Clean up branches in the translations repository.

    Parameters
    ----------
    token : str
        Personal access token of the source repository.
    translations_repo : str
        Translations repository name.
    """
    base_path = Path(os.getcwd())
    base_translations_path = base_path / translations_repo.split("/")[-1]

    auth = Auth.Token(token)
    g = Github(auth=auth)
    branches = g.get_repo(translations_repo).get_branches()
    branch_names = [branch.name for branch in branches]
    branch_names.remove("main")
    for branch in branch_names:
        if branch.startswith(
            ("content-sync-", "l10n_main", "add/translators-file", "add/status-file")
        ):
            print(f"### Deleting branch {branch}")
            run(["git", "branch", "-d", branch], cwd=base_translations_path)
            run(
                ["git", "push", "origin", "--delete", branch],
                cwd=base_translations_path,
            )


def main() -> None:
    """Main function to run the script."""
    try:
        gh_input = parse_input()
        configure_git_and_checkout_repos(
            username=gh_input["username"],
            token=gh_input["token"],
            translations_repo=gh_input["translations_repo"],
            translations_ref=gh_input["translations_ref"],
            name=gh_input["name"],
            email=gh_input["email"],
        )
        clean_up_branches(
            token=gh_input["token"],
            translations_repo=gh_input["translations_repo"],
        )
    except Exception as e:
        print("Error: ", e)
        print(traceback.format_exc())
        raise e


if __name__ == "__main__":
    main()
