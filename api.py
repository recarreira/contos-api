import tornado.ioloop
import tornado.web
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId

MONGODB_DB_URL = 'mongodb://localhost:27017/'
MONGODB_DB_NAME =  'stories'

client = MongoClient(MONGODB_DB_URL)
db = client[MONGODB_DB_NAME]

settings = {
    "debug" : True
}


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class StoriesHandler(tornado.web.RequestHandler):
    def get(self):
        stories = db.stories.find()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list(stories),default=json_util.default, sort_keys=True, indent=4))


application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/stories',StoriesHandler),
],**settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()