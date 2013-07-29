## Controller Python Script "publication_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters= text_format='', text='', imu_publisher='', imu_publisher_manual='', imu_in='', series='', number='', scope='', imu_author='', title='', SafetyBelt='', company='', location='', year='', isbn='', price='', source='', description='', id='', translation_complete=0, effective_date='', expiration_date=''
##title=Edit a Publication

request = context.REQUEST
if not id:
    id = context.getId()
if not title:
    title = context.Title()

if not text_format:
    text_format = context.text_format

if imu_publisher=='manual':
    imu_publisher = imu_publisher_manual
    request.set('imu_publisher', imu_publisher_manual)

new_context = context.portal_factory.doCreate(context, id)
new_context.plone_utils.contentEdit( new_context
                                   , id=id
                                   , title=title
                                   , description=description )

new_context.manage_edit( text_format = text_format
            , text=text
            , title=title
            , location=location
            , imu_publisher=imu_publisher
            , imu_in=imu_in
            , series=series
            , imu_author=imu_author
            , company=company
            , year=year
            , isbn=isbn
            , price=price
            , source=source
            , number=number
            , scope=scope
            , file=None
            , safety_belt=SafetyBelt
            , description=description
            , translation_complete=translation_complete
            , request=request )


return state.set(status='success', context=context, portal_status_message='Your Changes have been saved.')


