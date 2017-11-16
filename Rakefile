
require 'pathname'


project_dir = Pathname.new "projects/EX1605L3_one/"
json_file = project_dir.join('image_set.json')

task :extract do

  json_files = Dir.glob(project_dir.join('*.json'))

  sh "#{ENV['GOPATH']}/bin/extract_set",
      '-delete',
      json_file.to_s

end

task :photoscan do
  photoscan="/opt/photoscan-pro/photoscan.sh"

  json_files = Dir.glob(project_dir.join('*.json'))

  sh photoscan, '-r', 'scripts/photoscan.py',
      '--align',
      json_file.to_s
end
