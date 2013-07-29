import Globals, string, os
from StringIO import StringIO
from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.DirectoryView import createDirectoryView
from Products.IMU import module_globals, IMUResearch, IMUSeminar, IMUPublication, IMUConsulting

def install(self):
    """
    install the IMU Product
    """    
    out = StringIO()
    portal = self.portal_url.getPortalObject()
    
    out.write('Install IMU portal types to portal_types tool\n')
    
    # setup the new types
    typestool = portal.portal_types
    newTypes = [ IMUResearch
               , IMUSeminar
               , IMUPublication
               , IMUConsulting
               ]
    for i in newTypes:
        t = i.factory_type_information
        if t['id'] in typestool.objectIds():
            typestool._delObject(t['id'])
        cfm = apply(ContentFactoryMetadata, (), t)
        typestool._setObject(t['id'], cfm)
    
    skinFolder = 'imu'

    skinstool = portal.portal_skins
    if skinFolder in skinstool.objectIds():
        skinstool.manage_delObjects([skinFolder,])
    sp = os.path.join( Globals.package_home( module_globals ), 'skins', skinFolder )
    createDirectoryView(skinstool, sp, skinFolder)
    out.write('Skinfolder '+skinFolder+' added to portal_skins\n')
    
    # setup imu skin path
    skinname = 'imu'
    path=[elem.strip() for elem in skinstool.getSkinPath('elevateIT Default').split(',')]
    path.insert(path.index('custom')+1, skinname)
    skinstool.addSkinSelection(skinname, ','.join(path))
    
    out.write("skin imu created\n")
    
    skinstool.default_skin=skinname
        
    
#     left_slots = ( 'here/portlet_nav_imu/macros/portlet', 
#                    'here/portlet_nav_standorte/macros/portlet' )
#                  
#     right_slots = ( 'here/portlet_calendar/macros/portlet' 
#                  , 'here/portlet_news/macros/portlet' )
#                  
#     portal._updateProperty('left_slots', left_slots )
#     portal._updateProperty('right_slots', right_slots )
#     out.write('Portlet slots changed. We only need menu portlet in left slot.\n')
    
    # update portal properties
    sp = portal.portal_properties.site_properties
        
    sp._updateProperty('localTimeFormat', '%d.%m.%Y')
    sp._updateProperty('localLongTimeFormat', '%d.%m.%Y %H:%M')
    
    if sp.hasProperty('listMandants'):
        sp._delProperty('listMandants')
            
    if not sp.hasProperty('listProjecttypes'):
        sp._setProperty('listProjecttypes', ('Auftragsforschung', 'Sachverstand', 'Seminare', 'Grundlagenforschung', 'zweckbetr. Forschung'), 'lines')
            
    out.write("site properties updated\n")
    
    cityfolders = ['muenchen', 'berlin_dresden', 'karlsruhe', 'nuernberg', 'stuttgart']
    if not portal.hasProperty('cityfolders'):
        portal._setProperty('cityfolders', cityfolders, 'lines')
        out.write("properties cityfolders added\n")
    
    # set seminar as calendar type
    ct = portal.portal_calendar.calendar_types
    ct.append('Seminar')    
    portal.portal_calendar.calendar_types = ct 
    out.write("Seminar added to portal calendars calendar types\n")
    
    # setup default language
    languageTool = portal.portal_languages.setDefaultLanguage('de')
    
    memberdata = portal.portal_memberdata
    if memberdata.hasProperty('language'):
        memberdata._updateProperty('language', 'de')
    else:
        memberdata._setProperty('language', 'de', 'string')
    out.write("default language set to de\n")
    
    # add second navigation
    portlettool = portal.portal_utilities
    to_utf8 = portlettool.to_utf8
    ll=['de',]
    if not hasattr(portal, 'navigation'):
        portal.manage_addProduct['elevateIT'].addNavigation(id='navigation', 
                                                           localizer_languages=ll)
        n = portal.navigation
        n._setPortalTypeName( 'Navigation' )
        n.setTitle(to_utf8('Navigation'))
        portal.portal_workflow.doActionFor(n, 'publish', comment='navigation object should be public now.')
        out.write("add navigation\n")
        
    if not hasattr(portal, 'navigation_standorte'):
        portal.manage_addProduct['elevateIT'].addNavigation(id='navigation_standorte', 
                                                           localizer_languages=ll)
        n = portal.navigation_standorte
        n._setPortalTypeName( 'Navigation' )
        n.setTitle(to_utf8('Navigation'))
        out.write("add navigation_standorte\n")
        
    # add action upload projects
         
    at = portal.portal_actions   
    na = {"id":"upload_research", "name":"Upload research", "action":"string:${folder_url}/upload_research_form", "condition":"python:'research' in folder.absolute_url(1).split('/')", "permission":"Modify portal content", "category":"objectAdmin", "visible":1}
    
    if not na['id'] in [x.id for x in at.listActions()]:
        at.addAction(na['id'], na['name'], na['action'], na['condition'], na['permission'], na['category'], na['visible'])
        out.write("Action upload projects added\n")
    else:
        out.write("Action upload projects already exists\n")
        
    # add catalog indexes 
    ind = ['mandant']
    ctool = portal.portal_catalog
    for i in ind:
        if i not in ctool.indexes():
            ctool.manage_addIndex(i, 'FieldIndex')
            out.write("Index %s added\n" % i)
            
    class Extra:
        """ Just a dummy to build records for the Lexicon.
        """
        pass
        
    zcind = ['projectnumber']
    extra = Extra()
    extra.index_type = 'Okapi BM25 Rank'
    extra.lexicon_id = 'plone_lexicon'
        
    for i in zcind:
        if i not in ctool.indexes():
            extra.doc_attr = ''
            ctool.addIndex(i, 'ZCTextIndex', extra)
   
    
    return out.getvalue()
