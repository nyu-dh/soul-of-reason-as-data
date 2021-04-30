require 'fileutils'

ids = IO.readlines 'scripts/finished_transcript_ids.txt', chomp: true

# rm drafts
FileUtils.rm Dir.glob('data/*draft*.txt')

Dir.glob('data/*.txt').each do |f|
  name = File.basename f
  name.gsub! /\..*$/, ''
  name.gsub! /_0+1$/, ''

  if ids.include? name
    File.rename(f, "data/#{name}.txt")
  else
    FileUtils.rm f
  end
end
