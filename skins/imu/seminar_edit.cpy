## Controller Python Script "event_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters= text_format='', text='', host='', location='', contact='', contact_email='', file='', SafetyBelt='', title='', description='', id='', translation_complete=0, effective_date='', expiration_date=''
##title=Edit a seminar

request = context.REQUEST
if not id:
    id = context.getId()
if not title:
    title = context.Title()
    
if not text_format:
    text_format = context.text_format

new_context = context.portal_factory.doCreate(context, id)
new_context.plone_utils.contentEdit( new_context
                                   , id=id
                                   , title=title
                                   , description=description )
                                   

effective_date = '%s %s:%s' % (effective_date.split(' ')[0], request.get('effective_date_hour', '0'), request.get('effective_date_minute', '0'))
expiration_date = '%s %s:%s' % (expiration_date.split(' ')[0], request.get('expiration_date_hour', '0'), request.get('expiration_date_minute', '0'))
                                   
new_context.manage_edit( text_format = text_format
            , text=text
            , title=title
            , location=location
            , contact=contact
            , contact_email=contact_email
            , host=host
            , start_date=effective_date
            , end_date=expiration_date
            , file=None
            , safety_belt=SafetyBelt
            , description=description
            , translation_complete=translation_complete
            , request=request )           
            
return state.set(status='success', context=context, portal_status_message='Your Changes have been saved.')


