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


factory_type_information = {'id'       : 'Seminar',
                            'meta_type' : 'IMU Seminar',
                            'description'   : ('Add a Seminar'),
                            'icon'      : 'seminar_icon.gif',
                            'product'   : 'IMU',
                            'factory'   : 'addSeminar',
                            'filter_content_types' : 1,
                            'allowed_content_types' : ('File', 'Image', 'Link', 'I18NLayer'),
                            'immediate_view': 'seminar_edit_form',
                            'actions'   : (
                                {'id'       : 'view',
                                'name'     : 'View',
                                'action'   : 'string:${object_url}/seminar_view',
                                'permissions'  : (CMFCorePermissions.View,),
                                },
                                {'id'       : 'folderlisting',
                                 'name'     : 'Folder Listing',
                                 'action'   : 'string:${object_url}/seminar_view',
                                 'permissions' :( CMFCorePermissions.View,),
                                 'visible'  : 0
                                },
                                {'id'      : 'edit',
                                'name'    : 'Edit',
                                'action'  : 'string:${object_url}/seminar_edit_form',
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

def addSeminar(self
             , id
             , title=''
             , description=''
             , localizer_languages=[]
             , default_language=''):
    """
    Create an empty Seminar.
    """
    if type(localizer_languages)!=type([]): localizer_languages = list(localizer_languages)
    preflang = self.portal_languages.getPreferredLanguage()
    if preflang not in localizer_languages:
        localizer_languages.append(preflang)
    if default_language=='':
        default_language = preflang
    o = IMUSeminar(id
              , title=title
              , description=description
              , localizer_languages=localizer_languages
              , default_language=default_language                  
             )
    self._setObject(id, o)
    o._setPortalTypeName( 'Seminar' )
       
    
class IMUSeminar(eITDocument):
    """
    An IMU Seminar.
    """
    portal_type = 'Seminar'
    meta_type = 'IMU Seminar'

    __implements__ = ( eITDocument.__implements__
                     , DynamicType
                     , IObjectEventPublisher
                     )
                     
    isObjectEventPublisher = 1
    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(CMFCorePermissions.View)
    
    _properties = eITDocument._properties + (
          {'id': 'contact_email', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'start_date', 'type':'date', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'end_date', 'type':'date', 'value': '', 'mode': 'w', 'mandatory': ''},
    )
    
    contact_email=''
    start_date = None
    end_date = None
    
    location = LocalProperty('location')
    contact = LocalProperty('contact')
    host = LocalProperty('host')
    
    _local_properties_metadata = eITDocument._local_properties_metadata + (
                {'id': 'location', 'type': 'string'},
                {'id': 'contact', 'type': 'string'},
                {'id': 'host', 'type': 'string'},
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
                    
        self.contact_email = ''
        self.contact = ''
        self.location = ''
        self.host = ''
        self.start_date = None
        self.end_date = None

        
    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'manage_edit' )
    def manage_edit( self
            , text_format
            , text=''
            , location=''
            , contact=''
            , contact_email=''
            , host=''
            , start_date=None
            , end_date=None
            , title=''
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
        
        self.setLocation(location, localizer_language)
        self.setContact(contact, localizer_language)
        self.setHost(host, localizer_language)
        
        self.contact_email = contact_email
        
        self.start_date = self._datify(start_date)
        self.end_date = self._datify(end_date)
        
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
                         
    security.declarePublic( 'Location' )
    def Location( self, language=None ):
        "Location of the Seminar"
        return self._getAttributeFallback('location', language)[0]
        
    security.declarePublic( 'Contact' )
    def Contact( self, language=None ):
        "Contact of the Seminar"
        return self._getAttributeFallback('contact', language)[0]
        
    security.declarePublic( 'Host' )
    def Host( self, language=None ):
        "Host of the Seminar"
        return self._getAttributeFallback('host', language)[0]
        
    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setLocation' )
    def setLocation( self, location, language=None ):
        "set Location of the Seminar"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None): 
                language = self.portal_languages.getPreferredLanguage()          
        if language!="" and language!=None:
            self._setLocalPropValue('location', language, location)
            if language==self.get_default_language():
                self.location = location
        else:
            if self.location=="":
                self.location = location
                
    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setContact' )
    def setContact( self, contact, language=None ):
        "set Contact of the Seminar"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None): 
                language = self.portal_languages.getPreferredLanguage()          
        if language!="" and language!=None:
            self._setLocalPropValue('contact', language, contact)
            if language==self.get_default_language():
                self.contact = contact
        else:
            if self.contact=="":
                self.contact = contact
                
    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setHost' )
    def setHost( self, host, language=None ):
        "set Host of the Seminar"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None): 
                language = self.portal_languages.getPreferredLanguage()          
        if language!="" and language!=None:
            self._setLocalPropValue('host', language, host)
            if language==self.get_default_language():
                self.host = host
        else:
            if self.host=="":
                self.host = host
                
    security.declareProtected('View', 'start')
    def start(self):
        """
            Return our start time as a string.
        """
        date = getattr( self, 'start_date', None )
        return date is None and self.created() or date

    security.declareProtected('View', 'end')
    def end(self):
        """
            Return our stop time as a string.
        """
        date = getattr( self, 'end_date', None )
        return date is None and self.start() or date   
                
    security.declarePrivate( '_datify' )
    def _datify( self, attrib ):
        if attrib == 'None':
            attrib = None
        elif not isinstance( attrib, DateTime ):
            if attrib is not None:
                attrib = DateTime( attrib )
        return attrib
        
    security.declareProtected(CMFCorePermissions.View, 'SearchableText')
    def SearchableText(self):
        """ Used by the catalog for basic full text indexing """
        return "%s %s %s %s %s %s %s" % ( self.id
                                , join([ self.Title(x) for x in self.get_languages() ])
                                , join([ self.Description(x) for x in self.get_languages() ])
                                , join([ self.portal_utilities.removeHTML(self.EditableBody(x)) for x in self.get_languages() ])
                                , join([ self.Location(x) for x in self.get_languages() ])
                                , join([ self.Contact(x) for x in self.get_languages() ])
                                , join([ self.Host(x) for x in self.get_languages() ])
                                )

InitializeClass(IMUSeminar)
