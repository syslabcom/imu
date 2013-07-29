## Script (Python) "listAvailablePortlets"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=listAvailablePortlets 

request = context.REQUEST
portal = context.portal_url.getPortalObject()
additionals = portal.getProperty('additional_portlet_skinfolders', ())

logit = context.portal_utilities.logit

obs = {}
   
# portlet skins
skinstool = context.portal_skins
pskinfolders = ('imu', 'custom')
if additionals:
    pskinfolders = pskinfolders + additionals
    
defskin = skinstool.getDefaultSkin()
skinfolders = [x.strip() for x in skinstool.getSkinPath(defskin).split(',')]

skinfolders.reverse()
    
skip = ['portlet_overview', 'portlet_edit_form', 'portlet_macro_template', 'portlet_box_template']

def getPortletSkins(folder):
    fobs = folder.objectValues()
    for o in fobs:
        if o.meta_type in ['Page Template', 'Filesystem Page Template'] and string.find(o.id, 'portlet_')==0 and o.id not in skip:
            obs[o.id] = o
            
for f in skinfolders:
    if f in pskinfolders:
        try:
            sf = skinstool.restrictedTraverse(f, '')
            getPortletSkins(sf)
        except:
            pass
    
            
# page templates, documents starting wiht portlet_


# portlet and page template objects
cobjs = {}

def searchPortlets(obj):
    parent = obj.aq_parent
    if obj.isPrincipiaFolderish:
        objs = context.ZopeFind(obj, obj_metatypes=['eIT Portlet', 'Page Template'], search_sub=0)
        for o in objs:
            if o[0] not in cobjs.keys():
                cobjs[o[0]] = o[1]
    if obj!=portal:
        searchPortlets(parent)
        
searchPortlets(context)
for co in cobjs.keys():
    chk = getattr(context, co, '')
    if chk.meta_type == "Page Template":
        if not "portlet" in chk.macros.keys():
            chk = None

    if chk:
        obs[chk.id] = chk
     
portlets = obs.values()
portlets.sort(lambda x, y: cmp(x.title_or_id().lower(),y.title_or_id().lower()))
return portlets
