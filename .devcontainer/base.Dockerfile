# This is a multi-stage Docker build

FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.8-bullseye as python

# Do nothing; we just use it to get data from this image.

FROM mcr.microsoft.com/vscode/devcontainers/ruby:0-2-bullseye

# Copy in the important parts of the Python image.
COPY --from=python /usr/local/ /usr/local/
# Cheat a little bit by adding the /usr/local/lib to the library searchpath.
# The original image uses /opt/ for this, but this requires a lot more work.
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/python.conf && ldconfig

# Install all Gems, as installing takes a long time.
COPY Gemfile \
     Gemfile.lock \
     /tmp/gem-tmp/
RUN gem update && bundle install --gemfile=/tmp/gem-tmp/Gemfile && rm -rf /tmp/gem-tmp

# Customized first-run-notice to give clues how to work with this devcontainer.
COPY .devcontainer/first-run-notice.txt /usr/local/etc/vscode-dev-containers/first-run-notice.txt
