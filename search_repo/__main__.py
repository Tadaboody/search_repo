import argparse
import asyncio
import enum
import sys
import typing

import aiohttp


class Repository(typing.NamedTuple):
    name: str
    author: str
    stars: int
    provider: str
    fork: bool

    class UrlForm(enum.Enum):
        SSH = "ssh"
        HTTPS = "http"
        SHORTENED = "shortened"

    def get_link(self, form: "Repository.UrlForm") -> str:
        full_name = f"{self.author}/{self.name}"
        return {
            self.UrlForm.SSH: f"git@{self.provider}:{full_name}",
            self.UrlForm.HTTPS: f"https://{self.provider}/{full_name}",
            self.UrlForm.SHORTENED: f"{self.provider}:{full_name}",
        }[form]

    @classmethod
    def from_github_json(cls, json: typing.Dict):
        return cls(
            name=json["name"],
            author=json["owner"]["login"],
            stars=int(json["stargazers_count"]),
            provider="github.com",
            fork=json["fork"],
        )


async def get_repo(repo_name: str) -> Repository:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.github.com/search/repositories",
            params={"q": repo_name, "sort": "stars", "order": "desc"},
        ) as resp:
            github_response = await resp.json()
    github_repos: typing.List[Repository] = [
        Repository.from_github_json(json) for json in github_response["items"]
    ]
    return max(github_repos, key=lambda repo: repo.stars)


def parse_args(argv: typing.List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find the most matching repository")
    parser.add_argument("name")
    parser.add_argument(
        "--form",
        choices=[form.name.lower() for form in Repository.UrlForm],
        default="ssh",
    )
    return parser.parse_args(argv[1:])


def main():
    args = parse_args(sys.argv)
    res = asyncio.run(get_repo(args.name))
    print(res.get_link(Repository.UrlForm[args.form.upper()]))


if __name__ == "__main__":
    main()
