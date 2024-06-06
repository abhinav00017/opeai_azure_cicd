from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.web.models import ManagedServiceIdentity
from azure.mgmt.web.models import NameValuePair


import time, json, os, shutil, subprocess, requests, random
from dotenv import load_dotenv

load_dotenv()

class Function_utils:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.path = os.getcwd()+'/repo_folder'
        # # self.path = self.path.replace("\\", "/")
        # self.path  = "D:/.....Abhinav_Telefonica/Resource_Azure_py_SDK/projectazure_openai/repo_folder"
        
    def check_docker(self,repo_link, branch_name):
        api_url = repo_link.replace('github.com', 'api.github.com/repos')[:-4] + '/branches'
        headers = {
            "Authorization": "Bearer xxxxxxxxxxxxxxxxxxx",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return 'Invalid repository link'
        else:
            branches = [branch['name'] for branch in response.json()]
            
            if branch_name not in branches:
                return "Invalid branch name. Please provide a valid branch name, branches available are: " + ", ".join(branches)
            
            else:    
                if branch_name.lower() == "main":
                    api_url = repo_link.replace('github.com', 'api.github.com/repos')[:-4] + '/contents/Dockerfile'
                    headers = {
                        "Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxxx",
                        "Accept": "application/vnd.github.v3+json",
                        "X-GitHub-Api-Version": "2022-11-28"
                    }
                    response = requests.get(api_url, headers=headers)
                    print(response)
                    if response.status_code == 200:
                        return 'Dockerfile exists in this repository.'
                    else:
                        return 'Dockerfile does not exist in this repository.'
        
                else:
                    api_url = repo_link.replace('github.com', 'api.github.com/repos')[:-4] + '/contents/Dockerfile?ref=' + branch_name
                    headers = {
                        "Authorization": "Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxx",
                        "Accept": "application/vnd.github.v3+json",
                        "X-GitHub-Api-Version": "2022-11-28"
                    }
                    response = requests.get(api_url, headers=headers)
                    print(response)
                    if response.status_code == 200:
                        return 'Dockerfile exists in this repository.'
                    else:
                        return 'Dockerfile does not exist in this repository.'

    def create_folder(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print(f"Folder created at {self.path}")
        else:
            print(f"Folder already exists at {self.path}")
            for root, dirs, files in os.walk(self.path):
                for dir in dirs:
                    os.chmod(os.path.join(root, dir), 0o777)
                for file in files:
                    os.chmod(os.path.join(root, file), 0o777)
            shutil.rmtree(self.path)
            os.mkdir(self.path)

    def clone_repo(self, repo_url, branch_name):
        
        self.create_folder()
        
        try:
            subprocess.check_call(['git', 'clone', '-b', branch_name, repo_url, self.path])
            print(f"Branch {branch_name} of repository cloned successfully to {self.path}")
            return f"Branch {branch_name} of repository cloned successfully to {self.path}"
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone branch {branch_name} of repository. Error: {e}")
            return f"Failed to clone branch {branch_name} of repository. Error: {e}"

    # clone_repo("https://github.com/abhi000017/one_repo_main.git", "development")
    
    def get_acr_credentials(self, registry_name, subscription_id, resource_group_name):
        
        client = ContainerRegistryManagementClient(self.credential, subscription_id)
        acr = client.registries.get(resource_group_name, registry_name)
        acr_credentials = client.registries.list_credentials(resource_group_name, registry_name)
        print("acr credentials: ",acr.admin_user_enabled, acr_credentials.username, acr_credentials.passwords[0].value)
        return acr_credentials.username, acr_credentials.passwords[0].value
        # return acr.admin_user_enabled, acr.admin_user_name, acr.admin_user_password
    
    
    def assign_identity_and_grant_acr_access(self, subscription_id, resource_group_name, app_service_name, acr_name):
            
        try:
            web_client = WebSiteManagementClient(self.credential, subscription_id)
            # auth_client = AuthorizationManagementClient(self.credential, subscription_id)

            # site_config = web_client.web_apps.get(resource_group_name, app_service_name)

            # site_config.identity = {'type': 'SystemAssigned'}

            # poller = web_client.web_apps.begin_create_or_update(resource_group_name, app_service_name, site_config)

            # identity = poller.result()
           
            # principal_id = identity.identity.principal_id
            
            # print(principal_id)

            # # Get the resource ID of the ACR
            # acr_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ContainerRegistry/registries/{acr_name}"

            # # Grant the managed identity ACR pull access
            # role_assignment = auth_client.role_assignments.create(
            #     acr_id, 
            #     principal_id, 
            #     {
            #         'properties': {
            #             'roleDefinitionId': '/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/7f951dda-4ed3-4680-a7ca-43fe172d538d',
            #             'principalId': principal_id
            #         }
            #     }
            # )
            
            # print("Identity assigned and ACR access granted successfully.")
            # print(role_assignment)
            
            # app_service = web_client.web_apps.get(resource_group_name, app_service_name)
            
            # # print(app_service.identity.type)

            # # Check if the App Service already has a Managed Identity
            # if app_service.identity is None:
            #     # Create a new ManagedServiceIdentity object
            #     app_service.identity = ManagedServiceIdentity(type="SystemAssigned")
            # else:
            #     # If the App Service already has a Managed Identity, preserve the existing configuration
            #     app_service.identity.type = "SystemAssigned"

            # # Update the App Service configuration
            # poller = web_client.web_apps.begin_create_or_update(resource_group_name, app_service_name, app_service)

            # # Wait for the operation to complete
            # result = poller.result()

            # # The principal ID of the Managed Identity is now available as result.identity.principal_id
            # # print(f"Managed Identity Principal ID: {result}")
            
            app_settings = web_client.web_apps.list_application_settings(resource_group_name, app_service_name)
            
            username, password = self.get_acr_credentials(acr_name, subscription_id, resource_group_name)

            if app_settings is None:
                app_settings = NameValuePair()

            app_settings.properties = {
                'DOCKER_REGISTRY_SERVER_URL': f'https://{acr_name}.azurecr.io',
                'DOCKER_REGISTRY_SERVER_USERNAME': f'{username}',
                'DOCKER_REGISTRY_SERVER_PASSWORD': f'{password}',
            }

            
            web_client.web_apps.update_application_settings(resource_group_name, app_service_name, app_settings)
            
            return True
        
        except Exception as e:
            print(f"Failed to assign identity and grant ACR access. Error: {e}")
            return str(e)
    
    def get_acr_access_token(self, registry_name, subscription_id, resource_group_name):
        client = ContainerRegistryManagementClient(self.credential, subscription_id)
        login_server = client.registries.get(resource_group_name, registry_name).login_server
        token_credential = self.credential.get_token("https://management.azure.com/.default")
        access_token = token_credential.token
    
        # Obtain the ACR token
        response = requests.post(
            f'https://{login_server}/oauth2/exchange',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'access_token',
                'service': login_server,
                'tenant': os.getenv("AZURE_TENANT_ID"),
                'access_token': access_token
            }
        )
    
        if response.status_code != 200:
            raise Exception(f"Failed to obtain ACR access token: {response.text}")
    
        acr_access_token = response.json().get('refresh_token')
        return login_server, acr_access_token

    def deploy_docker_image_to_app_service(self, subscription_id, resource_group_name, app_service_name, acr_name, image_tag):

        web_client = WebSiteManagementClient(self.credential, subscription_id)
        
        site_config = web_client.web_apps.get_configuration(resource_group_name, app_service_name)

        site_config.linux_fx_version = f'DOCKER|{acr_name}.azurecr.io/{image_tag}'
        
        print(f"Deploying Docker image to App Service: {app_service_name}...")
        web_client.web_apps.update_configuration(resource_group_name, app_service_name, site_config)
        return f"Docker image deployed successfully to App Service: {app_service_name}"


    def build_and_push_docker_image(self, registry_name, subscription_id, resource_group_name, acr_password, flag):

        acr_name = registry_name
        client = ContainerRegistryManagementClient(self.credential, subscription_id)
        
        login_server = client.registries.get(resource_group_name, acr_name).login_server
        
        print(f"Login server: {login_server}")

        try:
            print("Building Docker image...")
            subprocess.check_call(['docker', 'build', '-t', 'temp_tag', self.path])
            print("Docker image built successfully.")
            
            print("Pushing Docker image...")
            image_id = subprocess.check_output(['docker', 'inspect', '-f', '{{.Id}}', 'temp_tag']).decode('utf-8').strip()
            print(image_id.split(":")[1])
            image_id = image_id.split(":")[1][:12]
            print(f"Image ID: {image_id}")

            print(f"Tagging Docker image with login server: {login_server}...")
            subprocess.check_call(['docker', 'tag', image_id, f'{login_server}/ai:{image_id}'])
            print(f"Image tagged successfully with login server: {login_server}")
            
            subprocess.check_call(['docker', 'login', login_server, '--username', '00000000-0000-0000-0000-000000000000', '--password', acr_password])

            print(f"Pushing Docker image to login server: {login_server}...")
            subprocess.check_call(['docker', 'push', f'{login_server}/ai:{image_id}'])
            print(f"Docker image pushed successfully to login server: {login_server}")
            
            return flag,image_id
            
            # deploy_docker_image_to_app_service(credential, subscription_id, resource_group_name, "openaitestdocker", acr_name, f'ai/{image_id}')

        except subprocess.CalledProcessError as e:
            print(f"Failed to build and push Docker image. Error: {e}")
            flag = str(e)
            return flag,None
        
    def build_push_deploy(self, registry_name, subscription_id, resource_group_name, app_service_name):
        print("path: ", self.path)
        acr_pull_access = self.assign_identity_and_grant_acr_access(subscription_id, resource_group_name, app_service_name, registry_name)
        if acr_pull_access != True:
            return acr_pull_access
        
        acr_password = self.get_acr_access_token(registry_name, subscription_id, resource_group_name)[1]
        flag = "no_error"
        flag,response_image_id = self.build_and_push_docker_image(registry_name, subscription_id, resource_group_name, acr_password, flag)
        if flag == "no_error":
            response = self.deploy_docker_image_to_app_service(subscription_id, resource_group_name, app_service_name, registry_name, f'ai:{response_image_id}')
            return response
        else:
            return flag
    
    def create_resource_group(self, rg_name, rg_location, rg_subscription_id):
        client = ResourceManagementClient(self.credential, rg_subscription_id)
        try:
            print(f"Creating resource group: {rg_name}...")
            client.resource_groups.create_or_update(rg_name, {'location': rg_location, 'tags': {'bus-owner': 'ccoe@telefonica.com'}})
            print(f"Resource group: {rg_name} created successfully.")
            return f"Resource group: {rg_name} created successfully."
        except Exception as e:
            print(f"Failed to create resource group: {rg_name}. Error: {e}")
            return f"Failed to create resource group: {rg_name}. Error: {e}"
        
    def create_azure_container_registry(self, acr_registry_name, acr_resource_group_name, acr_location, acr_subscription_id):
        
        resource_client = ResourceManagementClient(self.credential, acr_subscription_id)
        acr_client = ContainerRegistryManagementClient(self.credential, acr_subscription_id)

        # Create or get resource group
        resource_group_params = {'location': acr_location, 'tags': {'bus-owner': 'ccoe@telefonica.com'}}
        resource_client.resource_groups.create_or_update(acr_resource_group_name, resource_group_params)

        # Create container registry
        registry_params = {
            'location': acr_location,
            'sku': {'name': 'Basic'},
            'admin_user_enabled': True,
            'tags': {'bus-owner': 'ccoe@telefonica.com'}
        }
        acr_client.registries.begin_create(acr_resource_group_name, acr_registry_name, registry_params)

        print(f"Azure Container Registry: {acr_registry_name} created successfully.")
        return f"Azure Container Registry: {acr_registry_name} created successfully."
    
    def create_app_service(self, aps_name, aps_resource_group, aps_plan, aps_location, aps_runtime_stack, aps_subscription_id):
        web_client = WebSiteManagementClient(self.credential, aps_subscription_id)
        print(f"Creating App Service: {aps_name}...")
        
        try:
            app_service_plan = web_client.app_service_plans.get(aps_resource_group, aps_plan)
            print(f"App Service Plan ID: {app_service_plan.id}")
            
            web_client.web_apps.begin_create_or_update(
                aps_resource_group, 
                aps_name,
                {
                    "location": aps_location,
                    "server_farm_id": app_service_plan.id,
                    "site_config": {
                        "linux_fx_version": aps_runtime_stack
                        },
                    "tags": {"bus-owner" : "ccoe@telefonica.com"}
                }
                )
            
            print(f"App Service: {aps_name} created successfully.")
            return f"App Service: {aps_name} created successfully."
        
        except Exception as e:
            return str(e)
        
    def create_app_service_plan(self, asp_name, asp_resource_group, asp_location, asp_subscription_id):
        web_client = WebSiteManagementClient(self.credential, asp_subscription_id)
        print(f"Creating App Service Plan: {asp_name}...")
        
        try:
            web_client.app_service_plans.begin_create_or_update(
                asp_resource_group, 
                asp_name, 
                {
                    'location': asp_location, 
                    'reserved': True,
                    'sku': {'name': 'B1', 'tier': 'Basic'}, 
                    'tags' : {'bus-owner' : 'ccoe@telefonica.com'} 
                }
            )
            
            print(f"App Service Plan: {asp_name} created successfully.")
            return f"App Service Plan: {asp_name} created successfully."
        
        except Exception as e:
            return str(e)
        
    def execute_function_call(self,function_name, arguments):
        print("Function Name: ", function_name)
        response = ""
        arguments = json.loads(arguments)
        print("Arguments: ", arguments)
        if function_name == "check_docker":
            response = self.check_docker(arguments['repo_link'], arguments['branch_name'])
        elif function_name == "clone_repo":
            response = self.clone_repo(arguments['repo_link'], arguments['branch_name'])
        elif function_name == "create_resource_group":
            response = self.create_resource_group(arguments['rg_name'], arguments['rg_location'], arguments['rg_subscription_id'])
        elif function_name == "create_azure_container_registry":
            response = self.create_azure_container_registry(arguments['acr_registry_name'], arguments['acr_resource_group_name'], arguments['acr_location'], arguments['acr_subscription_id'])
        elif function_name == "create_azure_app_service_plan":
            response = self.create_app_service_plan(arguments['asp_name'], arguments['asp_resource_group'], arguments['asp_location'], arguments['asp_subscription_id'])
        elif function_name == "create_azure_app_service":
            response = self.create_app_service(arguments['aps_name'], arguments['aps_group'], arguments['aps_plan'], arguments['aps_location'], arguments['aps_runtime_stack'], arguments['aps_subscription_id'])
        elif function_name == "build_push_deploy":
            response = self.build_push_deploy(arguments['registry_name'], arguments['subscription_id'], arguments['resource_group_name'], arguments['app_service_name'])
        else:
            print("Invalid function name")
            response = "Invalid function name"
        print(response) 
        return response
    


# fun = Function_utils()

# # fun.get_acr_credentials("registry1017", "255b19ed-b087-4a1e-bff7-5c35f0b81de6", "tefde-azr-test-csp-1")

# # print(fun.assign_identity_and_grant_acr_access("255b19ed-b087-4a1e-bff7-5c35f0b81de6", "tefde-azr-test-csp-1","aps1017","registry1017"))
# # # fun.build_push_deploy("registry1017", "255b19ed-b087-4a1e-bff7-5c35f0b81de6", "tefde-azr-test-csp-1", "aps1017")

# print(fun.create_app_service("aps1017", "tefde-azr-test-csp-1", "apsplan1017", "germanywestcentral", "python|3.9", "255b19ed-b087-4a1e-bff7-5c35f0b81de6"))
