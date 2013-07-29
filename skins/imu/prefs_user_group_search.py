## Script (Python) "prefs_user_group_search"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=searchstring, restrict, return_form=None
##title=Extensive Search for Users.
##


#MembershipTool.searchForMembers
groups_tool = context.portal_groups
membership_tool = context.portal_membership
memberdata_tool = context.portal_memberdata
from_utf8 = context.portal_utilities.from_utf8
ldapatt = context.portal_properties.site_properties.getProperty('ldap_quicksearch_attr', None)
retlist = []

if not searchstring:
    if restrict != "groups":
        memberlist = retlist + membership_tool.listMembers()
    
        for m in memberlist:
            retlist.append( { 'username': m.getProperty( 'id' )
                            , 'email' : m.getProperty( 'email', '' )
                            , 'fullname' : m.getProperty( 'fullname', '' )
                            , 'found_in' : 'memberdata'
                            } )
    if restrict != "users":
        retlist = retlist + groups_tool.listGroups()
else:
    # take * as wildcard
    if searchstring.strip() == '*':
        searchstring = ''
    search_list = searchstring.split(' ')  
    query = None
    if ldapatt is not None:
        query = '(&'
        for v in search_list:
           v = v.lower().strip()
           query +='(|'
           for a in ldapatt:
               query += '(%s=%s*)' % (a,from_utf8(v))
           query += ')'
        query += ')'
        
    if restrict != "groups":
        retlist = retlist + memberdata_tool.searchMemberDataContents(search_param=None, search_term=searchstring, ldapQuery=query, memberDataOnly=None)
    if restrict != "users":
        retlist = retlist + groups_tool.searchForGroups(REQUEST=None, name=searchstring)

# reorder retlist?
if return_form:
    context.REQUEST.RESPONSE.redirect( context.absolute_url() + '/' + return_form )
return retlist
