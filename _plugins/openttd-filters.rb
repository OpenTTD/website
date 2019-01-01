module Jekyll
    module OpenTTDFilters

        # Code taken from (and slightly modified)
        # https://github.com/jekyll-octopod/jekyll-octopod/blob/master/lib/jekyll/octopod_filters.rb
        # jekyll-octopod is licensed under MIT.
        def string_of_size(bytes)
            bytes = bytes.to_i.to_f
            out = '0'
            return out if bytes == 0.0

            jedec = %w[b K M G]
            [3, 2, 1, 0].each { |i|
                if bytes > 1024 ** i
                    out = "%.1f #{jedec[i]}iB" % (bytes / 1024 ** i)
                    break
                end
            }

            return out
        end

        # Code taken from
        # http://talk.jekyllrb.com/t/how-to-properly-indicate-an-error-during-site-generation/447
        # Unlicensed; appears to be free to use.
        def raise_error(msg)
            bad_file = @context.registers[:page]['path']
            err_msg = "On #{bad_file}: #{msg}"
            raise err_msg
        end
    end
end

Liquid::Template.register_filter(Jekyll::OpenTTDFilters)
