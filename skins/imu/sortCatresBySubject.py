## Script (Python) "sortCatresBySubject"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=glist=[]
##title=return list of mandants

resmap = {}
resmap['no_category'] = []

sortSequence = context.sortSequence

logit = context.portal_utilities.logit
for brain in glist:
    subjs = brain.Subject
    if not subjs:
        resmap['no_category'].append(brain)
    else:
        for s in subjs:
            if resmap.has_key(s):
                resmap[s].append(brain)
            else:
                resmap[s] = [brain]

for k in resmap.keys():
    kresults = resmap[k]
    kresults.sort(lambda x, y: cmp(x.EffectiveDate, y.EffectiveDate))
    kresults.reverse()

return resmap

