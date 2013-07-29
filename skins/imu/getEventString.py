##parameters=event

transString = context.portal_utilities.transString
eventtype = transString(event['event'].portal_type, domain='elevateIT')
cityname = context.getFirstParent(obj=event['event'].getObject(), city=1)[0]
if cityname:
    eventtype = "%s - %s" % (eventtype, cityname)
eventinfo = "<strong>%s: %s</strong>" % (eventtype, event['title'])

if event['start'] and event['end']:
    start = event['start'][0:string.rfind(event['start'], ':')]
    end = event['end'][0:string.rfind(event['end'], ':')]
    eventstring = "%s-%s <br />" % (start, end)
elif event['start']: # can assume not event['end']
    start = event['start'][0:string.rfind(event['start'], ':')]
    eventstring = "%s- <br />" % (start)
elif event['end']: # can assume not event['start']
    end = event['end'][0:string.rfind(event['end'], ':')]
    eventstring = "-%s <br />" % (end)
else: # can assume not event['start'] and not event['end']
    eventstring = ""


eventstring = "%s%s<br />" % (eventstring, eventinfo)



return eventstring
