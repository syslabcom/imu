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


factory_type_information = {'id'       : 'Publication',
                            'meta_type' : 'IMU Publication',
                            'description'   : ('Add a Publication'),
                            'icon'      : 'publication_icon.gif',
                            'product'   : 'IMU',
                            'factory'   : 'addPublication',
                            'filter_content_types' : 1,
                            'allowed_content_types' : ('File', 'Image', 'Link', 'I18NLayer'),
                            'immediate_view': 'publication_edit_form',
                            'actions'   : (
                                {'id'       : 'view',
                                'name'     : 'View',
                                'action'   : 'string:${object_url}/publication_view',
                                'permissions'  : (CMFCorePermissions.View,),
                                },
                                {'id'       : 'folderlisting',
                                 'name'     : 'Folder Listing',
                                 'action'   : 'string:${object_url}/publication_view',
                                 'permissions' :( CMFCorePermissions.View,),
                                 'visible'  : 0
                                },
                                {'id'      : 'edit',
                                'name'    : 'Edit',
                                'action'  : 'string:${object_url}/publication_edit_form',
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

def addPublication(self
             , id
             , title=''
             , description=''
             , localizer_languages=[]
             , default_language=''):
    """
    Create an empty Publication.
    """
    if type(localizer_languages)!=type([]): localizer_languages = list(localizer_languages)
    preflang = self.portal_languages.getPreferredLanguage()
    if preflang not in localizer_languages:
        localizer_languages.append(preflang)
    if default_language=='':
        default_language = preflang
    o = IMUPublication(id
              , title=title
              , description=description
              , localizer_languages=localizer_languages
              , default_language=default_language
             )
    self._setObject(id, o)
    o._setPortalTypeName( 'Publication' )


class IMUPublication(eITDocument):
    """
    An IMU Publication.
    """
    portal_type = 'Publication'
    meta_type = 'IMU Publication'

    __implements__ = ( eITDocument.__implements__
                     , DynamicType
                     , IObjectEventPublisher
                     )

    isObjectEventPublisher = 1
    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(CMFCorePermissions.View)

    imu_publisher=''
    imu_in=''
    series=''
    number=''
    imu_author=''
    location=''
    company=''
    year=''
    isbn = ''
    scope = ''
    price=''
    source=''

    _properties = eITDocument._properties + (
          {'id': 'imu_publisher', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'imu_in', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'number', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'imu_author', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'location', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'year', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'isbn', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'price', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'source', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
    )

    series  =LocalProperty('series')
    company =LocalProperty('company')
    company =LocalProperty('scope')

    _local_properties_metadata = eITDocument._local_properties_metadata + (
            {'id': 'series', 'type':'string'},
            {'id': 'company', 'type':'string'},
            {'id': 'scope', 'type':'string'},
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

        self.imu_publisher = ''
        self.imu_in = ''
        self.series = ''
        self.number = ''
        self.imu_author = ''
        self.location = ''
        self.company = ''
        self.year = ''
        self.isbn = ''
        self.price = ''
        self.source = ''
        self.scope = ''


    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'manage_edit' )
    def manage_edit( self
            , text_format
            , text=''
            , title=''
            , imu_publisher = ''
            , imu_in=''
            , series = ''
            , number = ''
            , imu_author = ''
            , location = ''
            , company = ''
            , year=''
            , isbn=''
            , price = ''
            , source=''
            , scope = ''
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

        self.setSeries(series, localizer_language)
        self.setCompany(company, localizer_language)
        self.setScope(scope, localizer_language)

        self.imu_publisher=imu_publisher
        self.imu_in=imu_in
        self.number=number
        self.imu_author=imu_author
        self.location=location
        self.year=year
        self.isbn=isbn
        self.price=price

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

    security.declarePublic('Series')
    def Series(self, language=None):
        "Series of the publication"
        return self._getAttributeFallback('series', language)[0]

    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setSeries' )
    def setSeries( self, series, language=None ):
        "Set series of the Research"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None):
                language = self.portal_languages.getPreferredLanguage()
        if language!="" and language!=None:
            self._setLocalPropValue('series', language, series)
            if language==self.get_default_language():
                self.series = series
        else:
            if self.series=="":
                self.series = series


    security.declarePublic('Company')
    def Company(self, language=None):
        "Company of the publication"
        return self._getAttributeFallback('company', language)[0]

    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setCompany' )

    def setCompany( self, company, language=None ):
        "set company of the Research"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None):
                language = self.portal_languages.getPreferredLanguage()
        if language!="" and language!=None:
            self._setLocalPropValue('company', language, company)
            if language==self.get_default_language():
                self.company = company
        else:
            if self.company=="":
                self.company = company

    security.declarePublic('Scope')
    def Scope(self, language=None):
        "Scope of the publication"
        return self._getAttributeFallback('scope', language)[0]

    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setScope' )

    def setScope( self, scope, language=None ):
        "Set scope of the publication"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None):
                language = self.portal_languages.getPreferredLanguage()
        if language!="" and language!=None:
            self._setLocalPropValue('scope', language, scope)
            if language==self.get_default_language():
                self.scope = scope
        else:
            if self.scope=="":
                self.scope = scope


    security.declareProtected(CMFCorePermissions.View, 'SearchableText')
    def SearchableText(self):
        """ Used by the catalog for basic full text indexing """
        removeHTML = self.portal_utilities.removeHTML
        return "%s %s %s %s %s %s %s %s %s %s %s %s %s" % ( self.id
                                , join([ self.Title(x) for x in self.get_languages() ])
                                , join([ self.Description(x) for x in self.get_languages() ])
                                , join([ removeHTML(self.EditableBody(x)) for x in self.get_languages() ])
                                , self.isbn
                                , self.imu_in
                                , self.imu_author
                                , self.source
                                , self.company
                                , self.location
                                , self.imu_publisher
                                , join([ self.Company(x) for x in self.get_languages() ])
                                , join([ self.Series(x) for x in self.get_languages() ])
                                )

InitializeClass(IMUPublication)
