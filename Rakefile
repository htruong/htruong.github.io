require "rubygems"
require "tmpdir"

require "bundler/setup"
require "jekyll"


# Change your GitHub reponame
GITHUB_REPONAME = "htruong/htruong.github.io"


desc "Generate blog files"
task :generate do
  Jekyll::Site.new(Jekyll.configuration({
    "source"      => ".",
    "destination" => "_site"
  })).process
end


desc "Generate and publish blog to gh-pages"
task :publish => [:generate] do
  Dir.mktmpdir do |tmp|
    system "echo the temp dir is #{tmp}"
    system "rsync -a _site/ #{tmp}"

    #pwd = Dir.pwd
    system "git checkout master" or exit

    system "touch .nojekyll"
    system "rsync #{tmp}/_site/ ."
    system "git add ."
    message = "Site updated at #{Time.now.utc}"
    #system "git commit -m #{message.inspect}"
    #system "git remote add origin git@github.com:#{GITHUB_REPONAME}.git"
    #system "git push origin master --force"
    #system "git checkout source"

    #Dir.chdir pwd
  end
end
