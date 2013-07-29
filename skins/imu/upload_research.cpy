## Controller Python Script "upload_research_form"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=file=''
##title=Upload research

from Products.IMU.utils import getProjects, checkProjectId
from StringIO import StringIO
from DateTime import DateTime


request = context.REQUEST
folder = context

feedback = {}
fb_error = 0
fb_entries = []

fp = StringIO(file.read())
file.seek(0)

elems = getProjects(fp)

type_name='Research'
utiltool = context.portal_utilities
to_utf8 = utiltool.to_utf8
ctool = context.portal_catalog

logit = utiltool.logit

for e in elems:
    # make projectnumber/mandant check

    pid = e['projectnumber']
    mandant = e['mandant']

    pobjid, opid = checkProjectId(folder, pid, mandant)

    if pobjid:
        obj = getattr(folder, pobjid, '')
        msg = 'Forschungsprojekt aktualisiert.'
        state = 'updated'
    else:
        id = folder.generateUniqueId(type_name)
        folder.manage_addProduct['IMU'].addResearch(id=id, title='')
        obj = getattr(folder, id, None)
        msg = 'Forschungsprojekt neu angelegt.'
        state = 'created'

    if obj:
        sd = e['start_date'].split('.')
        ed = e['end_date'].split('.')
        sddt = DateTime('%s/%s/%s' % (sd[2], sd[1], sd[0]))
        eddt = DateTime('%s/%s/%s' % (ed[2], ed[1], ed[0]))
        obj.manage_edit( text_format = 'html'
                        , text=to_utf8(e['bodytext'])
                        , title=to_utf8(e['title'])
                        , projectnumber=pid
                        , projecttype=to_utf8(e['projecttype'])
                        , manager = to_utf8(e['manager'])
                        , financier=to_utf8(e['financier'])
                        , mandant=to_utf8(e['mandant'])
                        , partner=to_utf8(e['partner'])
                        , start_date=sddt
                        , end_date=eddt
                        , description=to_utf8(e['description'])
                        , localizer_language='de'
                        , translation_complete='1'
                        , request=None)
    else:
        msg = 'Forschungsprojekt anlegen schlug fehl.'
        state='error'

    fb_entries.append({'obj':obj,
                       'opid':opid,
                       'status':state,
                       'msg':msg})

feedback['error'] = fb_error
feedback['entries'] = fb_entries
feedback['num_entries'] = len(elems)

if feedback['error']:
    return state.set(status='failure', context=context , portal_status_message=msg)
else:
    return context.upload_research_feedback(feedback=feedback)
