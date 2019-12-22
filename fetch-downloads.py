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
from itertools import islice

session = None

mapping = {
    "releases": "openttd-releases",
    "nightlies/trunk": "openttd-nightlies",
    "extra/openttd-useful": "openttd-useful",
}

# Current supported types on the new infrastructure
types = {
    "openttd-nightlies": "flatten",
    "openttd-releases": "stable-testing",
    "openttd-pullrequests": "name",
}

# If set, this category is limited to these amount of entries to generate HTML
# pages for. This is mostly done because nightlies for example are stored till
# the end of times, but generating HTML for every one of them is not useful.
# People that want a very old nightly can browse the archives directly.
limits = {
    "openttd-nightlies": 14,
}


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
        (version, date, folder) = version.split("\t", 2)

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

    entries = listing["params"]["param"]["value"]["struct"]["member"]
    if not isinstance(entries, list):
        entries = [entries]

    versions = []
    for entry in entries:
        # Check if this is a directory
        for value in entry["value"]["struct"]["member"]:
            if value["name"] == "type" and value["value"]["string"] == "directory":
                break
        else:
            continue

        versions.append(entry["name"])

    return versions


async def get_listing(folder):
    # We use the non-CDN URL here, as we want the latest; not any edge-cached version
    listing = await download(f"https://openttd.ams3.digitaloceanspaces.com/{folder}/listing.txt")

    versions = {}
    for entry in listing.decode().split("\n"):
        if not entry:
            continue

        version, date, name = entry.split(",", 3)
        versions[version] = (date, name)

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


async def handle_version(folder, dest_folder, version, host, on_old_infrastructure="false",
                         latest=None, latest_filenames=None):
    print(f"Adding {dest_folder}/{version} to downloads collection ..")
    manifest = await fetch_manifest(folder, version, host, on_old_infrastructure=on_old_infrastructure)

    # Insert the version into the header; otherwise we don't know
    # what version this was on the downloads page.
    manifest = manifest.split("\n")
    manifest.insert(1, f"version: {version}")
    manifest = "\n".join(manifest)

    await write_to_collection(dest_folder, version, manifest)

    # If this is the current version, also copy the content to "latest"
    if version == latest:
        if latest_filenames is None:
            latest_filenames = ["latest"]

        for latest_filename in latest_filenames:
            await write_to_collection(dest_folder, latest_filename, manifest)


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
        if type in limits:
            versions = versions[:limits[type]]

        for version in versions:
            await handle_version(
                folder,
                type,
                version,
                "https://binaries.openttd.org",
                on_old_infrastructure="true",
                latest=latest)

    # Support for new infrastructure; those are hosted on the DigitalOcean CDN (Spaces)
    for type, method in types.items():
        version_grouped = defaultdict(list)
        latest_grouped = defaultdict(lambda: ["", ""])
        versions = await get_listing(type)

        limit = limits.get(type)

        # Regroup the versions based on the method
        for version, data in islice(versions.items(), 0, limit):
            (date, name) = data

            if method == "flatten":
                index = None
            else:
                index = name

            version_grouped[index].append(version)
            if latest_grouped[index][0] < date:
                latest_grouped[index] = (date, version)

        # Now, based on the group, generate the files
        for index in version_grouped.keys():
            for version in version_grouped[index]:
                if method == "name":
                    dest_folder = f"{type}/{index}"
                else:
                    dest_folder = type

                if method == "stable-testing":
                    if index == "stable":
                        # Force 'latest' to always point to 'stable'
                        latest_filenames = ["latest"]
                    else:
                        latest_filenames = ["testing"]

                    # In case testing is older than stable, stable becomes the testing
                    if latest_grouped["testing"][0] < latest_grouped["stable"][0]:
                        if index == "stable":
                            latest_filenames.append("testing")
                        else:
                            latest_filenames = []
                else:
                    latest_filenames = ["latest"]

                os.makedirs(f"_downloads/{dest_folder}", exist_ok=True)
                await handle_version(
                    type,
                    dest_folder,
                    version,
                    "https://proxy.binaries.openttd.org",
                    latest=latest_grouped[index][1],
                    latest_filenames=latest_filenames)

    await session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
