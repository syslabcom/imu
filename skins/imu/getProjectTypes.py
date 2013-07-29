## Script (Python) "getProjectTypes"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=return list of project types

ptypes = {  'Auftragsforschung':'Auftragsforschung',
            'Sachverstand':'Sachverstand',
            'Seminare':'Seminare',
            'Grundlagenforschung':'Grundlagenforschung',
            'zweckbetr. Forschung':'zweckbetr. Forschung'}
   
return ptypes
