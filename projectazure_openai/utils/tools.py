class Tools:
    def __init__(self):
        self.tools = [
            {
                "type": "function",
                
                "function": {
                    
                    "name": "check_docker",
                    "description": "Checks if docker file exists in the repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo_link": {
                                "type": "string",
                                "description": "Give link to the repository from user"
                            },
                            "branch_name": {
                                "type": "string",
                                "description": "Give the branch name from user"
                            }
                        },
                        "required": ["repo_link", "branch_name"]
                    },
                }
            },
            {
                "type": "function",
                
                "function" : {
            
                    "name": "clone_repo",
                    "description": "Helps to clone the repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo_link": {
                                "type": "string",
                                "description": "Give repo link given from user"
                            },
                            "branch_name": {
                                "type": "string",
                                "description": "Give the branch name from user"
                            }
                        },
                        "required": ["repo_link", "branch_name"]
                    }
                }
            },
            {
                "type": "function",
                
                "function" : {
            
                    "name": "build_push_deploy",
                    "description": "Helps to build, push and deploy the docker image to the Azure Container Registry and Azure App Service",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "registry_name": {
                                "type": "string",
                                "description": "Give the Azure Container Registry name from user"
                            },
                            "subscription_id": {
                                "type": "string",
                                "description": "Give the Azure Subscription ID from user"
                            },
                            "resource_group_name": {
                                "type": "string",
                                "description": "Give the Azure Resource Group name from user"
                            },
                            "app_service_name": {
                                "type": "string",
                                "description": "Give the Azure App Service name from user"
                            }
                        },
                        "required": ["registry_name", "subscription_id", "resource_group_name", "app_service_name"]
                    }
                }
            },
            {
                "type": "function",
                
                "function" : {
            
                    "name": "create_resource_group",
                    "description": "This will create a resource group in Azure",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rg_name": {
                                "type": "string",
                                "description": "Give name of the rg from user"
                            },
                            "rg_location": {
                                "type": "string",
                                "description": "Give location of the rg from user"
                            },
                            "rg_subscription_id": {
                                "type": "string",
                                "description": "Give subscription id of the rg from user"
                            }
                        },
                        "required": ["rg_name", "rg_location", "rg_subscription_id"]
                    }
                }
            },
            {
                "type": "function",
                
                "function" : {
                    "name" : "create_azure_container_registry",
                    "description": "This will create an Azure Container Registry",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "acr_subscription_id": {
                                "type": "string",
                                "description": "Give the Azure Subscription ID from user"
                            },
                            "acr_registry_name": {
                                "type": "string",
                                "description": "Give the Azure Container Registry name from user"
                            },
                            "acr_resource_group_name": {
                                "type": "string",
                                "description": "Give the Azure Resource Group name from user"
                            },
                            "acr_location": {
                                "type": "string",
                                "description": "Give the location of the Azure Container Registry from user"
                            }
                        },
                        "required": ["acr_subscription_id","acr_registry_name", "acr_resource_group_name", "acr_location"]
                    }
                }
            },
            {
                "type": "function",
                
                "function" : {
                    "name" : "create_azure_app_service",
                    "description": "This will create an Azure App Service",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "aps_subscription_id": {
                                "type": "string",
                                "description": "Give the Azure Subscription ID from user"
                            },
                            "aps_name": {
                                "type": "string",
                                "description": "Give the Azure App Service name from user"
                            },
                            "aps_group": {
                                "type": "string",
                                "description": "Give the Azure Resource Group name from user"
                            },
                            "aps_plan": {
                                "type": "string",
                                "description": "Give the Azure App Service Plan name from user"
                            },
                            "aps_location": {
                                "type": "string",
                                "description": "Give the location of the Azure App Service from user"
                            },
                            "aps_runtime_stack": {
                                "type": "string",
                                "description": "Give the runtime stack of the Azure App Service from user"
                            }
                        },
                        "required": ["aps_subscription_id", "aps_name", "aps_group", "aps_plan", "aps_location", "aps_runtime_stack"]
                    }
                }
            },
            {
                "type": "function",
                
                "function" : {
                    "name" : "create_azure_app_service_plan",
                    "description": "This will create an Azure App Service Plan",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "asp_subscription_id": {
                                "type": "string",
                                "description": "Give the Azure Subscription ID from user"
                            },
                            "asp_name": {
                                "type": "string",
                                "description": "Give the Azure App Service Plan name from user"
                            },
                            "asp_resource_group": {
                                "type": "string",
                                "description": "Give the Azure Resource Group name from user"
                            },
                            "asp_location": {
                                "type": "string",
                                "description": "Give the location of the Azure App Service Plan from user"
                            }
                        },
                        "required": ["asp_subscription_id", "asp_name", "asp_resource_group", "asp_location"]
                    }
                }
            }
        ]
        
    def get_instructions(self):
        with open('prompt_azure_openai.txt', 'r') as file:
            asst_instructions = file.read()
        return asst_instructions
    
    def get_tools(self):
        return self.tools
    
