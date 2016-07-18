import os
from percolation import c

platform = 0
while platform not in ('1', '2'):
    platform = input('platform is jena/fuseki (1) or virtuoso (2)?')


def uploadFile(platform, tdir, adir, afile):
    if platform == '1':
        os.system('s-put http://localhost:3030/adbname/data {} {}/{}/{}'.format(afile, tdir, adir, afile))
    elif platform == '2':
        # os.system('curl --digest --user dba:demo --url "http://192.168.0.11:8890/sparql-graph-crud-auth?graph-uri=urn:{}" -T {}/{}/{}'.format(afile, tdir, adir, afile))
        # os.system('curl --digest --user dba:dba --url "http://192.168.0.11:8890/sparql-graph-crud-auth?graph-uri=urn:{}" -T {}/{}/{}'.format(afile, tdir, adir, afile))
        os.system('curl --digest --user dba:dba --url "http://localhost:8890/sparql-graph-crud-auth?graph-uri=urn:{}" -T {}/{}/{}'.format(afile, tdir, adir, afile))
        # os.system('curl --digest --user dba:dba --url "http://localhost:8890/sparql-graph-crud-auth?graph-uri=urn:percolation" -T {}/{}/{}'.format(tdir, adir, afile))

ans = input('add twitter translates (y/n)')
if ans[0] == 'y':
    tdir = '/home/r/repos/social/tests/twitter_snapshots'
    dirs = os.listdir(tdir)
#    dirs = [i for i in dirs if not ('Snap' in i or 'science' in i or 'Fora' in i)]
    for adir in dirs:
        files = os.listdir('{}/{}'.format(tdir, adir))
        # files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        files_ = [i for i in files if i.endswith('.ttl')]
        for afile in files_:
            c(afile, 'pre')
            uploadFile(platform, tdir, adir, afile)
            c(afile, 'pos')
ans = input('add facebook translates (y/n)')
if ans[0] == 'y':
    tdir = '/home/r/repos/social/tests/facebook_snapshots'
    dirs = os.listdir(tdir)
    for adir in dirs:
        files = os.listdir('{}/{}'.format(tdir, adir))
        files_ = [i for i in files if i.endswith('.ttl')]
        # files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            uploadFile(platform, tdir, adir, afile)
            c(afile, 'pos')
# irc
ans = input('add irc translates (y/n)')
if ans[0] == 'y':
    tdir = '/home/r/repos/social/tests/irc_snapshots'
    dirs = os.listdir(tdir)
    for adir in dirs:
        files = os.listdir('{}/{}'.format(tdir, adir))
        files_ = [i for i in files if i.endswith('.ttl')]
        # files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            uploadFile(platform, tdir, adir, afile)
            c(afile, 'pos')
# gmane
ans = input('add gmane translates (y/n)')
if ans[0] == 'y':
    tdir = '/home/r/repos/gmane/tests/gmane_snapshots'
    dirs = os.listdir(tdir)
    for adir in dirs:
        files = os.listdir('{}/{}'.format(tdir, adir))
        files_ = [i for i in files if i.endswith('.ttl')]
        # files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            uploadFile(platform, tdir, adir, afile)
            c(afile, 'pos')

# participa
ans = input('add participabr translates (y/n)')
if ans[0] == 'y':
    # tdir = '/home/r/repos/participation/participation/participabr/participabr_snapshot'
    # dirs = os.listdir(tdir)
    tdir = ''
    dirs = '/home/r/repos/participation/participation/participabr/participabr_snapshot',
    for adir in dirs:
        files = os.listdir('{}'.format(adir))
        files_ = [i for i in files if i.endswith('.ttl')]
        # files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            uploadFile(platform, tdir, adir, afile)
            c(afile, 'pos')

# AA
ans = input('add aa translates (y/n)')
if ans[0] == 'y':
    # tdir = '/home/r/repos/participation/participation/aa/aa_snapshots'
    # dirs = os.listdir(tdir)
    tdir = ''
    dirs = '/home/r/repos/participation/participation/aa/aa_snapshots',
    for adir in dirs:
        files = os.listdir('{}'.format(adir))
        files_ = [i for i in files if i.endswith('.ttl')]
        # files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            uploadFile(platform, tdir, adir, afile)
            c(afile, 'pos')

# Cidade Democratica
ans = input('add cidade democratica translates (y/n)')
if ans[0] == 'y':
    # tdir = '/home/r/repos/participation/participation/cidadedemocratica/cidadedemocratica_snapshot'
    # dirs = os.listdir(tdir)
    tdir = ''
    dirs = '/home/r/repos/participation/participation/cidadedemocratica/cidadedemocratica_snapshot',
    for adir in dirs:
        files = os.listdir('{}'.format(adir))
        files_ = [i for i in files if i.endswith('.ttl')]
        # files_ = [i for i in files if i.endswith('.ttl') and 'Meta' not in i]
        for afile in files_:
            c(afile, 'pre')
            uploadFile(platform, tdir, adir, afile)
            c(afile, 'pos')
