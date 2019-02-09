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
import os
import xmltodict

from collections import defaultdict

session = None

mapping = {
    "releases": "openttd-releases",
    "nightlies/trunk": "openttd-nightlies",
    "extra/openttd-useful": "openttd-useful",
}

# Current supported types on the new infrastructure
types = [
    "openttd-nightlies",
    "openttd-releases",
]
types_grouped_by_branch = [
    "openttd-pullrequests",
]


async def download(url):
    async with session.get(url) as response:
        if response.status != 200:
            raise Exception("URL didn't return 200", url)
        return await response.read()


async def get_old_download_folders():
    versions = await download("https://finger.openttd.org/versions.txt")
    versions = versions.decode().strip().split("\n")

    folders = {}
    for version in versions:
        (version, date, folder) = version.split('\t', 2)

        # Do not process custom entries
        if folder.startswith("custom/"):
            continue

        # grfcodec-trunk had two aliases; only process one
        if folder in ("extra/nforenum-nightly", "extra/grfcodec-nightly"):
            continue

        # releases\tstable already covers openttd-releases
        if folder == "releases\ttesting":
            continue
        if folder == "releases\tstable":
            folder = "releases"

        # Try to map the entry as good as we possibly can to the new naming schema
        if folder in mapping:
            type = mapping[folder]
        elif folder.endswith("-trunk"):
            type = folder[:-6] + "-nightlies"
        elif folder.endswith("-nightly"):
            type = folder[:-8] + "-nightlies"
        else:
            type = folder + "-releases"

        # Remove the extra prefix
        if type.startswith("extra/"):
            type = type[6:]

        folders[folder] = (type, version)

    return folders


async def get_old_versions_of_folder(folder):
    listing = await download(f"https://binaries.openttd.org/{folder}/index.xml")
    listing = xmltodict.parse(listing.decode())

    entries = listing['params']['param']['value']['struct']['member']
    if not isinstance(entries, list):
        entries = [entries]

    versions = []
    for entry in entries:
        # Check if this is a directory
        for value in entry['value']['struct']['member']:
            if value['name'] == 'type' and value['value']['string'] == 'directory':
                break
        else:
            continue

        versions.append(entry['name'])

    return versions


async def get_latest(folder):
    # We use the non-CDN URL here, as we want the latest; not any edge-cached version
    latest = await download(f"https://openttd.ams3.digitaloceanspaces.com/{folder}/latest.txt")
    latest = latest.decode()

    version, _, date = latest.partition(",")
    return version


async def get_listing(folder):
    # We use the non-CDN URL here, as we want the latest; not any edge-cached version
    listing = await download(f"https://openttd.ams3.digitaloceanspaces.com/{folder}/listing.txt")

    versions = {}
    for entry in listing.decode().split("\n"):
        if not entry:
            continue

        version, _, date = entry.partition(",")
        versions[version] = date

    return versions


async def fetch_manifest(folder, version, host, on_old_infrastructure="false"):
    manifest = await download(f"{host}/{folder}/{version}/manifest.yaml")
    manifest = manifest.decode()

    manifest = manifest.split("\n")
    manifest.insert(1, f"on_old_infrastructure: {on_old_infrastructure}")
    manifest.insert(1, f"host: {host}")
    manifest = "\n".join(manifest)

    return manifest


async def write_to_collection(type, version, manifest):
    with open(f"_downloads/{type}/{version}.md", "wb") as f:
        f.write("---\n".encode())
        f.write(manifest.encode())
        f.write("---\n".encode())


async def handle_version(folder, type, version, host, on_old_infrastructure="false", latest=None):
    print(f"Adding {type}/{version} to downloads collection ..")
    manifest = await fetch_manifest(folder, version, host, on_old_infrastructure=on_old_infrastructure)
    await write_to_collection(type, version, manifest)

    # If this is the current version, also copy the content to "latest"
    if version == latest:
        # Insert the version into the header; otherwise we don't know
        # what version this was on the downloads page.
        manifest = manifest.split("\n")
        manifest.insert(1, f"version: {version}")
        manifest = "\n".join(manifest)
        await write_to_collection(type, "latest", manifest)


async def main():
    global session

    os.makedirs("_downloads", exist_ok=True)
    session = aiohttp.ClientSession()

    # Support for old infrastructure; those are hosted on the old mirror network
    folders = await get_old_download_folders()
    for folder, data in folders.items():
        type, latest = data

        os.makedirs(f"_downloads/{type}", exist_ok=True)

        versions = await get_old_versions_of_folder(folder)
        # For the nightlies, only generate the first 90; the real list is 4000+
        if type == "openttd-nightlies":
            versions = versions[:90]

        for version in versions:
            await handle_version(
                folder,
                type,
                version,
                "https://binaries.openttd.org",
                on_old_infrastructure="true",
                latest=latest)

    # Support for new infrastructure; those are hosted on the DigitalOcean CDN (Spaces)
    for type in types:
        latest = await get_latest(type)
        versions = await get_listing(type)
        for version, data in versions.items():
            os.makedirs(f"_downloads/{type}", exist_ok=True)
            await handle_version(
                type,
                type,
                version,
                "https://proxy.binaries.openttd.org",
                latest=latest)

    for type in types_grouped_by_branch:
        version_grouped = defaultdict(list)
        latest_grouped = defaultdict(str)
        versions = await get_listing(type)

        # Regroup the versions based on the branch (which is the second part in the name)
        for version, data in versions.items():
            (date, branch, tag) = version.split("-", 3)

            version_grouped[branch].append((version, data))
            if latest_grouped[branch] < date:
                latest_grouped[branch] = version

        # Now, based on the group, generate the files
        for branch in version_grouped.keys():
            for version, data in version_grouped[branch]:
                os.makedirs(f"_downloads/{type}/{branch}", exist_ok=True)
                await handle_version(
                    type,
                    f"{type}/{branch}",
                    version,
                    "https://proxy.binaries.openttd.org",
                    latest=latest_grouped[branch])

    await session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
