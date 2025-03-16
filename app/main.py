import json
import boto3
from botocore.exceptions import ClientError

def load_json_to_dynamodb(json_file_path, table_name):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # get the comments from the json file
        if 'comments' in data:
            items = data['comments']
        else:
            items = data 
            
        if not isinstance(items, list):
            items = [items]
        
        # connect to dynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        
        # add the item to dynamoDB
        count = 0
        with table.batch_writer() as batch:
            for item in items:
                if 'id' in item:
                    item['id'] = str(item['id'])
                else:
                    print(f"Warning: Item is missing 'id' field: {item}")
                    continue
                
                batch.put_item(Item=item)
                count += 1
                
        print(f"Successfully loaded {count} items into the {table_name} table.")
        
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Configuration
    json_file_path = "../resource/Copy of comments.json" 
    table_name = "comments"       

    # add the json info to dynamoDB
    load_json_to_dynamodb(json_file_path, table_name)