# IMU utility methods
import csv, types
from StringIO import StringIO
from AccessControl import ModuleSecurityInfo
from DateTime import DateTime

def checkProjectId(folder, pid, mandant):
    """
    check the imu combination id/mandant for a research object
    if an object with this combination already exists. then upgrade or remove the object
    """
    pobjid = ''
    opid = ''

    if len(pid)<5:
        return (pobjid, opid)
    pid_part = pid[:5]

    ptool = folder.portal_url
    portal = ptool.getPortalObject()
    ctool = portal.portal_catalog

    fpath = ptool.getPortalPath()+'/'+ptool.getRelativeUrl(folder)

    catres = ctool( {'portal_type':'Research'
                          , 'path':fpath
                          , 'projectnumber':pid_part+'*'
                          , 'mandant':mandant} )

    for c in catres:
        cobj = c.getObject()

        opid = cobj.projectnumber

        if opid==pid: # identisches projekt -> ersetzen
            pobjid = cobj.getId()
            break
        else:
            onum = int(opid[5:])
            nnum = int(pid[5:])

            if onum < 90: # altes projekt im upgradebeich
                if nnum < 90:   # neues projekt im upgradebeich -> upgrade
                    pobjid = cobj.getId()
                    break
                else: # neues projekt im archiv bereich -> neu anlegen
                    pobjid = ''
            else: # altes projekt im archiv bereich -> neu anlegen
                pobjid = ''

    return (pobjid, opid)

def getProjects(fp):
    """
    Return dictionary list with project values
    """
    fn      =   ['Mandant', 'Projekt', 'Kurztitel', 'Titel', 'Projektart', 'Beginn', 'Ende', 'Abgabe', 'W\xe4hrung', 'Leitung', 'Zuordnung', 'Kurzinhalt', 'Partner', 'Geldgeber']
    fnused  =   {'Mandant':'mandant', 'Projekt':'projectnumber', 'Kurztitel':'title', 'Titel':'description', 'Projektart':'projecttype', 'Beginn':'start_date', 'Ende':'end_date', 'Leitung':'manager','Kurzinhalt':'bodytext', 'Partner':'partner', 'Geldgeber':'financier'}

    class imucsv(csv.Dialect):
        delimiter = '\t'
        quotechar = '"'
        doublequote = False
        skipinitialspace = True
        lineterminator = '\r\n'
        quoting = csv.QUOTE_MINIMAL

    csv.register_dialect("imucsv", imucsv)


    reader=csv.DictReader(fp,fn,dialect="imucsv")
    retval=[]

    i=0


    for row in reader:
        prj_dict={}
        for key in row:
            if fnused.has_key(key):
                prj_dict[fnused[key]]=row[key]

        # do not add first record (header):
        if i>0: retval.append(prj_dict)
        i+=1

    return retval
