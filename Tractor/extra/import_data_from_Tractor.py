"""
Example of job query return from tractor DB:
{
    u'comment': u' Rendering: Write1.images',
    u'maxslots': 0,
    u'numblocked': 0,
    u'pil': 1701267110,
    u'spoolcwd': u'/tmp',
    u'assignments': u'',
    u'numerror': 0,
    u'elapsedsecs': 21713.669921875,
    u'owner': u'andrea',
    u'spoolhost': u'pc001',
    u'spooladdr': u'10.11.100.110',
    u'jid': 1701267110,
    u'service': u'',
    u'title': u'ToyStory_comp_v002',
    u'numactive': 0,
    u'editpolicy': u'',
    u'spooltime': u'2018-07-22 13:38:05+02',
    u'projects': [u'TOYSTORY'],
    u'crews': [],
    u'maxcid': 82,
    u'metadata': u'',
    u'numready': 0,
    u'tags': [],
    u'afterjids': [],
    u'lastnoteid': 0,
    u'stoptime': u'2018-07-22 14:17:13.046+02',
    u'envkey': [],
    u'tier': u'',
    u'etalevel': 1,
    u'numtasks': 164,
    u'minslots': 0,
    u'serialsubtasks': False,
    u'numdone': 164,
    u'maxtid': 164,
    u'aftertime': None,
    u'maxactive': 0,
    u'spoolfile': u'/unknown_origin',
    u'esttotalsecs': 21713.669921875,
    u'starttime': u'2018-07-22 13:55:56.563+02',
    u'pausetime': None,
    u'dirmap': None,
    u'deletetime': None,
    u'priority': 37315.0,
}
BY Marco Curado
"""

import sys
sys.path.insert(0, 'insert here the path of tractor folder') #tractor/2/linux_x86-64/lib/python2.7/site-packages/

import tractor
from tractor.api import query
from tractor import api
import tractor.api.query as tq

done = tq.jobs("projects={TOYSTORY} and done and owner={andrea}", columns=["jid", "title"], sortby=["-priority"],
               limit=60)

active = tq.jobs("active", columns=["jid", "title"], sortby=["-priority"], limit=20)

ready = tq.jobs("ready", columns=["jid", "title"], sortby=["-priority"], limit=40)

error = tq.jobs("error", columns=["jid", "title"], sortby=["-priority"], limit=10)


for elem in done:
	print elem
