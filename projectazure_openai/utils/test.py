from settings import Settings
from authenticate import Authenticate
from assistant import Assistant


class Test:
    def __init__(self):
        self.Authenticate = Authenticate()
        self.client = self.Authenticate.get_client()
        self.Assistant = Assistant(self.client, Settings.ASSISTANT_ID)

    def test(self):
        assistant_details = self.Assistant.retrive_assistant()
        # print(assistant_details)
        assistant_details = self.Assistant.update_assistant()
        print(assistant_details)

        
        
        
        
t=Test()
t.test()