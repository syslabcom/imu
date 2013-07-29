## Script (Python) "getFirstParent"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj='', city=0
##title=return first parent after root folder

foldername = ''
path = ''
folder = None
purl = context.portal_url
portal = purl.getPortalObject()

if not obj:
    obj = context

cityfolders = portal.getProperty('cityfolders', [])

ppath = purl.getRelativeUrl(obj).split('/')
if len(ppath)>0:
    if city:
        if ppath[0] in cityfolders:
            folder = portal.restrictedTraverse(ppath[0], '')
            if folder:
                foldername = folder.Title()
                path = purl.getRelativeUrl(folder)
    else:
        folder = portal.restrictedTraverse(ppath[0], '')
        if folder:
            foldername = folder.Title()
            path = purl.getRelativeUrl(folder)
            
return (foldername, folder, path)

