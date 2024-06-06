import json

class Records:
    def __init__(self):
        pass
    
    def create_record(self, record):
        try:
            with open('database.txt', 'r') as file:
                data = json.load(file)
                data[list(record.keys())[0]] = list(record.values())[0]

            with open('database.txt', 'w') as file:
                json.dump(data, file)
                
            return True
        except Exception as e:
            return e

    
    def retrieve_record(self, email_id):
        with open('database.txt', 'r') as file:
            record = json.load(file)
            
            if record.get(email_id):
                return list(record[email_id])
            else:
                return "Record not found"

    
    
rec = Records()

# print(rec.create_record({'ahi@1xcv23svf': ['123fd', '420']}))
print(rec.retrieve_record('abhinavch53@gmail.com'))