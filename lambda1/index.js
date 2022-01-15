const AWS = require('aws-sdk');
AWS.config.update({ region: process.env.AWS_REGION});
const s3 = new AWS.S3();
//const uploadBucket = 'gomes-test-bucket'; //bucket name
const uploadBucket = 'cloudfors-rekog-source'; //bucket name
const URL_EXPIRATION_SECONDS = 30000; //how long the pre-signed URL will be valid


exports.handler = async (event) => {
    return await getUploadURL(event);
};

const getUploadURL = async function(event){
    const randomID = parseInt(Math.random() * 10000000); //random ID between 0 and 10000000
    const Key = `${randomID}`; //key will be used as filename in the S3 bucket

    //Get signed URL from S3 with these parameters
    const s3Params = {
        Bucket: uploadBucket,
        Key,
        Expires: URL_EXPIRATION_SECONDS,
        ContentType: 'image/'
    };
    
    return new Promise((resolve, reject) => {
        //Get signed URL
        let uploadURL = s3.getSignedUrl('putObject', s3Params);
        resolve({
            "statusCode": 200,
            "isBase64Encoded": false,
            "headers": {
                "Access-Control-Allow-Origin" : "*"
            },
            "body": JSON.stringify({
                "uploadURL": uploadURL,
                "filename": Key
            })
        });
    });
};