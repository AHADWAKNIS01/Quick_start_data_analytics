import os, time, urllib.request, urllib.parse, json

host=os.getenv("COUCHBASE_ADMIN", "http://localhost:8091")
user=os.getenv("COUCHBASE_USER", "Administrator"); password=os.getenv("COUCHBASE_PASSWORD", "password")
def post(path, data):
    req=urllib.request.Request(host+path, data=urllib.parse.urlencode(data).encode(), method="POST")
    req.add_header("Authorization", "Basic "+(__import__('base64').b64encode(f"{user}:{password}".encode()).decode()))
    try: urllib.request.urlopen(req, timeout=5).read()
    except Exception as e: print(e)
for _ in range(30):
    try:
        post('/clusterInit', {'username':user,'password':password,'port':'8091','services':'kv,n1ql,index','memoryQuota':'512','indexMemoryQuota':'256','hostname':'127.0.0.1'})
        break
    except Exception: time.sleep(2)
post('/pools/default/buckets', {'name':'quickcart','bucketType':'membase','ramQuotaMB':'256','replicaNumber':'0','flushEnabled':'1'})
print('Couchbase initialized (existing resources are safe to reuse).')
