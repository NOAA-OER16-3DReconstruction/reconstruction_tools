
require 'pathname'


project_dir = Pathname.new "projects/EX1605L3_one/"

task :extract do

  json_files = Dir.glob(project_dir.join('*.json'))

  sh "#{ENV['GOPATH']}/bin/extract_set",
      '-delete',
      '-outdir', project_dir.to_s,
      *json_files

end

task :photoscan do
  photoscan="/opt/photoscan-pro/photoscan.sh"

  json_files = Dir.glob(project_dir.join('*.json'))

  sh photoscan, '-r', 'scripts/photoscan.py',
      '--align',
      project_dir.to_s
end
