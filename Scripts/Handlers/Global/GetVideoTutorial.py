'''
    # Get video tutorial's path
'''

import os

import config as CONFIG


def get_video_tutorial():
    '''
        ## get the path of video tutorial
        - returns None on fail
    '''
    try:
        if os.path.exists(CONFIG.VIDEO_TUTORIAL_PATH):
            return CONFIG.VIDEO_TUTORIAL_PATH
    except:
        pass
    return None
