# assisted_swarm_client.assisted_swarm.SwarmApi

All URIs are relative to *http://api.assisted-swarm.com/api/assisted-swarm*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_new_agent**](SwarmApi.md#create_new_agent) | **POST** /agents | Create new agent.
[**delete_agent**](SwarmApi.md#delete_agent) | **DELETE** /agents/{agent_id} | Delete agent.
[**exit**](SwarmApi.md#exit) | **GET** /exit | Exit the process.
[**get_agent**](SwarmApi.md#get_agent) | **GET** /agents/{agent_id} | Get specific agent.
[**health**](SwarmApi.md#health) | **GET** /health | Health check.
[**list_agents**](SwarmApi.md#list_agents) | **GET** /agents | List all running agents.


# **create_new_agent**
> Agent create_new_agent(new_agent_params=new_agent_params)

Create new agent.

### Example
```python
from __future__ import print_function
import time
import assisted_swarm_client.assisted_swarm
from assisted_swarm_client.assisted_swarm.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assisted_swarm_client.assisted_swarm.SwarmApi()
new_agent_params = assisted_swarm_client.assisted_swarm.NewAgentParams() # NewAgentParams | Create new agent for swarm. (optional)

try:
    # Create new agent.
    api_response = api_instance.create_new_agent(new_agent_params=new_agent_params)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SwarmApi->create_new_agent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **new_agent_params** | [**NewAgentParams**](NewAgentParams.md)| Create new agent for swarm. | [optional] 

### Return type

[**Agent**](Agent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_agent**
> delete_agent(agent_id)

Delete agent.

### Example
```python
from __future__ import print_function
import time
import assisted_swarm_client.assisted_swarm
from assisted_swarm_client.assisted_swarm.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assisted_swarm_client.assisted_swarm.SwarmApi()
agent_id = 56 # int | 

try:
    # Delete agent.
    api_instance.delete_agent(agent_id)
except ApiException as e:
    print("Exception when calling SwarmApi->delete_agent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **exit**
> exit()

Exit the process.

### Example
```python
from __future__ import print_function
import time
import assisted_swarm_client.assisted_swarm
from assisted_swarm_client.assisted_swarm.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assisted_swarm_client.assisted_swarm.SwarmApi()

try:
    # Exit the process.
    api_instance.exit()
except ApiException as e:
    print("Exception when calling SwarmApi->exit: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent**
> Agent get_agent(agent_id)

Get specific agent.

### Example
```python
from __future__ import print_function
import time
import assisted_swarm_client.assisted_swarm
from assisted_swarm_client.assisted_swarm.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assisted_swarm_client.assisted_swarm.SwarmApi()
agent_id = 56 # int | 

try:
    # Get specific agent.
    api_response = api_instance.get_agent(agent_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SwarmApi->get_agent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id** | **int**|  | 

### Return type

[**Agent**](Agent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health**
> health()

Health check.

### Example
```python
from __future__ import print_function
import time
import assisted_swarm_client.assisted_swarm
from assisted_swarm_client.assisted_swarm.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assisted_swarm_client.assisted_swarm.SwarmApi()

try:
    # Health check.
    api_instance.health()
except ApiException as e:
    print("Exception when calling SwarmApi->health: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_agents**
> AgentList list_agents()

List all running agents.

### Example
```python
from __future__ import print_function
import time
import assisted_swarm_client.assisted_swarm
from assisted_swarm_client.assisted_swarm.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = assisted_swarm_client.assisted_swarm.SwarmApi()

try:
    # List all running agents.
    api_response = api_instance.list_agents()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SwarmApi->list_agents: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AgentList**](AgentList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

