import os
from percolation import c
ans = input('add twitter translates (y/n)')
if ans[0] == 'y':
    tdir = '/home/r/repos/social/tests/twitter_snapshots'
    dirs = os.listdir(tdir)
    dirs = [i for i in dirs if ('Snap' in i or 'science' in i or 'Fora' in i)]
    for adir in dirs[:3]:
        files = os.listdir('{}/{}'.format(tdir, adir))
        files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            os.system('s-put http://localhost:3030/adbname/data {} {}/{}/{}'.format(afile, tdir, adir, afile))
            c(afile, 'pos')
ans = input('add facebook translates (y/n)')
if ans[0] == 'y':
    tdir = '/home/r/repos/social/tests/facebook_snapshots'
    dirs = os.listdir(tdir)
    for adir in dirs[:3]:
        files = os.listdir('{}/{}'.format(tdir, adir))
        files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            os.system('s-put http://localhost:3030/adbname/data {} {}/{}/{}'.format(afile, tdir, adir, afile))
            c(afile, 'pos')
