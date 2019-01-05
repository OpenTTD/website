# This is a multi-stage Docker build

# Create the downloads collection
FROM python:3.6-alpine as collection

WORKDIR /source/

COPY . /source/
RUN pip install -r requirements.txt
# Validate that what was installed was what was expected
RUN pip freeze 2>/dev/null | grep -v "deployer" > requirements.installed \
        && diff -u requirements.txt requirements.installed 1>&2 \
        || ( echo "!! ERROR !! requirements.txt defined different packages or versions for installation" \
                && exit 1 ) 1>&2
RUN pip install flake8

COPY .flake8 .flake8
RUN flake8 fetch-downloads.py

RUN python fetch-downloads.py

# Build the HTML from the source
FROM alpine as html

WORKDIR /source/

# Copy the Gemfiles, so the dependencies can be installed correctly
COPY Gemfile Gemfile.lock /source/

RUN apk --no-cache add \
        build-base \
        ruby \
        ruby-bigdecimal \
        ruby-dev \
        ruby-json \
        ruby-rdoc \
    && echo "gem: --no-ri --no-rdoc --no-document" > ~/.gemrc \
    && gem update --system \
    && gem install http_parser.rb -v 0.6.0 -- --use-system-libraries \
    && gem install safe_yaml -v 1.0.4 -- --use-system-libraries \
    && bundle install \
    && apk --no-cache del \
        build-base \
        ruby-dev

COPY . /source/
COPY --from=collection /source/_downloads /source/_downloads

RUN mkdir /html \
    && jekyll build --strict_front_matter -s /source -d /html

# Copy the HTML and serve it via nginx
FROM nginx:alpine
COPY --from=html /html/ /usr/share/nginx/html/
COPY nginx.default.conf /etc/nginx/conf.d/default.conf
