"""
This script populates the 'downloads' collection by looking firstly at
finger.openttd.org what is currently published. After that it uses
the index and manifest files on binaries.openttd.org to create all the
needed markdown files in the 'downloads' collection.

After running this script, you can run Jekyll, and all the download pages
will work with the latest representation of what is available.
"""

import aiohttp
import asyncio
import pathlib
import yaml

from collections import defaultdict

session = None


async def download(url):
    async with session.get(url) as response:
        if response.status != 200:
            raise Exception("URL didn't return 200", url)
        return await response.read()


async def get_versions():
    latest_raw = await download("https://cdn.openttd.org/latest.yaml")
    latest = yaml.safe_load(latest_raw)
    return latest["latest"]


async def fetch_manifest(folder, version):
    manifest = await download(f"https://cdn.openttd.org/{folder}/{version}/manifest.yaml")
    return manifest.decode()


async def write_to_collection(folder, local_folder, name, manifest):
    with open(f"_downloads/{local_folder}/{name}.md", "wb") as f:
        f.write("---\n".encode())
        f.write(f"folder: {folder}\n".encode())
        f.write(manifest.encode())
        f.write("---\n".encode())


async def handle_version(folder, local_folder, version, name=None):
    print(f"Adding {local_folder}/{version} to downloads collection ..")
    manifest = await fetch_manifest(folder, version)

    if name is None:
        name = "latest"

    pathlib.Path(f"_downloads/{local_folder}").mkdir(parents=True, exist_ok=True)
    await write_to_collection(folder, local_folder, name, manifest)


async def main():
    global session

    session = aiohttp.ClientSession()

    versions = await get_versions()

    grouped_versions = defaultdict(list)
    for version in versions:
        grouped_versions[version["folder"]].append(version)

    for _, versions in grouped_versions.items():
        for version in versions:
            name = version["name"]
            if name != "testing":
                name = "latest"

            local_folder = version["folder"]
            # openttd-nightlies is a "per-year" folder, so remove the year.
            if local_folder.startswith("openttd-nightlies"):
                local_folder = "openttd-nightlies"

            await handle_version(
                folder=version["folder"],
                local_folder=local_folder,
                version=version["version"],
                name=name,
            )

    await session.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
