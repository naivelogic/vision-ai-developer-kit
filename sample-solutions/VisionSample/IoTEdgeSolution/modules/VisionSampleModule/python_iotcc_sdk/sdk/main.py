# Copyright (c) 2018, The Linux Foundation. All rights reserved.
# Licensed under the BSD License 2.0 license. See LICENSE file in the project root for
# full license information.

import argparse
import sys
import time
import subprocess
import utility
import os
import iot

from camera import CameraClient

restartCamera = False
def main(protocol=None):
    #while(True):
        #time.sleep(1)
    print("\nPython %s\n" % sys.version)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--pushmodel',help ='sets whether to push the model and required files to device or not', default=False)
    parser.add_argument('--ip', help='ip address of the camera', default=utility.getWlanIp())
    parser.add_argument('--username', help='username of the camera', default='admin')
    parser.add_argument('--password', help='password of the camera', default='admin')
    args = parser.parse_args()
    if args.pushmodel is not None:
        mypushmodel = args.pushmodel
        print("setting value from argu -p pushmodel to :: %s" % mypushmodel)
    ip_addr = args.ip
    username = args.username
    password = args.password
    
    #getting Iot hub sdk ready with hub manager
    hub_manager = iot.HubManager()
    print("value of restartCamera is :: " + str(iot.restartCamera))
    #Connecting to camer using ipcWebServer SDK and turing camera on and then starting inferencing 
    with CameraClient.connect(ip_address=ip_addr, username=username, password=password) as camera_client:
        #transferring model files to camera for inferencing 
        utility.transferdlc(mypushmodel)
       
        #this call we set the camera to dispaly over HDMI 
        print(camera_client.configure_preview(resolution="1080P",encode="AVC/H.264",bitrate="1.5Mbps",display_out=1))
        # this call turns on the camera and start transmetting over RTSP and HDMI a stream from camera 
        camera_client.set_preview_state("on")
       
        #rtsp stream address 
        rtsp_stream_addr = str(camera_client.preview_url)
        print("rtsp stream is :: " + rtsp_stream_addr)
        #uploading rtsp stream address to iot hub as twin property so that user one can know what there rtsp address is and then use it on vlc media player 
        hub_manager.iothub_client_sample_run(rtsp_stream_addr)

        #Vam(Video analytics engine ) this will take the model and run on thee device 
        camera_client.set_analytics_state("on")
        print(camera_client.vam_url)
        
        # this will set the frames to be overlayed with information recieved from inference results ffrom your model
        camera_client.configure_overlay("inference")

        #Turning overlay to Truse to see inferencing frame overlayed with inference results
        camera_client.set_overlay_state("on")

        # heer we will use gstreamer to get the inference results from camera into thsi module and then send them up to cloud or another module
        try:
            with camera_client.get_inferences() as results:
                print_inferences(results,camera_client,hub_manager)
        except KeyboardInterrupt:
            print("Stopping")
        try:
            print("inside infinite loop now")
            while(True):
                time.sleep(2)
        except KeyboardInterrupt:
            print("Stopping")

        # turning everything off and logging out ...
        camera_client.set_overlay_state("off")

        camera_client.set_analytics_state("off")

        camera_client.set_preview_state("off")

def print_inferences(results=None, camera_client=None,hub_manager=None):
    print("")
    for result in results:
        if iot.restartCamera :
            print(iot.restartCamera)
            restartInference(camera_client,hub_manager)
        if result is not None and result.objects is not None and len(result.objects):
            timestamp = result.timestamp
            if timestamp:
                print("timestamp={}".format(timestamp))
            else:
                print("timestamp= " + "None")
            for object in result.objects:
                if iot.restartCamera :
                    print(iot.restartCamera)
                    restartInference(camera_client,hub_manager)
                id = object.id
                print("id={}".format(id))
                label = object.label
                print("label={}".format(label))
                confidence = object.confidence
                print("confidence={}".format(confidence))
                x = object.position.x
                y = object.position.y
                w = object.position.width
                h = object.position.height
                print("Position(x,y,w,h)=({},{},{},{})".format(x, y, w, h))
                hub_manager.SendMsgToCloud("I see " + str(label) + " with confidence :: " + str(confidence))
                print("")
        else:
            print("No results")

def restartInference(camera_client = None,hub_manager = None) :
    """camera_client.set_overlay_state("off")
    camera_client.set_analytics_state("off")
    time.sleep(5)
    camera_client.set_analytics_state("on")
    camera_client.set_overlay_state("on")"""
    iot.restartCamera = False
    camera_client.set_preview_state("off")
    camera_client.logout()
    time.sleep(2)
    ip_addr = utility.getWlanIp()
    with CameraClient.connect(ip_address=ip_addr, username='admin', password='admin') as camera_client:
        #this call we set the camera to dispaly over HDMI 
        #print(camera_client.configure_preview(resolution="1080P",display_out=1))
        # this call turns on the camera and start transmetting over RTSP and HDMI a stream from camera 
        camera_client.set_preview_state("on")
        #Vam(Video analytics engine ) this will take the model and run on thee device 
        camera_client.set_analytics_state("on")
        print(camera_client.vam_url)
        
        # this will set the frames to be overlayed with information recieved from inference results ffrom your model
        camera_client.configure_overlay("inference")

        #Turning overlay to Truse to see inferencing frame overlayed with inference results
        camera_client.set_overlay_state("on")

        # heer we will use gstreamer to get the inference results from camera into thsi module and then send them up to cloud or another module
        try:
            with camera_client.get_inferences() as results:
                print_inferences(results,camera_client,hub_manager)
        except KeyboardInterrupt:
            print("Stopping")
        try:
            print("inside infinite loop now")
            while(True):
                time.sleep(2)
        except KeyboardInterrupt:
            print("Stopping")

        # turning everything off and logging out ...
        camera_client.set_overlay_state("off")

        camera_client.set_analytics_state("off")

        camera_client.set_preview_state("off")

    


if __name__ == '__main__':
    main()