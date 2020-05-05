namenodes = {
    "Kerberized_Env": (["ENV_NN1", "ENV_NN2"], True),
    "Not_Secured_Env": (["ENV_NN1", "ENV_NN2"], False)
}

URI_QUERY = "jmx?qry=Hadoop:service=Namenode,name=NameNodeStatus"
WEBHDFS_DEFAULT_PORT = 50070
NAMENODE_URL = "http://{domain}:{port}/{uri}"

LISTENER = ('0.0.0.0', 8080)

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

ExceptionResponse = {"message": "An error occurred while querying for the active namenode."}

REFRESH_INTERVAL = 5 * 60.0
