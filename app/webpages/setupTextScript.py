# Shamelessly copied from https://gelnior.wordpress.com/2012/05/23/whoosh-full-text-search-for-python/
import os
 
from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir, exists_in
from whoosh.query import Term
from whoosh.qparser import QueryParser
from pymongo import MongoClient
from bson.objectid import ObjectId

# Set up mongoClient and to DB compareDB and to collection phones
mongo = MongoClient('localhost', 27017)['compareDB']
products = mongo.phones

# Set index, we index title and content as texts and tags as keywords.
# We store inside index only titles and ids.
schema = Schema(productname=TEXT(stored=True),
                nid=ID(stored=True))

# Create index dir if it does not exists.
if not os.path.exists("index"):
    os.mkdir("index")

# Initialize index
ix = create_in("index", schema)
ix = open_dir("index")
# Fill index with posts from DB
writer = ix.writer()

for product in products.find():
    try:
    	fullProductName = product["Brand"] + " " + product["Model Name"]
    	writer.add_document(productname=fullProductName,
                           nid=unicode(product["_id"]))
    except:
    	print product["Brand"],  product["Model Name"]
    writer.add_document(productname=fullProductName,
                           nid=unicode(product["_id"]))
    
writer.commit(optimize=True)
exists = exists_in("index")


# results = ix.searcher().documents()
# for result in results:
# 	print result


query = QueryParser("productname", schema=ix.schema).parse(u"5c iphone Apple")
productSearchList = []
with ix.searcher() as searcher:
	results = searcher.search(query, limit=None)
	i=0
	productSearchList = [result["nid"] for result in results]
print productSearchList
        # result = searcher.search(Term("productname", "Apple"))
    # post = posts.find_one(ObjectId(result["nid"]))
        # print result
    # print post["content"]
