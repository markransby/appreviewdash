#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2
import feedcollect as fc
import webfunctions as wf

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        config = self.request.get("config", default_value='default')
        ourreviews = fc.populate_reviews(config)

        treemap = wf.treemapdata(ourreviews)
        appimages = wf.imagelist(ourreviews)
        versionaverages = wf.versionaverages(ourreviews)
        barchartdatasize = len(versionaverages)


        template_values = {
            'treemap_data': treemap,
            'versionaverages_data': versionaverages,
            'appimages': appimages,
            'reportdate': wf.today(),
            'barchartheight': barchartdatasize * 700 / 1200
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class TreeMapHandler(webapp2.RequestHandler):
    def get(self):
        config = self.request.get("config", default_value='default')
        ourreviews = fc.populate_reviews(config)

        treemap = wf.treemapdata(ourreviews)

        template_values = {
            'treemap_data': treemap,
        }

        template = JINJA_ENVIRONMENT.get_template('treemap.html')
        self.response.write(template.render(template_values))

class VersionRatingsHandler(webapp2.RequestHandler):
    def get(self):
        config = self.request.get("config", default_value='default')
        ourreviews = fc.populate_reviews(config)

        versionaverages = wf.versionaverages(ourreviews)
        barchartdatasize = len(versionaverages)


        template_values = {
            'versionaverages_data': versionaverages,
            'barchartheight': barchartdatasize * 700 / 1200
        }

        template = JINJA_ENVIRONMENT.get_template('versionratings.html')
        self.response.write(template.render(template_values))

class ReviewsJson(webapp2.RequestHandler):
    def get(self):
        config = self.request.get("config", default_value='default')
        ourreviews = fc.populate_reviews(config)
        self.response.write(wf.jsonreviews(ourreviews))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/treemap', TreeMapHandler),
    ('/versionratings', VersionRatingsHandler),
    ('/json', ReviewsJson)
], debug=True)
