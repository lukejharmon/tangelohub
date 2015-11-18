from girder_client import GirderClient
import json
import pymongo
import sys

if len(sys.argv) < 2:
    print "%s /path/to/ArborWebApps" % sys.argv[0]
    sys.exit(1)
arborWebAppsPath = sys.argv[1]

# Get the ID for our Analyses folder.
c = GirderClient(host='localhost', port=9000)
c.authenticate('girder', 'girder')
folderSearch = c.get('resource/search', parameters={
    'q': 'Analyses',
    'types': '["folder"]'
})
folderId = folderSearch['folder'][0]['_id']

# Disable authorization requirements for running romanesco tasks
c.put('system/setting', parameters={
    'key': 'romanesco.require_auth',
    'value': 'false'
})

# Check if these analyses already exist.  If so, we won't re-upload them.
uploadACR = False
uploadPHYSIG = False
uploadPGLS = False

searchACR = c.get('resource/search', {
    'q': 'aceArbor',
    'types': '["item"]'
})
if len(searchACR['item']) == 0:
  uploadACR = True

searchPHYSIG = c.get('resource/search', {
    'q': 'Phylogenetic signal',
    'types': '["item"]'
})
if len(searchPHYSIG['item']) == 0:
  uploadPHYSIG = True

searchPGLS = c.get('resource/search', {
    'q': 'PGLS',
    'types': '["item"]'
})
if len(searchPGLS['item']) == 0:
  uploadPGLS = True



# Read our analyses into Python dictionaries and upload them to girder.
if uploadACR:
  ACR = {}
  with open ("%s/ancestral-state/aceArbor.json" % arborWebAppsPath, "r") as acrFile:
      acrStr = acrFile.read()
  ACR['analysis'] = json.loads(acrStr)
  item = c.createItem(folderId, 'aceArbor', 'Ancestral state reconstruction')
  c.addMetadataToItem(item['_id'], ACR)
  print "aceArbor successfully uploaded"
else:
  print "aceArbor already exists"

if uploadPHYSIG:
  PHYSIG = {}
  with open ("%s/phylogenetic-signal/Phylogenetic_signal.json" % arborWebAppsPath, "r") as physigFile:
      physigStr = physigFile.read()
  PHYSIG['analysis'] = json.loads(physigStr)
  item = c.createItem(folderId, 'Phylogenetic signal', 'Phylogenetic signal')
  c.addMetadataToItem(item['_id'], PHYSIG)
  print "Phylogenetic signal successfully uploaded"
else:
  print "Phylogenetic signal already exists"

if uploadPGLS:
  PGLS = {}
  with open ("%s/PGLS/PGLS.json" % arborWebAppsPath, "r") as pglsFile:
      pglsStr = pglsFile.read()
  PGLS['analysis'] = json.loads(pglsStr)
  item = c.createItem(folderId, 'PGLS', 'PGLS')
  c.addMetadataToItem(item['_id'], PGLS)
  print "PGLS successfully uploaded"
else:
  print "PGLS already exists"

