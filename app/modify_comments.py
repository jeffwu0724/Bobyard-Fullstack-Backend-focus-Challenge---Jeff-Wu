# Impliment edit, add, and delete functionality to comments. Update the database accordingly when these APIs are called.

# Requirements:
# Edit text of existing comments 
# Add a comment, with new text (from “Admin” user), with the current time
# Delete existing comments 
# List all comments

import boto3
import json
import decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("comments")

# Helper class to convert Decimal types to float for JSON serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o) if o % 1 else int(o)
        return super(DecimalEncoder, self).default(o)

# List all comments
def fetch_all_comments():
    response = table.scan()
    # print(response)
    items = response["Items"]
    if items:
        return {"statusCode": 200, "body": json.dumps(items, cls=DecimalEncoder)}
    else:
        return {"statusCode": 404, "body": "comments not found"}

def edit_comment_text(id, new_text):
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

if __name__ == "__main__":
    
    # result = fetch_all_comments()
    result = edit_comment_text("1", "lol")
    print(result)