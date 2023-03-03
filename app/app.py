#!/usr/bin/env python3
"""
Created on Wed Mar 01 07:05:11 2023

1. This is a python version of the Raj's bash script that provides an easy way to move 
Mobotix camera to a preset position. 
2. It uses the "curl" command via subprocess to send RS232 commands to the camera.
3. Currently it scans all the points1-32, but it should be able to perform loop-scan over given set of points.
"""

import argparse
import subprocess
import os
import time

from waggle.plugin import Plugin
# Dictionary contains "presets" which maps preset position numbers to the corresponding string for curl command for that position. 
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



def loop_check(i, m):
        '''
        A helper function used to control the loop-scan.
        
        Returns True if i < m, where i is a loop counter 
        and m is the number of times to perform the loop-scan. 
        '''
        return m < 0 or i < m


# Scans all preset positions in loop
def scan_preset_loop(args):
    '''
    Performs the loop-scan over all preset positions. 
    
    It calls the move_to_preset function for each preset position
    and publishes the camera message to the beehive.
    '''
    preset_id = [i for i in range(1, 33)]
    loops=0
    with Plugin() as plugin:
        while loop_check(loops, args.loops):
            loops = loops + 1
            for ptid in preset_id:
                status = move_to_preset(ptid, args)
                plugin.publish('mobotix.move.status', status)


# Move to single preset position and report to the beehive.
def move_preset_single(args):
    '''
    Moves the camera to a single preset position and publishes the camera message to the beehive.
    '''    
    preset_id = args.preset
    with Plugin() as plugin:
        status = move_to_preset(ptid, args)
        plugin.publish('mobotix.move.status', status)


# Move to only single preset position (Does not report to the beehive)
def move_to_preset(pt_id, args):
    '''
    This function sends the curl command for the given preset position to the camera via subprocess. 
    It returns the result of the "curl" command. 
    Do not call it directly as this will not publish error messages in the beehive.
    '''
    preset_code = presets.get(pt_id)
    if not preset_code:
        print("Invalid preset number")
        return -1

    cmd = ["curl",
        "-u",
        args.user+':'+args.password,
        "-X",
        "POST",
        "http://{}/control/rcontrol?action=putrs232&rs232outtext=".format(args.ip)+preset_code]

    #print(cmd)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        time.sleep(args.interval)
        return result.stdout

    except subprocess.CalledProcessError as e:
        #print("Error: {}".format(e))
        return e

    return 0


# calls move functions 
def main(args):
    # scan over all location if value=99
    if args.preset==99:
        scan_preset_loop(args)
    else:
        move_preset_single(args)





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
        "-l",
        "--loops",
        dest="loops",
        type=int,
        default=os.getenv("LOOPS", -1),
        help="Number of loops to perform. Defaults to 'infinite' (-1)",
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

