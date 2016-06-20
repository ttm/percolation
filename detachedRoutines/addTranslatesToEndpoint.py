import os
from percolation import c
tdir = '/home/r/repos/social/tests/facebook_snapshots'
dirs = os.listdir(tdir)
for adir in dirs[:3]:
    files = os.listdir('{}/{}'.format(tdir, adir))
    files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
    for afile in files_:
        c(afile, 'pre')
        os.system('s-put http://localhost:3030/adbname/data {} {}/{}/{}'.format(afile, tdir, adir, afile))
        c(afile, 'pos')
