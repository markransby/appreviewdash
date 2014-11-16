import feedfunctions as ff

class Review(object):

    def __init__(self, appname, product, rating, title, comment, appversion, image, reviewid, color, makebig, showicon):
        self.appname = appname
        self.product = product
        self.rating = int(rating)
        self.title = title
        self.comment = comment
        self.appversion = appversion
        self.image = image
        self.reviewid = reviewid
        self.color = color
        self.makebig = makebig
        self.showicon = showicon

    def print_summary(self):
        toret = self.appname + " " + self.rating + " " + self.title
        return unicode(toret)



def populate_reviews(config):
    listofreviews = list()
    applist = ff.get_apps(config)
    for app in applist:
        appname = app["name"]
        product = app["product"]
        color = app["color"]
        makebig = app["makebig"]
        showicon = app["showicon"]
        appfeed = ff.get_feed(app["id"])
        if "entry" in appfeed["feed"]:
            image = appfeed["feed"]["entry"][0]["im:image"][2]["label"]
            numentries = len(appfeed["feed"]["entry"])
            for entrynum in range(1, numentries):
                rating = appfeed["feed"]["entry"][entrynum]["im:rating"]["label"]
                title = appfeed["feed"]["entry"][entrynum]["title"]["label"]
                comment = appfeed["feed"]["entry"][entrynum]["content"]["label"]
                appversion = appfeed["feed"]["entry"][entrynum]["im:version"]["label"]
                reviewid = appfeed["feed"]["entry"][entrynum]["id"]["label"]
                listofreviews.append(Review(appname, product, rating, title, comment, appversion, image, reviewid, color, makebig, showicon))
    return listofreviews

