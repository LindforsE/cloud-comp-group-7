import json
import boto3
client = boto3.client('dynamodb')

def lambda_handler(event, context):
  print("event" + str(event))
  item=event['id']
  
  scode=0
  
  data = client.get_item(
    TableName='rekog-test',
    Key={
        'id': {
          'S': event['id']
        }
    }
  )
  
  print("data" + str(data))
  print("length is " + str(data['ResponseMetadata']['HTTPHeaders']['content-length']))
  if data['ResponseMetadata']['HTTPHeaders']['content-length'] is '2':
  #if item in str(data):
    scode=300
  else:
    scode=200
  response = {
      'statusCode': scode,
      'body': json.dumps(data),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials' : True
      },
  }

  return response