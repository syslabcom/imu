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


factory_type_information = {'id'       : 'Research',
                            'meta_type' : 'IMU Research',
                            'description'   : ('Add a Research'),
                            'icon'      : 'research_icon.gif',
                            'product'   : 'IMU',
                            'factory'   : 'addResearch',
                            'filter_content_types' : 1,
                            'allowed_content_types' : ('File', 'Image', 'Link', 'I18NLayer'),
                            'immediate_view': 'research_edit_form',
                            'actions'   : (
                                {'id'       : 'view',
                                'name'     : 'View',
                                'action'   : 'string:${object_url}/research_view',
                                'permissions'  : (CMFCorePermissions.View,),
                                },
                                {'id'       : 'folderlisting',
                                 'name'     : 'Folder Listing',
                                 'action'   : 'string:${object_url}/research_view',
                                 'permissions' :( CMFCorePermissions.View,),
                                 'visible'  : 0
                                },
                                {'id'      : 'edit',
                                'name'    : 'Edit',
                                'action'  : 'string:${object_url}/research_edit_form',
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

def addResearch(self
             , id
             , title=''
             , description=''
             , localizer_languages=[]
             , default_language=''):
    """
    Create an empty Research.
    """
    if type(localizer_languages)!=type([]): localizer_languages = list(localizer_languages)
    preflang = self.portal_languages.getPreferredLanguage()
    if preflang not in localizer_languages:
        localizer_languages.append(preflang)
    if default_language=='':
        default_language = preflang
    o = IMUResearch(id
              , title=title
              , description=description
              , localizer_languages=localizer_languages
              , default_language=default_language
             )
    self._setObject(id, o)
    o._setPortalTypeName( 'Research' )
    return id


class IMUResearch(eITDocument):
    """
    An IMU Research.
    """
    portal_type = 'Research'
    meta_type = 'IMU Research'

    __implements__ = ( eITDocument.__implements__
                     , DynamicType
                     , IObjectEventPublisher
                     )

    isObjectEventPublisher = 1
    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(CMFCorePermissions.View)

    projectnumber = ''
    projecttype = ''
    manager=''
    mandant=''
    start_date = None
    end_date = None

    _properties = eITDocument._properties + (
          {'id': 'projectnumber', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'projecttype', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'manager', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'mandant', 'type':'string', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'start_date', 'type':'date', 'value': '', 'mode': 'w', 'mandatory': ''},
          {'id': 'end_date', 'type':'date', 'value': '', 'mode': 'w', 'mandatory': ''},
    )

    partner = LocalProperty('partner')
    financier = LocalProperty('financier')

    _local_properties_metadata = eITDocument._local_properties_metadata + (
                {'id': 'partner', 'type': 'text'},
                {'id': 'financier', 'type': 'text'},
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
        self.projectnumber = ''
        self.projecttype = ''
        self.manager = ''
        self.financier = ''
        self.mandant = ''
        self.partner = ''
        self.start_date = None
        self.end_date = None


    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'manage_edit' )
    def manage_edit( self
            , text_format
            , text=''
            , projectnumber = ''
            , projecttype=''
            , manager = ''
            , financier = ''
            , mandant=''
            , partner=''
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

        if localizer_language is None and request:
            localizer_language = request.get('edit_language', '')
        if localizer_language =='' and getattr(self, 'portal_languages', ''):
            localizer_language = self.portal_languages.getPreferredLanguage()

        self.setPartner(partner, localizer_language)
        self.setFinancier(financier, localizer_language)

        self.projectnumber = projectnumber
        self.projecttype = projecttype
        self.manager = manager
        self.mandant = mandant

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

    security.declarePublic( 'Partner' )
    def Partner( self, language=None ):
        "Partner of the research"
        return self._getAttributeFallback('partner', language)[0]

    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setPartner' )
    def setPartner( self, partner, language=None ):
        "set Partner of the Research"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None):
                language = self.portal_languages.getPreferredLanguage()
        if language!="" and language!=None:
            self._setLocalPropValue('partner', language, partner)
            if language==self.get_default_language():
                self.partner = partner
        else:
            if self.partner=="":
                self.partner = partner

    security.declarePublic( 'Financier' )
    def Financier( self, language=None ):
        "Financier of the research"
        return self._getAttributeFallback('financier', language)[0]

    security.declareProtected( CMFCorePermissions.ModifyPortalContent, 'setFinancier' )
    def setFinancier( self, financier, language=None ):
        "set Financier of the Research"
        if language=="" or language==None:
            if getattr(self, 'portal_languages', None):
                language = self.portal_languages.getPreferredLanguage()
        if language!="" and language!=None:
            self._setLocalPropValue('financier', language, financier)
            if language==self.get_default_language():
                self.financier = financier
        else:
            if self.financier=="":
                self.financier = financier

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
        return "%s %s %s %s %s %s %s %s %s %s" % ( self.id
                                , join([ self.Title(x) for x in self.get_languages() ])
                                , join([ self.Description(x) for x in self.get_languages() ])
                                , join([ self.portal_utilities.removeHTML(self.EditableBody(x)) for x in self.get_languages() ])
                                , self.projecttype
                                , self.projectnumber
                                , self.manager
                                , self.mandant
                                , join([ self.Financier(x) for x in self.get_languages() ])
                                , join([ self.Partner(x) for x in self.get_languages() ])
                                )

InitializeClass(IMUResearch)

