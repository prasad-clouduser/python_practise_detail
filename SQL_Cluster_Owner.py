from silo_common.snippets.powershell import powershell_winrm

# logger debug Mode
do_debug_output = False

logfile = '/data/logs/sql_cluster_owner.log'

if do_debug_output is True:
    logger = em7_snippets.logger(filename=logfile)
else:
    logger = em7_snippets.logger(filename='/dev/null')

device_name = this_device.name

logger.debug("**** [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + " Snippet Started ****")
logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Device Info: " + str(device_name))


# returns the Cluster Owner details
def ps_query_result(ps_request, uniq_column_in_query):
    logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Make a Connection to PowerShell on Target Server")
    Request = namedtuple('Request', 'req_id key_column request app_id')
    request = Request(-1, uniq_column_in_query, ps_request, self.app_id)
    try:
        ps_query_result, error = powershell_winrm(self.did, self.ip, request, self.cred_details, True, None, None,self.logger)
        if ps_query_result is not None and ps_query_result:
            logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: PowerShell Connection Established Successfully")
            return ps_query_result
        elif error:
            logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Error in PowerShell Command: " + str(error))
        else:
            return None
    except Exception as error:
        logger.debug("[DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: " + " Error in PowerShell Connection: " + str(error))


try:

    results = {}

    # Get the cluster owner details query
    ps_request = """$cluster_group = Get-ClusterGroup | select-object Cluster, Name, OwnerNode, State | format-list *
    Write-output $cluster_group"""

    ps_request_resource = """$cluster_group = $cluster_resource = Get-ClusterResource | Select-Object Name, OwnerGroup, ResourceType | format-list *
    Write-output $cluster_resource"""

    print("PS Request:", str(ps_request))
    query_result = ps_query_result(ps_request, 'Name')
    print("Query Result: ", str(query_result))
    logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Cluster Group query results: " + str(query_result))

    query_result_resource = ps_query_result(ps_request_resource, 'Name')
    print("PS Request:", str(ps_request_resource))
    print("Query Result: ", str(query_result_resource))
    logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Cluster resources query results: " + str(query_result_resource))

    results = {"GroupName": [], "ClusterName": [], "ClusterState": [], "OwnerNode": [], "ResourceType": []}

    # First extract the individual dictionaries
    group_name = cluster_group['Name']
    cluster_name = cluster_group['cluster']
    owner_node = cluster_group['ownernode']
    cluster_state = cluster_group['state']

    # These are the lists that will be plugged into result_handler
    groupname = []
    clustername = []
    clusterstate = []
    ownernode = []
    resourcetype = []

    for key in group_name.keys():

        if (key in cluster_name) and (key in owner_node) and (key in cluster_state):
            index = str(key)
            groupname.append((index, group_name[index]))
            clustername.append((index, cluster_name[index]))
            clusterstate.append((index, cluster_state[index]))
            ownernode.append((index, owner_node[index]))
        else:
            print("Data Consistency Error")

    list_groups = cluster_group['Name'].values()
    print("list groups: ", str(list_groups))
    logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: List all groups: " + str(list_groups))
    print("cluster resource owner groups : ", str(cluster_resource['ownergroup'].values()))
    logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: cluster resource owner groups: " + str(cluster_resource['ownergroup'].values()))

    for each in list_groups:
        resources = []
        logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Group name: " + each)
        if each in str(cluster_resource['ownergroup'].values()):
            for key, value in cluster_resource['ownergroup'].items():
                if value == each:
                    resources.append(cluster_resource['resourcetype'][key])
            resources_unique = set(resources)
            resources_join = ",".join(resources_unique)
            logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: all resource types: " + str(resources_join) + " for the group: " + str(each))
            resourcetype.append((each, resources_join))
        else:
            resourcetype.append((each, "No Resources"))
        logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Resources for the group: " + str(resources))

    logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: resource types populated in the result handler: " + str(resourcetype))

    results['GroupName'] = groupname
    results['ClusterName'] = clustername
    results['ClusterState'] = clusterstate
    results['OwnerNode'] = ownernode
    results['ResourceType'] = resourcetype

    print("Final Results: ", str(results))
    logger.debug(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Final results of the cluster: " + str(results))

    result_handler.update(results)

except Exception as err:
    logger.debug("[DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Error in Snippet Code : " + str(err))
logger.debug("**** [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]:  Snippet Closed ****")
