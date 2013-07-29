## Controller Python Script "consulting_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters= text_format='', text='', client='', period='', contact='', title='', SafetyBelt='', description='', id='', translation_complete=0, effective_date='', expiration_date=''
##title=Edit a Consulting case

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
                                   
new_context.manage_edit( text_format = text_format
            , text=text
            , title=title
            , client=client
            , contact=contact
            , period=period
            , file=None
            , safety_belt=SafetyBelt
            , description=description
            , translation_complete=translation_complete
            , request=request )           
            
return state.set(status='success', context=context, portal_status_message='Your Changes have been saved.')


