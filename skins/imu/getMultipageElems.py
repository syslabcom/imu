## Script (Python) "getMultipageElems"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=''
##title=

mp_info = {}

elems = []
prev_elem = None
next_elem = None
separator = '_'
if not obj:
    obj = context

act_elem = obj
act_id = obj.id

base_id = act_id
act_num = 0

if(act_id.rfind(separator)>-1):
    base_id = act_id[:act_id.rfind(separator)]
    try:
        act_num = int(act_id[(act_id.rfind(separator)+1):len(act_id)])
    except:
        # no number after separator? it's the base object
        base_id = act_id
        act_num = 0
        
# get elems
docs = obj.aq_parent.getFolderListingFolderContents()
for doc in docs:
    if doc.portal_type == "Document":
        doc_id = doc.id
        if doc_id.startswith(base_id):
            try:
                num = int(doc_id[(doc_id.rfind(separator)+1):len(doc_id)]) 
            except: 
                num = 0
            elems.append((doc, num))
        
if len(elems)>1:
    elems.sort(lambda x, y: cmp(x[1],y[1]))

sortedelems = []
for n in range(len(elems)):
    sortedelems.append(elems[n][0])
    if elems[n][0]==act_elem:
        if (n-1)>=0:
            prev_elem = elems[n-1][0]
        if (n+1)<len(elems):
            next_elem = elems[n+1][0]
            
mp_info['elems'] = sortedelems
mp_info['current'] = act_elem
mp_info['previous'] = prev_elem
mp_info['next'] = next_elem

return mp_info
