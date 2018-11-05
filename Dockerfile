FROM nginx:alpine

WORKDIR /workdir

# Copy the Gemfiles, so the dependencies can be installed correctly
COPY Gemfile Gemfile.lock /workdir/

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

# Copy the rest of Jekyll files
COPY \
    *.html \
    *.md \
    *.yml \
    _layouts \
    _posts \
    /workdir/

COPY scripts/startup.sh /usr/bin/startup

ENTRYPOINT ["startup"]
CMD []

