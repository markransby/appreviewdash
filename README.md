appreviewdash
=============

Aggregate and visualise IOS app store reviews

Google App Engine application

Implements 4 endpoints:

/               ...show the dashboard
/treemap        ...just show the treemap visualisation
/versionratings ...just show the bar chart
/json           ...dump the review objects (handy for saving history with curl under cron)

All endpoints accept a config parameter to allow you to serve different audiences from the same instance.

Base URL is hardcoded in feedfunctions.py,
Looks for default.json as standard, or the parameter allows override to ???.json

Probably better to accept a URL as the parameter... TODO

