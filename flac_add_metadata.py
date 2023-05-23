#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import glob

parser = argparse.ArgumentParser()

parser.add_argument('--json', type=str, required=True)
parser.add_argument('--dir', type=str, required=True)
parser.add_argument('--mixtape', default=False, type=bool, required=False)

args = vars(parser.parse_args())

print(args)

json_file = args['json']
print(json_file)
with open(json_file) as f:
   data = json.load(f)
   print(data)

mixtape_bool = args['mixtape']

def mod_song_meta_data(data: dict, file: str, mixtape_bool: bool):
    file_name = file.split('/')[-1]
    track_number = file_name.split(' - ')[0]
    print(data['Songs'][track_number]['ARTIST'])

    #Album
    tag_album = data['ALBUM']
    cmd_album = [
                'metaflac',
                '--remove-tag=ALBUM',
                '--set-tag=ALBUM=' + tag_album,
                file
                ]

    #AlbumArtist
    tag_alb_art = data['ALBUMARTIST']
    cmd_alb_art = [
                'metaflac',
                '--remove-tag=ALBUMARTIST',
                '--set-tag=ALBUMARTIST=' + tag_alb_art,
                file
                ]

    #MUSICBRAINZ_ALBUMARTIST
    tag_muscbrnz_alb_art = data['MUSICBRAINZ_ALBUMARTIST']
    cmd_muscbrnz_alb_art = [
                'metaflac',
                '--remove-tag=MUSICBRAINZ_ALBUMARTIST',
                '--set-tag=MUSICBRAINZ_ALBUMARTIST=' + tag_muscbrnz_alb_art,
                file
                ]

    #ARTIST
    if mixtape_bool:
        tag_art = data['Songs'][track_number]['ARTIST']
    else:
        tag_art = data['ARTIST']
    cmd_art = [
                'metaflac',
                '--remove-tag=ARTIST',
                '--set-tag=ARTIST=' + tag_art,
                file
                ]

    #TRACKNUMBER
    tag_trknum = str(data['Songs'][track_number]['TRACKNUMBER'])
    cmd_trknum = [
                'metaflac',
                '--remove-tag=TRACKNUMBER',
                '--set-tag=TRACKNUMBER=' + tag_trknum,
                file
                ]

    #TITLE
    tag_title = data['Songs'][track_number]['TITLE']
    cmd_title = [
                'metaflac',
                '--remove-tag=TITLE',
                '--set-tag=TITLE=' + tag_title,
                file
                ]

    #GENRE
    tag_genre = data['GENRE']
    cmd_genre = [
                'metaflac',
                '--remove-tag=GENRE',
                '--set-tag=GENRE=' + tag_genre,
                file
                ]

    # Run the commands to process the files
    out_album = subprocess.run(cmd_album, 
                            capture_output=True)
    out_alb_art = subprocess.run(cmd_alb_art, 
                                capture_output=True)
    out_muscbrnz_alb_art = subprocess.run(cmd_muscbrnz_alb_art, 
                                        capture_output=True)
    out_art = subprocess.run(cmd_art, 
                            capture_output=True)
    out_trknum = subprocess.run(cmd_trknum, 
                                capture_output=True)
    out_title = subprocess.run(cmd_title, 
                            capture_output=True)
    out_genre = subprocess.run(cmd_genre, 
                            capture_output=True)

    #Change file Name
    file_path = file.split('/')
    file_path.pop()

    file_name_new = track_number + ' - ' + tag_title + '.flac'
    file_new = '/'.join(file_path) + '/' + file_name_new

    os.rename(file, file_new)

    return file_new #Could add a dictionary of subprocess outs.


flac_dir =  args['dir']
mixtape_bool = True

new_files = []
for i in glob.glob(flac_dir + '*.flac'):
    file_name = i.split('/')[-1]
    print(file_name)
    new_files.append(mod_song_meta_data(data, i, mixtape_bool))
    print(new_files[-1])



# Command line example check that the renameing worked. Could fold into a check.
#!ls /Users/jcorwin/Desktop/MusicTemp/MixTapes/Lisa\ MixTape\ 01/

#!metaflac --list /Users/jcorwin/Desktop/MusicTemp/MixTapes/Lisa\ MixTape\ 01/15\ -\ Uncle\ John\'s\ Band.flac | grep comment


