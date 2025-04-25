import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USER = os.getenv('GITHUB_USER')
REPO_NAME = os.getenv('REPO_NAME', f"test-repo-{int(time.time())}")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def create_repo():
    """Создание репозитория"""
    response = requests.post(
        "https://api.github.com/user/repos",
        json={
            "name": REPO_NAME,
            "auto_init": True
        },
        headers=headers
    )
    assert response.status_code == 201, f"Failed to create repo: {response.json()}"
    print(f"Репозиторий {REPO_NAME} создан!")


def check_repo_exists():
    """Проверка списка репозиториев для подтверждения создания"""
    response = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}/repos",
        headers=headers
    )
    repos = [repo["name"] for repo in response.json()]
    assert REPO_NAME in repos, "Репозиторий не найден в списке!"
    print("Репозиторий найден в списке.")


def delete_repo():
    """Deletes the repository."""
    response = requests.delete(
        f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}",
        headers=headers
    )
    assert response.status_code == 204, "Ошибка удаления!"
    print("Репозиторий успешно удален.")


if __name__ == "__main__":
    create_repo()
    check_repo_exists()
    delete_repo()
