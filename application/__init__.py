from flask import Flask
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app = Flask(__name__)
bundlepath = 'application/secure-connect-datn.zip'
clientId = 'PKUrqlvgFpAippRORPhslTCP'
clientSecret = '4NnPaNpsB8Z_SpdTUX7hFy3UHmCfZtmB_Xrs7K21,WmxMJTTjzmZXqfwFNqTETCZ6f2nj6sL_h1KNc6xrokZtkIUlekoraJiZygUBlcrvlNKfQ13KtkbIvuv4qm9ZSWZ'

cloud_config= {
    'secure_connect_bundle': bundlepath
}
auth_provider = PlainTextAuthProvider(clientId, clientSecret)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
from application import routes

