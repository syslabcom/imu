from Globals import InitializeClass, Persistent, HTMLFile
from DateTime import DateTime
from string import join
from AccessControl import ClassSecurityInfo
from Products.elevateIT.Localizer.LocalPropertyManager import LocalProperty
from Products.elevateIT.eITDocument import eITDocument
from Products.CMFCore.interfaces.Dynamic import DynamicType
from Products.elevateIT.interfaces.EventInterfaces import IObjectEventPublisher

# Import permission names
from Products.CMFCore import CMFCorePermissions


factory_type_information = {'id'       : 'Consulting',
                            'meta_type' : 'IMU Consulting',
                            'description'   : ('Add a Consulting'),
                            'icon'      : 'consulting_icon.gif',
                            'product'   : 'IMU',
                            'factory'   : 'addConsulting',
                            'filter_content_types' : 1,
                            'allowed_content_types' : ('File', 'Image', 'Link', 'I18NLayer'),
                            'immediate_view': 'consulting_edit_form',
                            'actions'   : (
                                {'id'       : 'view',
                                'name'     : 'View',
                                'action'   : 'string:${object_url}/consulting_view',
                                'permissions'  : (CMFCorePermissions.View,),
                                },
                                {'id'       : 'folderlisting',
                                 'name'     : 'Folder Listing',
                                 'action'   : 'string:${object_url}/consulting_view',
                                 'permissions' :( CMFCorePermissions.View,),
                                 'visible'  : 0
                                },
                                {'id'      : 'edit',
                                'name'    : 'Edit',
                                'action'  : 'string:${object_url}/consulting_edit_form',
                                'permissions' : (CMFCorePermissions.ModifyPortalContent,),
                                },
                                {'id'      : 'contents',
                                'name'    : 'Attachments',
                                'action'  : 'string:${object_url}/folder_contents',
                                'permissions' : (CMFCorePermissions.ModifyPortalContent,),
                                },
                                { 'id'      : 'properties',
                                'name'    : 'Properties',
                                'action'  : 'string:${object_url}/metadata_edit_form',
                                'permissions' : (CMFCorePermissions.ModifyPortalContent,),
                                },
                                { 'id'          : 'local_roles'
                                , 'name'        : 'Sharing'
                                , 'action'      : 'string:${object_url}/folder_localrole_form'
                                , 'permissions' : (CMFCorePermissions.ManageProperties,)
                                , 'category'    : 'objectAdmin'
                                },
                                ),
                                }

def addConsulting(self
             , id
             , title=''
             , description=''
             , localizer_languages=[]
             , default_language=''):
    """
    Create an empty Consulting case.
    """
    if type(localizer_languages)!=type([]): localizer_languages = list(localizer_languages)
    preflang = self.portal_languages.getPreferredLanguage()
    if preflang not in localizer_languages:
        localizer_languages.append(preflang)
    if default_language=='':
        default_language = preflang
    o = IMUConsulting(id
              , title=title
              , description=description
              , localizer_languages=localizer_languages
              , default_language=default_language                  
             )
    self._setObject(id, o)
    o._setPortalTypeName( 'Consulting' )
       
    
class IMUConsulting(eITDocument):
    """
    An IMU Consulting case.
    """
    portal_type = 'Consulting'
    meta_type = 'IMU Consulting'

    __implements__ = ( eITDocument.__implements__
                     , DynamicType
                     , IObjectEventPublisher
                     )
                     
    isObjectEventPublisher = 1
    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(CMFCorePermissions.View)
    
    client=''
    period=''
    contact=''
    
    _properties = eITDocument._properties + (
          {'id': 'client', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'period', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'contact', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''}                    
    )
    
    def __init__(self
                 , id
                 , title=''
                 , description=''
                 , localizer_languages=[]
                 , default_language=''):
        eITDocument.__init__(self
                    , id
                    , title=title
                    , description=description
                    , localizer_languages=localizer_languages
                    , default_language=default_language )
                    
        self.client = ''
        self.period = ''
        self.contact= ''
        
    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'manage_edit' )
    def manage_edit( self
            , text_format
            , text=''
            , title=''
            , client = ''
            , period = ''
            , contact = ''        
            , source=''           
            , file=''
            , safety_belt=''
            , localizer_language=None
            , description = ''
            , translation_complete=0
            , request=None):
        "edit the content"
        
        if localizer_language is None:
            localizer_language = request.get('edit_language', '')
        if localizer_language =='' and getattr(self, 'portal_languages', ''):
            localizer_language = self.portal_languages.getPreferredLanguage()

        self.client=client
        self.period=period
        

        eITDocument.manage_edit(self, 
                         text_format=text_format, 
                         text=text, 
                         title=title, 
                         file=file, 
                         safety_belt=safety_belt, 
                         localizer_language=localizer_language, 
                         description=description,
                         translation_complete=translation_complete,
                         request=request)
             
    security.declareProtected(CMFCorePermissions.View, 'SearchableText')
    def SearchableText(self):
        """ Used by the catalog for basic full text indexing """
        return "%s %s %s %s %s %s" % ( self.id
                                , join([ self.Title(x) for x in self.get_languages() ])
                                , join([ self.Description(x) for x in self.get_languages() ])
                                , join([ self.portal_utilities.removeHTML(self.EditableBody(x)) for x in self.get_languages() ])
                                , self.client
                                , self.contact
                                )

InitializeClass(IMUConsulting)
