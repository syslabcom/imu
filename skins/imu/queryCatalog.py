## Script (Python) "queryCatalog"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=REQUEST=None,show_all=0,quote_logic=0,quote_logic_indexes=['SearchableText'],type_filter=[]
##title=wraps the portal_catalog with a rules qualified query
##
import string

results=[]
catalog=context.portal_catalog
indexes=catalog.indexes()
query={}
show_query=show_all
second_pass = {}

logit=context.portal_utilities.logit


if REQUEST is None:
    REQUEST = context.REQUEST
    
path = REQUEST.get('path', '')
portal_type = REQUEST.get('portal_type', '')

if getattr(path, 'append', ''):
    path = [x for x in path if x.strip() != '']
if len(path)==0:
    REQUEST.set('path', '')

def quotestring(s):
    return '"%s"' % s

def quotequery(s):
    if not s:
        return s
    try:
        terms = s.split()
    except:
        return s
    terms = s.split()
    tokens = ('OR', 'AND', 'NOT')
    s_tokens = ('OR', 'AND')
    check = (0, -1)
    for idx in check:
        if terms[idx].upper() in tokens:
            terms[idx] = quotestring(terms[idx])
    for idx in range(1, len(terms)):
        if (terms[idx].upper() in s_tokens and
            terms[idx-1].upper() in tokens):
            terms[idx] = quotestring(terms[idx])
    
    return ' '.join(terms)
    
def addasterisks(s):
    if not s:
        return s
    if s.strip()=='*':
        return ''
    try:
        terms = s.split()
    except:
        return s
    terms = s.split()
    tokens = ('OR', 'AND', 'NOT')
     
    for idx in range(0, len(terms)):
        if terms[idx].upper() not in tokens and terms[idx]!='*':
            if not terms[idx].startswith('*'):
                terms[idx] = "*%s" % terms[idx]
            if not terms[idx].endswith('*'):
                terms[idx] = "%s*" % terms[idx]
    return ' '.join(terms)
    
for k, v in REQUEST.items():
    
    if k.startswith('__display'):
        v=''
    if v and k in indexes:
        #if k=='SearchableText':
        #    v = addasterisks(v)
            
        if quote_logic and k in quote_logic_indexes:
            v = quotequery(v)
            
        if hasattr(v, 'append'):
            nv = []
            for i in v:
                if i.strip():
                    nv.append(v)
            if not nv:
                v = ''
        # The following 3 lines prevent ZCTextIndex from throwing a
        # ParseError - dirty, but it fixes the bug                
        if isinstance(v, basestring):
            v = string.replace(v, '(', ' ')
            v = string.replace(v, ')', ' ')    
        if k!='SearchableText':    
            query.update({k:v})
        else:
            if v!='':
                query.update({k:v})
        show_query=1    
    elif k.endswith('_usage'):
        key = k[:-6]
        param, value = v.split(':')
        second_pass[key] = {param:value}
    elif k.endswith('_level'):
        key = k[:-6]
        second_pass[key] = {'level':int(v)}
    elif k=='sort_on' or k=='sort_order':
        query.update({k:v})
        
for k, v in second_pass.items():
    qs = query.get(k)
    if qs is None:
        continue
    query[k] = q = {'query':qs}
    q.update(v)
    
    
if query.has_key('portal_type'):
    if 'all' in query['portal_type']:
        types = context.portal_types.listContentTypes()
        query.update({'portal_type':types})
        
if show_query:
    results=catalog(query)
        
return results    
    
    
    
    
    
    

