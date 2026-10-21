import argparse, json, os
from datetime import datetime, timezone, timedelta
from pyspark.sql import SparkSession, functions as F

def main():
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['sample','full'],default='sample'); p.add_argument('--input',required=True); p.add_argument('--output',default='data/processed'); p.add_argument('--publish',choices=['none','couchbase'],default='none'); a=p.parse_args()
    # Native Windows Spark needs Hadoop's small filesystem helper for Parquet writes.
    # The repository includes it so students do not need a separate Hadoop install.
    if os.name == 'nt':
        java_home = r'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
        if os.path.isdir(java_home):
            os.environ.setdefault('JAVA_HOME', java_home)
            os.environ['PATH'] = os.path.join(java_home, 'bin') + os.pathsep + os.environ.get('PATH', '')
        hadoop_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools', 'hadoop'))
        os.environ.setdefault('HADOOP_HOME', hadoop_home)
        os.environ.setdefault('hadoop.home.dir', hadoop_home)
    os.environ.setdefault('SPARK_LOCAL_IP', '127.0.0.1')
    spark=SparkSession.builder.appName('QuickCartAnalytics').master('local[2]').config('spark.driver.host','127.0.0.1').config('spark.driver.bindAddress','127.0.0.1').config('spark.sql.shuffle.partitions','4').getOrCreate()
    def read(name): return spark.read.option('header',True).option('inferSchema',True).csv(os.path.join(a.input,name))
    orders=read('orders.csv'); products=read('products.csv'); departments=read('departments.csv');
    prior=read('order_products__prior.csv'); train=read('order_products__train.csv'); lines=prior.unionByName(train)
    joined=lines.join(orders,'order_id').join(products,'product_id').join(departments,'department_id','left')
    kpis=joined.agg(F.countDistinct('order_id').alias('orders'),F.countDistinct('user_id').alias('customers'),F.count('*').alias('items'),F.avg('reordered').alias('reorder_rate')).collect()[0].asDict()
    hourly=joined.groupBy('order_hour_of_day').agg(F.count('*').alias('items')).orderBy('order_hour_of_day')
    days=joined.groupBy('order_dow').agg(F.count('*').alias('items')).orderBy('order_dow')
    departments_out=joined.groupBy('department_id','department').agg(F.count('*').alias('items'),F.avg('reordered').alias('reorder_rate')).orderBy(F.desc('items'))
    products_out=joined.groupBy('product_id','product_name','department_id','department').agg(F.count('*').alias('items'),F.avg('reordered').alias('reorder_rate')).orderBy(F.desc('items')).limit(20)
    os.makedirs(a.output,exist_ok=True)
    frames={'hourly':hourly,'days':days,'departments':departments_out,'products':products_out}
    for n,df in frames.items(): df.write.mode('overwrite').parquet(os.path.join(a.output,n))
    meta={'dataset':a.mode,'generated_at':datetime.now(timezone.utc).isoformat(),'source':'Instacart Online Grocery Shopping Dataset 2017','batch_type':'local batch'}
    with open(os.path.join(a.output,'metadata.json'),'w') as f: json.dump(meta,f)
    kpis={k:float(v) if isinstance(v,float) else int(v) for k,v in kpis.items()}; docs={'metadata':meta,'kpis':kpis}
    for n,df in frames.items(): docs[n]={'dataset':a.mode,'data':[r.asDict() for r in df.collect()]}
    with open(os.path.join(a.output,'docs.json'),'w') as f: json.dump(docs,f)
    if a.publish=='couchbase':
        from couchbase.cluster import Cluster
        from couchbase.auth import PasswordAuthenticator
        from couchbase.options import ClusterOptions
        c=Cluster.connect(os.getenv('COUCHBASE_CONNSTR','couchbase://localhost'),ClusterOptions(PasswordAuthenticator(os.getenv('COUCHBASE_USER','Administrator'),os.getenv('COUCHBASE_PASSWORD','password')))); c.wait_until_ready(timeout=timedelta(seconds=20)); col=c.bucket(os.getenv('COUCHBASE_BUCKET','quickcart')).default_collection()
        for n,d in docs.items(): col.upsert('quickcart::'+n,d)
        print('Published analytics documents to Couchbase.')
    print(json.dumps({'mode':a.mode,'kpis':kpis})); spark.stop()
if __name__=='__main__': main()
