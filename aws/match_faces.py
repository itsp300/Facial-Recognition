from picamera import PiCamera
import time
import boto3

directory = 'C:\Users\Br\Documents\GitHub Projects\attendance_facial_recognition\aws' #folder name on your raspberry pi

collectionId='faces' #collection name

rek_client=boto3.client('rekognition',
                        aws_access_key_id='AKIAUMTBC6HNMLK6TQGA',
                        aws_secret_access_key='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',)

while True:
        image = 'test.jpg'
        print('captured '+image)
        with open(image, 'rb') as image:
            try: #match the captured imges against the indexed faces
                match_response = rek_client.search_faces_by_image(CollectionId=collectionId, Image={'Bytes': image.read()}, MaxFaces=1, FaceMatchThreshold=85)
                if match_response['FaceMatches']:
                    print('Hello, ',match_response['FaceMatches'][0]['Face']['ExternalImageId'])
                    print('Similarity: ',match_response['FaceMatches'][0]['Similarity'])
                    print('Confidence: ',match_response['FaceMatches'][0]['Face']['Confidence'])
    
                else:
                    print('No faces matched')
            except:
                print('No face detected')
            

        time.sleep(10)       
