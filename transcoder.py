'''
Author: max@maxsorto.com
Title: S3 Uploader and Transcoder
Description: Uploads .mov file to S3 and begins Elastic Transcoder jobs.
'''

#Pull in required libraries...
import boto3
import time
import sys

#AWS Keys (Replace with your own values)...
aws_access_key_id = 'REPLACE_WITH_YOUR_ACCESS_KEY'
aws_secret_access_key = 'REPLACE_WITH_YOUR_SECRET_KEY'


'''
Uploads files to S3
'''
def upload_file_to_s3(file, vid_id):
	
	# CREATE BOTO S3 CLIENT
	s3 = boto3.resource(
	    's3',
	    aws_access_key_id = aws_access_key_id,
	    aws_secret_access_key = aws_secret_access_key
	)	

	print('Began upload...')

	data = open(file, 'rb')
	s3.Bucket('medium-demo').put_object(Key = vid_id + '.mov', Body = data)
	
	print('File uploaded to S3.')


'''
Starts Elastic Transcoder job
'''
def transcode_file_to_mp4(file, vid_id):

	# CREATE BOTO ELASTIC TRANSCODER CLIENT
	transcoder = boto3.client(
		'elastictranscoder', 
		'us-west-2',
	    aws_access_key_id = aws_access_key_id,
	    aws_secret_access_key = aws_secret_access_key
	)

	print('Began transcoding job...')

	transcoder.create_job(
	    PipelineId = '1517180014907-6hwssy',
	    Input = {
	        'Key': vid_id + '.mov',
	        'FrameRate': 'auto',
	        'Resolution': 'auto',
	        'AspectRatio': 'auto',
	        'Interlaced': 'auto',
	        'Container': 'mov'
	    },
		Outputs = [
			{
				'Key': vid_id + '.mp4',
				'PresetId': '1517179733213-v0k5ut',
				'ThumbnailPattern': vid_id + '-thumbnail-{count}'
			}
		]
	)

	print('Done transcoding!')


'''
Main execution expects system argument for video file path
'''
def init():

	try: 
		#Set directory path for video to upload...
		file = sys.argv[1]
	except:
		print('Did not supply file path for .mov video.')
		exit()

	#Create a unique ID for video using timestamp...
	vid_id = str(int(time.time()))

	#Call functions...
	upload_file_to_s3(file, vid_id)
	transcode_file_to_mp4(file, vid_id)


#Execute script...
init()