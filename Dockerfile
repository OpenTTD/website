# This is a multi-stage Docker build

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

RUN mkdir /html \
    && jekyll build --strict_front_matter -s /source -d /html

# Copy the HTML and serve it via nginx
FROM nginx:alpine
COPY --from=html /html/ /usr/share/nginx/html/
