## Script (Python) "groupCatresByCity"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=results
##title=return first parent after root folder

resmap = {}

purl = context.portal_url
portal = purl.getPortalObject()

cityfolders = portal.getProperty('cityfolders', [])

for r in results:
    ppath = r.getPath().split('/')
    if len(ppath)>2:
        foldername = ppath[2]
        if foldername not in cityfolders:
            foldername = 'gesamt'
        if not resmap.has_key(foldername):
            resmap[foldername] = []
        resmap[foldername].append(r)

return resmap

