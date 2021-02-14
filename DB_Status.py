from silo_common.snippets.powershell import powershell_winrm
from silo_sql_server.powershell_instance import PowerShellException, PowerShellEmptyKey

ERROR_CODE = 519  # snippet error
app_name = "SQL Server Database Configuration"
snippet_name = "get-db-basic-config"

ps_request = """
Add-PSSnapin SqlServerCmdletSnapin100 -ErrorAction SilentlyContinue
Add-PSSnapin SqlServerProviderSnapin100 -ErrorAction SilentlyContinue
Function GetProperty($sql, $propertyKey, $propertyValue){
    $response = "";
    $response += "sqlinstance : $($sql)`r`n";
    $response += "$($propertyKey) : $($propertyValue)`r`n`r`n";
    return $response
}
$output =  "`r`n`r`n";
$instance = "@instance_name";
$network_name = "@network_name";
$server =".\";
if ($network_name -eq "") {
    if ($instance -ne "MSSQLSERVER") {
        $server = "$($env:computername)\$($instance)"
    }
} else {
    $server = $network_name;
}

$SqlQuery = "select sd.name, sd.version, db.collation_name, db.state_desc
             from sys.sysdatabases as sd
             join sys.databases as db
             on db.name=sd.name;"

$query_results = Invoke-Sqlcmd -ServerInstance $server -Database "master" -Query $SqlQuery -WarningAction SilentlyContinue

foreach($row in $query_results) {
    $sqlkey = "$($instance).$($row.name)"
    $output += GetProperty $sqlkey "name" $row.name;
    $output += GetProperty $sqlkey "state_desc" $row.state_desc;
    $output += GetProperty $sqlkey "db_state_desc" $row.state_desc;
}
Write-Output $output"""


def send_alert(message):
    alert_message = "[AppID {}] {}".format(self.app_id, message)
    self.internal_alerts.append((ERROR_CODE, alert_message))


def get_sql_instances_and_network_names():
    # Return data structure used to invoke ps_request for each sql instance/network name combination
    # Clustered SQL instances:
    #   { <sql instance 1> : <network name 1>,
    #     <sql instance 2> : <network name 2>,
    #     ...
    #   }
    #
    # Non-clustered SQL instances:
    #   { <sql instance 1> : '',
    #     <sql instance 2> : '',
    #     ...
    #   }
    sql_instances_and_network_names = {}

    # Find all SQL instances included in the device list
    for did, device_values in self.devices.iteritems():
        temp_instance_name = get_sql_instance_from_component_unique_id(device_values[0].unique_id)
        if len(temp_instance_name) > 0:
            temp_comp_dn = device_values[0].dn
            # If this database is on a clustered SQL instance,
            #    get the network name
            if (temp_comp_dn and len(temp_comp_dn) > 1):
                # dn value:
                #   clustered named instance: Server\\Instance@IP
                #   clustered default instance: Server@IP
                temp_network_name = temp_comp_dn.split('@', 1)[0]
            else:
                # for a non clustered SQL instance, leave network name as an empty string
                temp_network_name = ''
            sql_instances_and_network_names[temp_instance_name] = temp_network_name
    self.logger.ui_debug(
        "{} [{}] {}: Found SQL instances and network names: {}".format(app_name, self.app_id, snippet_name,
                                                                       sql_instances_and_network_names))

    return sql_instances_and_network_names


def get_sql_instance_from_component_unique_id(unique_id):
    # Parse a component unique id value and return the sql instance
    #   ex. "SqlDatabase.<sql instance>.<database name>.<root did>  -> <sql instance>
    # Note that <database name> may contain '.' characters itself
    instance_name = ''
    temp_unique_id = unique_id.replace('SqlDatabase.', '')  # Remove SqlDatabase prefix
    new_uid = temp_unique_id[:temp_unique_id.rfind('.')]  # Strip off the root device ID
    if new_uid:
        # Split on the first . and ensure the length in response is two items
        final_uid = new_uid.split('.', 1)
        if final_uid and len(final_uid) == 2:
            instance_name = final_uid[0]

    if len(instance_name) == 0:
        parse_error_msg = "Could not parse component unique id: {}".format(unique_id)
        self.logger.ui_debug("{} [{}] {}: {}".format(app_name, self.app_id, snippet_name, parse_error_msg))

    return instance_name


def get_sql_instance_and_db_name_from_component_unique_id(unique_id):
    # Parse a component id value and return the sql instance and database name
    #   ex. "SqlDatabase.<sql instance>.<database name>.<root did> ->  <sql instance>.<database name>
    # Note that <database name> may contain '.' characters itself
    instance_and_db = ''
    temp_unique_id = unique_id.replace('SqlDatabase.', '')  # Remove SqlDatabase prefix
    new_uid = temp_unique_id[:temp_unique_id.rfind('.')]  # Strip off the root device ID
    if new_uid:
        instance_and_db = new_uid

    if len(instance_and_db) == 0:
        parse_error_msg = "Could not parse component unique id: {}".format(unique_id)
        self.logger.ui_debug("{} [{}] {}: {}".format(app_name, self.app_id, snippet_name, parse_error_msg))

    return instance_and_db


def query_single_sql_instance(sql_instance, network_name):
    # Issue PowerShell request to the target device
    #   to retrieve all database backup information for a single sql instance

    substituted_powershell = ps_request.replace('@network_name', network_name)
    substituted_powershell = substituted_powershell.replace('@instance_name', sql_instance)

    Request = namedtuple('Request', 'req_id key_column request app_id')
    request = Request(-1, 'sqlinstance', substituted_powershell, self.app_id)
    query_result, error = powershell_winrm(self.did, self.ip, request, self.cred_details, True, None, None, self.logger)

    self.logger.ui_debug(
        "{} [{}] {}: SQL instance: {}, PowerShell results: {}".format(app_name, self.app_id, snippet_name, sql_instance,
                                                                      query_result))
    if error:
        self.logger.ui_debug(
            "{} [{}] {}: SQL instance: {}, PowerShell execution error: {}".format(app_name, self.app_id, snippet_name,
                                                                                  sql_instance, error))
        send_alert(error)

    return query_result


def group_results_by_component(query_result):
    # Restructure the results to have the component names as the top-level elements
    #   rather than the collection object names.
    #   This simplifies writing the results to the result handler.

    results_grouped_by_component = {}
    # Find all <sql instance>.<database name> result keys in the results
    for results_key in query_result['sqlinstance']:
        # Note that the result key is not the complete component unique identifier,
        #     but can be used to identify the component when looping over the device list
        results_key_upper = results_key.upper()
        if results_key_upper not in results_grouped_by_component:
            results_grouped_by_component[results_key_upper] = {}
    self.logger.ui_debug("{} [{}] {}: Component identifiers found: {}".format(app_name, self.app_id, snippet_name,
                                                                              results_grouped_by_component))

    # Loop over the remaining results and insert them under the corresponding component key by metric
    #    { <sql instance>.<db name> : { <metric> : [(<sql instance>.<db name>, <metric value>),],
    #                                   <metric> : [(<sql instance>.<db name>, <metric value>),], ...
    #                                 }
    #      <sql instance>.<db name> : { <metric> : [(<sql instance>.<db name>, <metric value>),], ...
    #                                 }
    #    }
    for metric, instances_and_values_dict in query_result.iteritems():
        if metric != 'sqlinstance':
            for results_key, item_value in instances_and_values_dict.iteritems():
                results_key_upper = results_key.upper()
                if metric not in results_grouped_by_component[results_key_upper]:
                    results_grouped_by_component[results_key_upper][metric] = []
                results_grouped_by_component[results_key_upper][metric].append((results_key, item_value))
    self.logger.ui_debug("{} [{}] {}: Grouped instance results: {}".format(app_name, self.app_id, snippet_name,
                                                                           results_grouped_by_component))

    return results_grouped_by_component


def insert_results_into_result_handler(complete_results):
    # Write the collected results for all SQL instances into the result handler structure
    #   result_handler[(<device id>, <collection object name>)] = [(<index>, <data value>), (<index>, <data value>), ...]

    for did, device_values in self.devices.iteritems():
        temp_comp_id = device_values[0].unique_id
        temp_component_key = get_sql_instance_and_db_name_from_component_unique_id(temp_comp_id).upper()
        if temp_component_key in complete_results:
            if did in self.oids:
                for group_id, group_objects in self.oids[did].iteritems():
                    for object_id, object_details in group_objects.iteritems():
                        if object_details['oid'] == 'state_disc':
                            if object_details['oid'] in complete_results[temp_component_key] and object_details['oid'] == 'state_disc':
                                metric_oid = object_details['oid']
                                metric_values = complete_results[temp_component_key][metric_oid]
                                self.logger.ui_debug("{} [{}] {}: Device: {} [{}], metric: {}, results: {}".format(app_name, self.app_id,snippet_name,temp_component_key, did,object_details['name'],metric_values))
                                result_handler[(did, metric_oid)] = metric_values
                        elif object_details['oid'] == 'db_state_disc':
                            if object_details['oid'] in complete_results[temp_component_key] and object_details['oid'] == 'state_disc':
                                metric_oid = object_details['oid']
                                metric_values = complete_results[temp_component_key][metric_oid]
                                self.logger.ui_debug("{} [{}] {}: Device: {} [{}], metric: {}, results: {}".format(app_name, self.app_id,snippet_name,temp_component_key, did,object_details['name'],metric_values))
                                result_handler[(temp_component_key, metric_oid)] = metric_values
            else:
                self.logger.ui_debug(
                    "{} [{}] {}: Device: {} [{}] - Not found in object id structure.  Not including device in results.".format(
                        app_name, self.app_id, snippet_name, temp_component_key, did))
        else:
            self.logger.ui_debug(
                "{} [{}] {}: Device: {} [{}] - No data collected for this device.".format(app_name, self.app_id,
                                                                                          snippet_name,
                                                                                          temp_component_key, did))


#####################################################################

try:
    # This dynamic app should only be executed on component devices
    if not self.comp_unique_id:
        component_error_msg = "Component unique id is not set."
        self.logger.ui_debug(
            "{} [{}] {}: Device: {} [{}] {}".format(app_name, self.app_id, snippet_name, self.name, self.did,
                                                    component_error_msg))
        send_alert(component_error_msg)
    else:
        # composite result structure
        complete_results = {}

        # Get dictionary of SQL instances and associated network names
        sql_instances_and_network_names = get_sql_instances_and_network_names()

        # For each SQL instance,
        for sql_instance, network_name in sql_instances_and_network_names.iteritems():
            # issue the PowerShell command to get all database backup info
            query_result = query_single_sql_instance(sql_instance, network_name)
            # reformat the results based on device components
            single_instance_results = group_results_by_component(query_result)
            # merge the results from this instance into the overall structure
            complete_results.update(single_instance_results)

        # Store results into result handler
        insert_results_into_result_handler(complete_results)

except PowerShellException as ps_exe:
    self.logger.ui_debug(
        "{} [{}] {}: Device: {} [{}] PowerShellException exception caught: {}".format(app_name, self.app_id,
                                                                                      snippet_name, self.name, self.did,
                                                                                      ps_exe.message))
    send_alert(ps_exe.message)
except PowerShellEmptyKey as ps_empty:
    self.logger.ui_debug(
        "{} [{}] {}: Device: {} [{}] PowerShellEmptyKey exception caught: {}".format(app_name, self.app_id,
                                                                                     snippet_name, self.name, self.did,
                                                                                     ps_empty))
except Exception as exe:
    self.logger.ui_debug(
        "{} [{}] {}: Device: {} [{}] Exception caught: {}".format(app_name, self.app_id, snippet_name, self.name,
                                                                  self.did, exe.message))
    send_alert(exe.message)
