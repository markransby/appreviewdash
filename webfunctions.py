from __future__ import division
import feedcollect as fc
import json
import datetime



def imagelist(listofreviews):
    imagelist = list()
    for review in listofreviews:
        if review.image not in imagelist:
            if review.showicon:
                imagelist.append(review.image)
    return imagelist


def today():
    today = datetime.date.today()
    return today.strftime('%d/%m/%Y')

def getproductlist(listofreviews):
    productlist = list()
    for review in listofreviews:
        if review.product not in productlist:
            productlist.append(review.product)
    return productlist


def makeunique(idlist, id):    # Function to make an ID unique by appending underscores. App review titles like "crashes" or "excellent" tend to repeat
    if id not in idlist:
        return id
    else:
        return makeunique(idlist, id + "_")

def treemapdata(listofreviews):
    listoflists = list()
    idlist = ['Title','All','CBeebies','CBBC']   # Setup the list of unique IDs... visualisation barfs if two things have the same ID
    listoflists.append(['Title','Parent','Rating','Rating2'])
    listoflists.append(['All','',0,0])
    for product in getproductlist(listofreviews):
        listoflists.append([product,'All',0,0])
    currentapp = str()
    for review in listofreviews:
        if review.appname != currentapp:
            listoflists.append([review.appname, review.product, 0, 0])
            currentapp = review.appname
            idlist.append(review.appname)
        uniqueid = makeunique(idlist, review.title)
        listoflists.append([uniqueid, review.appname, 0, 0])
        idlist.append(uniqueid)
        uniqueid2 = makeunique(idlist, str(review.rating) + " Stars: " + review.comment)
        if review.makebig:        # Make the products you care about larger in the treemap
            listoflists.append([uniqueid2, uniqueid, 10000 + review.rating, review.rating])  #treemap inserts rectangles by decreasing size, so this keeps ratings grouped by score
        else:
            listoflists.append([uniqueid2, uniqueid, 1000 + review.rating, review.rating])
        idlist.append(uniqueid2)

    return json.dumps(listoflists, ensure_ascii=True)

def versionaverageshelper(vah_listofreviews, listofvalues, current, currentcolor, reviewcount, reviewtotal):
    review = vah_listofreviews.pop()
    label = review.appname + " " + review.appversion
    color = review.color
    if label != current:
        listofvalues.append([current, reviewtotal / reviewcount, currentcolor])
        current = label
        currentcolor = color
        reviewcount = 0
        reviewtotal = 0
    reviewcount += 1
    reviewtotal += review.rating
    if len(vah_listofreviews) == 0:
        listofvalues.append([current, reviewtotal / reviewcount, currentcolor])
        listofvalues.reverse()
        return listofvalues
    else:
        return versionaverageshelper(vah_listofreviews, listofvalues, current, currentcolor, reviewcount, reviewtotal)

def versionaverages(listofreviews):
    va_listofreviews = list(listofreviews)     # copy the list to stop .pop() deleting our data
    listofresults = list()
    rolestyledict = {}
    rolestyledict["role"] = "style"
    listofresults.append(["App Version", "Rating", rolestyledict])
    firstreview = va_listofreviews[0]
    current = firstreview.appname + " " + firstreview.appversion
    currentcolor = firstreview.color
    va_listofreviews.reverse()
    for result in (versionaverageshelper(va_listofreviews, list(), current, currentcolor, 0, 0)):
        listofresults.append(result)
    return json.dumps(listofresults, ensure_ascii=True)

def jsonreviews(listofreviews):
    listofdicts = list()
    for review in listofreviews:
        listofdicts.append(review.__dict__)
    return json.dumps(listofdicts, ensure_ascii=True)
