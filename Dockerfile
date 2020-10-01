# website-1
# This is a multi-stage Docker build

# Create the downloads collection
FROM python:3.8-slim as collection

WORKDIR /source/

COPY . /source/

RUN pip --no-cache-dir install -r requirements.txt

# Validate that what was installed was what was expected
RUN pip freeze 2>/dev/null > requirements.installed \
        && diff -u --strip-trailing-cr requirements.txt requirements.installed 1>&2 \
        || ( echo "!! ERROR !! requirements.txt defined different packages or versions for installation" \
                && exit 1 ) 1>&2

RUN python -m fetch_downloads

# Build the HTML from the source
FROM alpine as html

WORKDIR /source/

# Copy the Gemfiles, so the dependencies can be installed correctly
COPY Gemfile Gemfile.lock /source/

RUN apk --no-cache add \
        build-base \
        libstdc++ \
        ruby \
        ruby-bigdecimal \
        ruby-dev \
        ruby-json \
        ruby-rdoc \
    && echo "gem: --no-ri --no-rdoc --no-document" > ~/.gemrc \
    && gem update --system \
    && bundle update --bundler \
    && bundle install \
    && apk --no-cache del \
        build-base \
        ruby-dev

COPY . /source/
COPY --from=collection /source/_downloads /source/_downloads

RUN mkdir /html \
    && JEKYLL_ENV=production jekyll build --strict_front_matter -s /source -d /html

# Copy the HTML and serve it via nginx
FROM nginx:alpine

ARG BUILD_DATE=""
ARG BUILD_VERSION="dev"

LABEL maintainer="OpenTTD Dev Team <info@openttd.org>"
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.authors="OpenTTD Dev Team <info@openttd.org>"
LABEL org.opencontainers.image.url="https://github.com/OpenTTD/website"
LABEL org.opencontainers.image.source="https://github.com/OpenTTD/website"
LABEL org.opencontainers.image.version=${BUILD_VERSION}
LABEL org.opencontainers.image.licenses="GPLv2"
LABEL org.opencontainers.image.title="OpenTTD's website in Jekyll"
LABEL org.opencontainers.image.description="his is the main website for OpenTTD, as can be seen on https://www.openttd.org/."

COPY --from=html /html/ /usr/share/nginx/html/
RUN sed -i 's/access_log/# access_log/g' /etc/nginx/nginx.conf
COPY nginx.default.conf /etc/nginx/conf.d/default.conf
