# This is a multi-stage Docker build

# Build the HTML from the source
FROM alpine as html

WORKDIR /source/

# Copy the Gemfiles, so the dependencies can be installed correctly
COPY Gemfile Gemfile.lock /source/

RUN apk --no-cache add \
        build-base \
        ruby \
        ruby-dev \
    && gem update --no-document --system \
    && gem install --no-document \
        bigdecimal \
        json \
        -- --use-system-libraries \
    && bundle install \
    && apk --no-cache del \
        build-base \
        ruby-dev

COPY . /source/

RUN mkdir /html \
    && jekyll build -s /source -d /html

# Copy the HTML and serve it via nginx
FROM nginx:alpine
COPY --from=html /html/ /usr/share/nginx/html/
