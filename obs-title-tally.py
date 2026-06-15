import obspython as obs # type: ignore

"""
Filename: obs-title-tally.py
Author: snuwehy
Date: 1 June 2026
Version: 1.0
Description: An OBS script that runs in the background during recordings that keeps track of the Game Capture and renames the highest/multiple captures
"""

#   Track-> Tally-> Stop-> Rename
#   Runs continuously in the background as long as OBS is open
#   Tally in Python memory like dictionary

#   1. On Recording Start: Clear Previous Dictionary/Memory
#   2. During Recording: Poll OBS and increment the name of active Game Capture
#   3. On Record Stop: Find the highest int in dictionary, rename the latest/recorded recording file

#   obs_frontend_add_event_callback: listen for events like "Recording Stated" and "Recording Stopped" without infinite while loop
#   obs_frontend_get_last_recording: function that hands exact file path of last recording
#   timer_add: timer for polling interval (check source every x seconds)
#   obs_get_source_by_name: target a specific "Game Capture" source
#   obs_source_get_settings: read internal settings of source [to see executable or window title being captured/hooked to]

#   Notes:
#   Title/Game Attribute is appended to the start of the file [prefix], therefore, when sorting by title, games will be grouped while sorting by creation date will store by chronological absolute datetime
#   Checking that the capture is active
#       1. Check that the game capture is being recorded
#       2. Check that the source is visible/showing
#       3. Check that Game Capture is actually capturing a live game
#   There is a Multiple Game Capture Feature:
#       the timer interval will keep track of multiple things, incase you switch contents throughout the recording, if so. A threshold will determine if the additional/other sources will be put into the title, by time.
#       math works out ~ 1 poll = 5 seconds -> 10 minutes = 600 seconds, tally > 120 threshold to be renamed. otherwise one or none

#   script prints are logged into script log. yeah.

def on_event(event):
    '''
    This just listens for events from OBS, anytime an event happens, it is sent to all the scripts
    the scripts look at input *event* and check it for the particular event they want (because event 
    is an enum) then the script does what it wants to do, basically scripts run ontop and do extra stuff, not outright modify but "enhance" programs per se'''
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        print("~[Title Tally] Recording STARTED! The Clock Starts NOW!~ ")
        #   then start timer thang

    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        print("[Title Tally] RED LIGHT! Recording has STOPPED! Tally Up The Numbers!")
        # stop timer, but then also rename file

#   the script lives and dies by on_event, if anything, it is what makes an OBS script what it is, everything below is just filling out the struct essentially. on_event is what is *dynamically mounted* and so therefore must be taken care of with special care

def script_description():
    # script_description(): function that returns a string, it is what OBS displays in the Scripts window UI so you know what the loaded script is
    return "Keeps track of Game Capture source during recordings and renames the output file"

def script_load(settings):
    # basically inits the script, loads the script for OBS to handle behind the scenes
    # script_load(settings): fires exactly once, this is first loaded into OBS [when OBS is launched], where init happens, where we need to call obs_frontend_add_event_callback to start listening for recordings
    print("[Title Tally] Script loaded.")
    obs.obs_frontend_add_event_callback(on_event) 

def script_unload():
    #   for my use, its called when OBS is closed, but is also when script is removed or reloaded ie destruct() or unmount() something of the like
    # script_unload(): called when script is removed or OBS closes, best to clean up when its unloaded, remove timer and event callbacks
    print("[Title Tally] Script unloaded, sweep sweep sweep.")
    obs.obs_frontend_remove_event_callback(on_event)