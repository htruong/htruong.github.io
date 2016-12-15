  require 'nokogiri'
  require 'fastimage'
  require 'fastimage_resize'
  require 'digest'
  require 'fileutils'

  module Jekyll
    module AmpFilter
      # Filter for HTML 'img' elements.
      # Converts elements to 'amp-img' and adds additional attributes
      # Parameters:
      #   input       - the content of the post
      #   responsive  - boolean, whether to add layout=responsive, true by default
      def amp_images(input, responsive = true, wi = nil, he = nil)
        destdir = File.join(Dir.pwd, '/mobile/images/')
        FileUtils::mkdir_p destdir
        doc = Nokogiri::HTML.fragment(input);
        # Add width and height to img elements lacking them
        doc.css('img:not([width])').each do |image|
          puts image['src'] + ' does not have w and h, trying to figure it out!'
          #if wi && he
          #  image['width']  = wi
          #  image['height'] = he
          #else
          destfn = Digest::MD5.hexdigest(image['src']) + File.extname(image['src'])

          dest = File.join(destdir, destfn)
          puts 'Checking if its local copy ' + dest + ', is there or not?'

          if File.exist?(dest)
            puts dest + ' is already there.'
          else
            if image['src'].start_with?('http://', 'https://')
              src = image['src']
            else
              # FastImage doesn't seem to handle local paths when used with Jekyll
              src = File.join(Dir.pwd, image['src'])
            end
            size = FastImage.size(src)
            if size[0] > 1920
              FastImage.resize(src, 1920, 0, :outfile=>dest)
            else
              FastImage.resize(src, size[0], 0, :outfile=>dest)
            end
            if !File.exist?(dest)
              abort 'WTF? ' + dest + ' is not there.'
            end
          end
          # Jekyll generates static assets after the build process.
          # This causes problems when trying to determine the dimensions of a locally stored image.
          # For now, the only solution is to skip the build and generate the AMP files after the site has beem successfully built.
          # TODO: find a better solution.
          begin
            size = FastImage.size(dest)
            image['width']  = size[0]
            image['height'] = size[1]
            image['src'] = "/mobile/images/" + destfn
          rescue Exception => e
            puts 'Unable to get image dimensions for "' + dest + '". [Error: ' + e.to_s + ']'
          end
          #end
        end
        # Change 'img' elements to 'amp-img', add responsive attribute when needed
        doc.css('img').each do |image|
          #destfn = Digest::MD5.hexdigest(image['src']) + File.extname(image['src'])
          image.name = "amp-img"
          image['layout'] = "responsive" if responsive
        end
        # Return the html as plaintext string
        doc.to_s
      end
    end
  end

  Liquid::Template.register_filter(Jekyll::AmpFilter)
