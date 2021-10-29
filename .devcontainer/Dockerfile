ARG VARIANT=2-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/ruby:0-${VARIANT}

ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Install all Gems, as installing takes a long time.
COPY Gemfile \
     Gemfile.lock \
     /tmp/gem-tmp/
RUN gem update && bundle install --gemfile=/tmp/gem-tmp/Gemfile && rm -rf /tmp/gem-tmp

# Customized first-run-notice to give clues how to work with this devcontainer.
COPY .devcontainer/first-run-notice.txt /usr/local/etc/vscode-dev-containers/first-run-notice.txt

# There is not a way to change the location of the default Python interpreter.
# So instead, we symlink the right path to the default one GitHub Codespaces expects.
RUN ln -s /usr/local/python/bin/python /usr/local/bin/python
