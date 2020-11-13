from flask import Flask, Response
import boto3 
import os

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

@app.route('/images/<id>', methods=['GET'])
def imageFormId(id):
    s3 = session.client('s3')
    filename='%s.jpg' % (id)
    print(filename)
    file = s3.get_object(Bucket='animedevops', Key=filename) 
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=1.jpg"}
    )


app.run(host="0.0.0.0", debug=True, port=8800)
