# Impliment edit, add, and delete functionality to comments. Update the database accordingly when these APIs are called.

# Requirements:
# Edit text of existing comments 
# Add a comment, with new text (from “Admin” user), with the current time
# Delete existing comments 
# List all comments

from fastapi import HTTPException
import boto3
import json
import decimal
import datetime
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("comments")

# Helper class to convert Decimal types to float for JSON serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o) if o % 1 else int(o)
        return super(DecimalEncoder, self).default(o)

# List all comments
async def fetch_all_comments():
    response = table.scan()
    # print(response)
    items = response["Items"]
    if items:
        return {"statusCode": 200, "body": json.dumps(items, cls=DecimalEncoder)}
    else:
        return {"statusCode": 404, "body": "comments not found"}

async def edit_comment_text(id, new_text):
    response = table.get_item(Key={"id": id})
    
    if "Item" not in response:
        # Comment not found, raise an HTTPException
        raise HTTPException(status_code=404, detail=f"Comment with ID {id} not found")
    
    table.update_item(
        Key={"id": id},
        UpdateExpression="SET #text = :text",
        ExpressionAttributeNames={
            "#text": "text"  
        },
        ExpressionAttributeValues={
            ":text": new_text
        }
    )
    return {"statusCode": 200, "body": "Comment updated successfully"}

# Add a comment, with new text (from “Admin” user), with the current time
async def add_admin_comment(text=None, image=None):
    comment_id = str(uuid.uuid4()) # we can also get the biggest id of the id in the table, and +1 to that
    
    # get current timestamp in the specified format (2015-09-01T13:10:00Z)
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Create the comment item
    comment_item = {
        "id": comment_id,
        "author": "Admin",
        "text": text,
        "date": current_time,
        "likes": 0,
        "image": ""  
    }
    
    table.put_item(Item=comment_item)
    
    return {
        "statusCode": 201,
        "body": f"Comment added successfully with ID: {comment_id}"
    }

# Delete existing comments 
async def delete_comment_by_id(comment_id):
    try:
        response = table.get_item(Key={"id": comment_id})
        
        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": f"Comment with ID {comment_id} not found"
            }
        
        # Delete the comment
        table.delete_item(Key={"id": comment_id})
        
        return {
            "statusCode": 200,
            "body": f"Comment with ID {comment_id} deleted successfully"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error deleting comment: {str(e)}"
        }
    
async def delete_all_comments():
    response = table.scan(AttributesToGet=["id"])
    items = response.get("Items", [])
    
    # Delete each item
    for item in items:
        table.delete_item(Key={"id": item["id"]})

    return {
            "statusCode": 200,
            "body": f"Deleted {len(items)} items from the database."
        }
    
if __name__ == "__main__":
    
    # result = fetch_all_comments()
    # result = edit_comment_text("1", "lol")
    # result = add_admin_comment("this is a new one")
    # result = delete_comment_by_id('2')
    result = delete_all_comments()

    print(result)