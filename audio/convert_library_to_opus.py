import os.path
import subprocess
import shutil

source = "/run/media/hatsnp/backup/Music"
target = "/run/media/hatsnp/backup/OpusMusic"

source_uris = []
uris_to_delete = []

def walk(d, append):
    for f in os.listdir(d):
        nd = os.path.join(d, f)
        
        f = os.path.join(append, f)
        source_uris.append(f)

        if os.path.isdir(nd):
            walk(nd, f)

#loops over target and deletes folders that don't exist in origin
#could all be done in the same loop but it's fast and reads clearer this way
def sync_target(t, s, append):
    for f in os.listdir(t):
        nd = os.path.join(target, f)
        f = os.path.join(append, f)

        if os.path.isdir(nd):
            if not os.path.isdir(os.path.join(s, f)):
                uris_to_delete.append(nd)
            sync_target(nd, s, f)

walk(source, "")

for uri in source_uris:
    s_uri = os.path.join(source, uri)
    t_uri = os.path.join(target, uri)

    if os.path.isdir(s_uri) and not os.path.isdir(t_uri):
        print(f'Creating new dir {t_uri}')
        os.makedirs(t_uri)
        continue
    
    xt = uri.split('.')[-1]
    t_opus = t_uri.replace(xt, 'opus')
    if xt in [ 'flac', 'wav' ]:
        if os.path.isfile(t_opus):
            continue

        print(f'Converting to -> {t_opus}')
        subprocess.run(["opusenc", "--bitrate", "128", "--vbr", s_uri, t_opus])

    if xt in [ 'mp3', 'opus' ]:
        if os.path.isfile(t_uri):
            continue

        print(f'Copying from {s_uri} to {t_uri}')
        shutil.copy(s_uri, t_uri)

print(f'Deleting orphan dirs in target')
sync_target(target, source, "")
for uri in uris_to_delete:
    print(f'Deleting Directory -> {uri}')
    shutil.rmtree(uri)


