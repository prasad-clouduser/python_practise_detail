from silo_common.snippets.powershell import powershell_winrm

# logger debug Mode
do_debug_output = False

logfile = '/data/logs/sql_cluster_owner.log'

if do_debug_output is True:
    logger = em7_snippets.logger(filename=logfile)
else:
    logger = em7_snippets.logger(filename='/dev/null')

device_name = this_device.name
print("#####" + str(root_device))
logger.debug("**** [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + " Snippet Started ****")


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
            logger.error(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Error in PowerShell Command: " + str(error))
        else:
            return None
    except Exception as error:
        logger.error("[DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: " + " Error in PowerShell Connection: " + str(error))
try:

    RESULTS = {}
    # Get the cluster owner details query
    ps_request = "Get-ClusterGroup|Select-Object Cluster,Name,OwnerNode,State"
    logger.info("[DID:" + str(self.did) + "]:: PowerShell command executed:: " + str(ps_request))
    query_result = ps_query_result(ps_request, 'Name')

    if query_result:
        logger.info(" [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Cluster Owner Details : " + str(query_result))
        names = query_result['Name'].values()
        RESULTS['root_device'] = [('name', str(root_device.name.split('.')[0]))]
        RESULTS['host_name'] = [(name, str(root_device.name.split('.')[0])) for name in names]
        RESULTS['name'] = [(name, name) for name in names]
        RESULTS['cluster'] = [(name, query_result['Cluster'][name]) for name in names]
        RESULTS['owner_node'] = [(name, query_result['OwnerNode'][name]) for name in names]
        RESULTS['state'] = [(name, query_result['State'][name]) for name in names]
        result_handler.update(RESULTS)
        logger.info("[DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Cluster Owner Results: " + str(RESULTS))
except Exception as err:
    logger.error("[DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]: Error in Snippet Code : " + str(err))
logger.debug("**** [DID:" + str(self.did) + "],[App ID:" + str(self.app_id) + "]:  Snippet Closed ****")
