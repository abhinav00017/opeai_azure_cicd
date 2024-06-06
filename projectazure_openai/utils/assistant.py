from openai import AzureOpenAI

from utils.tools import Tools


class Assistant:
    
    def __init__(self, client, assistant_id):
        self.client = client
        self.assistant_id = assistant_id
        self.Tools = Tools()
    
    def retrive_assistant(self):
        assistant_details = self.client.beta.assistants.retrieve(self.assistant_id)  
        return assistant_details
    
    def update_assistant(self):
        assistant_details = self.client.beta.assistants.update(
                        assistant_id=self.assistant_id,
                        instructions=self.Tools.get_instructions(),
                        model="gpt4_deployment",
                        tools= self.Tools.get_tools()
                    )
        return assistant_details
    
    
    
    