import boto
import boto.s3
import sys
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'AKIAI7AF7AL3SQETDXIA'
AWS_SECRET_ACCESS_KEY = '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'

bucket_name ='hisaab.navgurukul.org'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)


bucket = conn.create_bucket("monu17",
    location=boto.s3.connection.Location.DEFAULT)

testfile = "/home/navgurukul/hisaab/HisaabProject/media/bankScreenshot/34/download_8YxFMZq.png"
print 'Uploading %s to Amazon S3 bucket %s' % \
   (testfile, bucket_name)



k = Key(bucket)
k.key = 'download_8YxFMZq.png'
k.set_contents_from_filename(testfile)
