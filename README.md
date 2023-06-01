# OpenTTD's website

[![GitHub License](https://img.shields.io/github/license/OpenTTD/website)](https://github.com/OpenTTD/website/blob/main/LICENSE)

This is the main website for OpenTTD, as can be seen on [https://www.openttd.org/](https://www.openttd.org/).
`main` is always deployed on [production](https://www.openttd.org/).
Pull Request can be reviewed on their preview URL.

This is a [Jekyll](https://jekyllrb.com/) website, and is served by nginx as a static site.

## Development

### Populating _downloads

By default `_downloads` is empty, so when building the website locally there is no latest stable/nightly.
This can be resolved by running `fetch_downloads`.
This script will download the latest available binaries, and populate `_downloads`.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m fetch_downloads
```

### Running a local server

If you do not want to run a server, but just build the current site, replace `serve` with `build` in the examples below.

Under `_site` Jekyll will put the compiled result in both `serve` and `build`.

- Follow [jekyll installation](https://jekyllrb.com/docs/installation/)
- Run `bundle install`
- Run `JEKYLL_ENV=production jekyll serve`

## FAQ

### I want to make a new blog post

- Create a new file in _posts.
- Follow the existing format.
- Make a Pull Request.
  It will automatically be published on a preview website for you to see the result.
- Get it approved, squash/rebase it to `main`.
  `main` is automatically deployed to [production](https://www.openttd.org/).

### I get an error about ua-parser.js while building

Please set `JEKYLL_ENV` to `production`.
Without this, the symlink `ua-parser.js` is copied, instead of following it.
With `production` it does the right thing.
To recover, remove `_site/static/js/ua-parser.js` manually.

### What is this download-descriptions.yml

On download pages, you notice that every binary has a human readable description.
`windows-win64.exe` is for most people to cryptic.
`Windows XP / Vista / 7 / 8 / 10 (64bit) (installer)` is much more clear.
This file takes care of that mapping, based on the postfix of the file.

### Why the downloads?

Because this is a static website, but we do want to show in the header what the latest version is, we need to find a solution.
We picked a solution where we fetch some files to know what the latest version is, and create a static version out of it.
This means that every time the latest version changes, the website has to be recreated.
As new versions are rare (once or sometimes twice a day at most), it is very cheaper to do it this way.
It avoids any dynamic component in production.

### Screenshots in a git repository?

Yes.
By lack of better, we are doing this.
