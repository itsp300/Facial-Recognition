import communication
import threading
import time
import ssl
import base64
import face_recon
from typing import Dict


debug = True
ws = None


def debug_log(message):
    if debug:
        print("[Main]" + str(message))


def start_queue_handler():
    while True:
        time.sleep(0.3) # artificial wait to prevent spamming cpu time checking, change as desired
        if not communication.request_queue.empty():
            message = communication.request_queue.get()
            if len(message) < 2048: # gets rid of 
                debug_log("Dispatching queued jwt request: " + str(message))
            else:
                debug_log("Dispatching queued jwt request [Truncated, too long for console (" + str(len(message)) + ")]")
            try:
                ws.send(message)
            except Exception as e:
                debug_log("Queue: " + str(e))
 

def use_communication_queue_thread():
    queue_thread = threading.Thread(target=start_queue_handler)
    queue_thread.start()
    
    
def use_communication_and_run():
    global ws
    while True:
        try:
            ws = communication.start_websocket()
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})  # REMOVE CERT_NONE WHEN IN PRODUCTION ENVIRONMENT
        except KeyboardInterrupt:
            break


# handler method, you write a bunch of these to handle different messages sent by server
def handle_auth_timeout(payload):
    print("Auth Timeout: " + str(payload))


def face_rec_image(payload: Dict):
    record_id = payload['record_id']
    print("Obtaining Facial Image Data")
    req_encode = payload['image']
    # Decode the image into temp image file
    image_64_decode = base64.decodebytes(req_encode)
    image_result = open('testDrive.jpg', 'wb')
    image_result.write(image_64_decode)

    people = face_recon.classify_face('testDrive.jpg')
    print("Students: " + people)

    communication.request_send_jwt(
        {
            "type": "face_rec",
            "students": "people",
            "record_id": payload['record_id']
        }
    )


def face_rec_identify(payload: Dict):
    print("Something")


def face_rec_detail(payload: Dict):
    print("Detailed Info")

    id = payload["id"]
    
    communication.request_send_jwt(
        {
            "type": "face_rec_details",
            "identified": [
                {
                    "person_id": "RJMMLYX21",
                    "certainty": "56"
                },
                {
                    "person_id": "PR3C56TY",
                    "certainty": "56"
                }
            ]
        }
    )


def main():
  print("Server Started!")
  # define what message types we want to handle
  communication.register_message_type("auth_timeout", handle_auth_timeout)
  communication.register_message_type("face_rec", face_rec_image)
  communication.register_message_type("face_rec_identifier", face_rec_identify)
  communication.register_message_type("face_rec_details", face_rec_detail)

    # good place to start the facial recognition thread(s), or you could spawn them in the message handlers just above this line
  # start queue thread
  use_communication_queue_thread()
  # start websocket - code will never run past here since .run_forever blocks infinitely
  use_communication_and_run()


if __name__ == '__main__':
    main()

