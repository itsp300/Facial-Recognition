import os
import communication
import threading
import time
import ssl
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
    print("what to do when I receive this message")
    print(payload['image'])


def main():
  print("Server Started!")
  # define what message types we want to handle
  communication.register_message_type("auth_timeout", handle_auth_timeout)

  communication.register_message_type("face_rec", face_rec_image)

    # good place to start the facial recognition thread(s), or you could spawn them in the message handlers just above this line
  # start queue thread
  use_communication_queue_thread()
  # start websocket - code will never run past here since .run_forever blocks infinitely
  use_communication_and_run()


if __name__ == '__main__':
    main()

