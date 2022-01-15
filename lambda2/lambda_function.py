import json
import boto3
from decimal import Decimal

s3 = boto3.client('s3')
rekog = boto3.client('rekognition')
#db = boto3.client('dynamodb')

db_resource = boto3.resource('dynamodb')

def lambda_handler(event, context):   
    bucketName = event['Records'][0]['s3']['bucket']['name']
    objectKey = event['Records'][0]['s3']['object']['key']
    
    print(bucketName + " " + objectKey)
    
    try:
        print("doing rekog....")
        response = rekog.detect_labels(
            Image={
                 'S3Object': {
                     'Bucket':bucketName,
                     'Name':objectKey
                 }
             },
             MaxLabels=10,
             MinConfidence=80.0
        )
        print("rekog succeeded!")
        #print(response)
    except Exception as err:
        print(err)
        print("could not rekog. Check bucket and object")
        raise(err)


    # retreive labels from response
    labels = response['Labels']

    # transform labels into dynamo-workable format (decimal instead of float)
    decimaled_labels =json.loads(json.dumps(labels), parse_float=Decimal)

    # create item (dictionary) to save in DB
    db_item = {'id':objectKey, 'Labels':decimaled_labels}
    
    try:
        # get table object
        table = db_resource.Table('rekog-test')
        
        # Save item in DynamoDB
        print("saving to db....")
        table.put_item(Item=db_item)
        
        print("successfully saved!")
    except Exception as err:
        print(err)
        print("could not save to db. Check db and item")
        raise(err)
    

    try:
        print("deleting object from s3")
        response = s3.delete_object(Bucket=str(bucketName), Key=str(objectKey))
        print("object deleted")
    except Exception as err:
        print(err)
        print("could not delete object from s3")
        raise(err)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
