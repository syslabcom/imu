import Globals, sys
from os import path
from Products.CMFCore import DirectoryView, utils
from AccessControl import ModuleSecurityInfo

# esc: allow import of module "csv" in scripts
from Products.PythonScripts.Utility import allow_module
allow_module('csv')
# /esc

module_globals = globals()
ADD_CONTENT_PERMISSION = 'Add portal content'

DirectoryView.registerDirectory('skins', module_globals)

misc_ = {'IMU_icon': Globals.ImageFile(path.join('skins',
                                                  'imu',
                                                  'logoIcon.gif'),
                                                   module_globals)}
                                                   
def initialize(context):
    from Products.IMU import IMUResearch, IMUSeminar, IMUPublication, IMUConsulting
    security = ModuleSecurityInfo( 'Products.IMU.utils' )
    security.declareObjectPublic()
    security.declarePublic('uploadProjectsFromFile')
    security.declarePublic('getProjects')
    security.declarePublic('checkProjectId')

    contentClasses = ( IMUResearch.IMUResearch, 
                       IMUSeminar.IMUSeminar,
                       IMUPublication.IMUPublication,
                       IMUConsulting.IMUConsulting 
                       )
                       
    contentConstructors = ( IMUResearch.addResearch,
                            IMUSeminar.addSeminar,
                            IMUPublication.addPublication,
                            IMUConsulting.addConsulting
                            )
                            
    ftis = ( IMUResearch.factory_type_information,
             IMUSeminar.factory_type_information,
             IMUPublication.factory_type_information,
             IMUConsulting.factory_type_information
             )
             
    this_module = sys.modules[ __name__ ]
    
    bases = contentClasses
    z_bases = utils.initializeBasesPhase1(bases, this_module)

    utils.initializeBasesPhase2( z_bases, context )
    
    utils.ContentInit( 'IMU Content'
                     , content_types=contentClasses
                     , permission=ADD_CONTENT_PERMISSION
                     , extra_constructors=contentConstructors
                     , fti=ftis
                     ).initialize( context )

