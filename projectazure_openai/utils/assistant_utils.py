
from utils.tools import Tools


class Assistant_utils:
    
    def __init__(self, client, assistant_id):
        self.client = client
        self.assistant_id = assistant_id
        
    def retrive_thread(self, thread_id, run_id):
        return self.client.beta.threads.get(thread_id = thread_id, run_id = run_id)
    
    def create_message_and_run(self,assistant, query, thread=None):
        if not thread:
            thread = self.client.beta.threads.create()
        
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )
        
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id, 
            assistant_id=assistant.id,
        )
        
        return run, thread
    
    def get_function_details(self,run):
        print("Run Required action: ", run.required_action)
        

        function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
        arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
        function_id = run.required_action.submit_tool_outputs.tool_calls[0].id
        
        
        
        print("Function Name: ", function_name, "and arguments: ", arguments)
        
        return function_name, arguments, function_id
    
    def submit_tool_outputs(self, run, thread, function_id, function_response):
        # tools_outputs = []
        # for i in range(len(function_id)):
            
        #     tools_outputs.append(
        #         {
        #             "tool_call_id": function_id,
        #             "output": str(function_response )
        #         }
        #     )
            
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id = thread.id,
            run_id = run.id,
            tool_outputs = [
                {
                    "tool_call_id": function_id,
                    "output": str(function_response)
                }
            ]
        )
        
        return run 
    
    