#!/usr/bin/env python3
"""
Created on Wed Mar 01 07:05:11 2023

1. This is a python version of the Raj's bash script that provides an easy way to move 
Mobotix camera to a preset position. 
2. It uses the "curl" command via subprocess to send RS232 commands to the camera.
"""

import argparse
import subprocess
import os
import time



def main(args):

    presets = {
        1: "%FF%01%00%07%00%01%09",
        2: "%FF%01%00%07%00%02%0A",
        3: "%FF%01%00%07%00%03%0B",
        4: "%FF%01%00%07%00%04%0C",
        5: "%FF%01%00%07%00%05%0D",
        6: "%FF%01%00%07%00%06%0E",
        7: "%FF%01%00%07%00%07%0F",
        8: "%FF%01%00%07%00%08%10",
        9: "%FF%01%00%07%00%09%11",
        10: "%FF%01%00%07%00%10%18",
        11:"%FF%01%00%07%00%11%19",
        12:"%FF%01%00%07%00%12%1A",
        13:"%FF%01%00%07%00%13%1B",
        14:"%FF%01%00%07%00%14%1C",
        15:"%FF%01%00%07%00%15%1D",
        16:"%FF%01%00%07%00%16%1E",
        17:"%FF%01%00%07%00%17%1F",
        18:"%FF%01%00%07%00%18%20",
        19:"%FF%01%00%07%00%19%21",
        20:"%FF%01%00%07%00%20%28",
        21:"%FF%01%00%07%00%21%29",
        22:"%FF%01%00%07%00%22%2A",
        23:"%FF%01%00%07%00%23%2B",
        24:"%FF%01%00%07%00%24%2C",
        25:"%FF%01%00%07%00%25%2D",
        26:"%FF%01%00%07%00%26%2E",
        27:"%FF%01%00%07%00%27%2F",
        28:"%FF%01%00%07%00%28%30",
        29:"%FF%01%00%07%00%29%31",
        30:"%FF%01%00%07%00%30%38",
        31:"%FF%01%00%07%00%31%39",
        32:"%FF%01%00%07%00%32%3A"
    }


    # loop over all location if default value
    if args.preset==99:
        preset_id = [i for i in range(1, 33)]
    else:
        preset_id = [args.preset]


    for id in preset_id:
        preset_code = presets.get(id)
        if not preset_code:
            print("Invalid preset number")
            return

        cmd = ["curl",
            "-u",
            args.user+':'+args.password,
            "-X",
            "POST",
            "http://{}/control/rcontrol?action=putrs232&rs232outtext=".format(args.ip)+preset_code]

        #print(cmd)

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            #print(result.stdout)
            time.sleep(args.interval)
        except subprocess.CalledProcessError as e:
            print("Error: {}".format(e))




if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        required=True,
        type=str,
        dest="ip",
        default=os.getenv("CAMERA_IP", ""),
        help="Camera IP or URL",
    )
    parser.add_argument(
        "-pt",
        "--preset",
        dest="preset",
        type=int, 
        default= 99,
        help="preset location id"
        )
    parser.add_argument(
        "-i",
        "--interval",
        dest="interval",
        type=int,
        default=os.getenv("MOVE_INTERVAL", 120),
        help="Seconds to sleep in-between movements",
    )
    parser.add_argument(
        "-u",
        "--user",
        dest="user",
        type=str,
        default=os.getenv("CAMERA_USER", "admin"),
        help="Camera User ID",
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="password",
        type=str,
        default=os.getenv("CAMERA_PASSWORD", "meinsm"),
        help="Camera Password",
    )
    args = parser.parse_args()
    main(args)

