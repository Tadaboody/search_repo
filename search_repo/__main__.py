import argparse
import asyncio
import enum
import os
import sys
import typing

import aiohttp

USE_HTTPS_VARIABLE = "SEARCH_REPO_USE_HTTPS"


class Repository(typing.NamedTuple):
    name: str
    author: str
    stars: int
    provider: str

    def to_link(self, https: bool) -> str:
        full_name = f"{self.author}/{self.name}"
        if https:
            return f"https://{self.provider}/{full_name}"
        return f"git@{self.provider}:{full_name}"

    @classmethod
    def from_github_json(cls, json: typing.Dict):
        return cls(
            name=json["name"],
            author=json["owner"]["login"],
            stars=int(json["stargazers_count"]),
            provider="github.com",
        )


async def get_repo(repo_name: str, language: str) -> typing.List[Repository]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.github.com/search/repositories",
            params={
                "q": f"{repo_name} language:{language}",
                "sort": "stars",
                "order": "desc",
            },
        ) as resp:
            github_response = await resp.json()
    return [Repository.from_github_json(json) for json in github_response["items"]]


def parse_args(argv: typing.List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find the most matching repository")
    parser.add_argument("name")
    parser.add_argument(
        "--language",
        help="Programming language to filter by.",
    )
    parser.add_argument(
        "--https",
        action="store_true",
        help=f"Output an http clone link, can also be toggled by defining {USE_HTTPS_VARIABLE}",
    )
    return parser.parse_args(argv[1:])


def main():
    args = parse_args(sys.argv)
    repos = asyncio.run(get_repo(args.name, args.language))
    if not repos:
        print("No repos match the query", file=sys.stderr)
        return 1
    best_match = max(repos, key=lambda repo: repo.stars)
    print(best_match.to_link(https=args.https or (USE_HTTPS_VARIABLE in os.environ)))
    return 0


if __name__ == "__main__":
    main()
