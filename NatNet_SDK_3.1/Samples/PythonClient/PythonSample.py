# Copyright © 2018 Naturalpoint
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# OptiTrack NatNet direct depacketization sample for Python 3.x
#
# Uses the Python NatNetClient.py library to establish a connection (by creating a NatNetClient),
# and receive data via a NatNet connection and decode it using the NatNetClient library.
import argparse
import time
from NatNetClient import NatNetClient
import numpy as np

outputfile = None
data = []

# This is a callback function that gets connected to the NatNet client and called once per mocap frame.
def receiveNewFrame(frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                    labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged):
    #print("Received frame", frameNumber)
    return


# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receiveRigidBodyFrame(id, position, rotation):
    #print("Received frame for rigid body " + str(id) + " " + str(position) + " " + str(rotation))
    if outputfile != None:
        ts = time.time()
        item = [ts]
        for i in range(len(position)):
            item.append(position[i])
        for i in range(len(rotation)):
            item.append(rotation[i])
        data.append(item)
        print(item)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default="172.24.71.201", help='host to connect to')
    parser.add_argument('--file', help='write to file')

    args = parser.parse_args()
    outputfile = args.file

    # This will create a new NatNet client
    streamingClient = NatNetClient(args.host)

    # Configure the streaming client to call our rigid body handler on the emulator to send data out.
    streamingClient.newFrameListener = receiveNewFrame
    streamingClient.rigidBodyListener = receiveRigidBodyFrame

    # Start up the streaming client now that the callbacks are set up.
    # This will run perpetually, and operate on a separate thread.
    streamingClient.run()

    to_stop = input("Enter to enter")
    if args.file is not None:
        print(np.asarray(data).shape)
        np.savetxt(args.file + ".csv", np.asarray(data))
        exit()

