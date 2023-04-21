# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from contextlib import contextmanager

import squish
import test
import os
import squishinfo

def _failures_results_count():
    return test.resultCount("errors") + test.resultCount("fatals") + test.resultCount("xpasses") + test.resultCount("fails")

def _videos_set() -> set:
    video_dir = os.path.join(squishinfo.resultDir, squishinfo.testSuiteName,squishinfo.testCaseName,"attachments")
    
    videos_list = set()
    
    if not os.path.exists(video_dir):
        return videos_list

    for file in os.listdir(video_dir):
        if file.endswith('.mp4'):
            videos_list.add(file)
    return videos_list

def _remove_videos(videos: set):
    video_dir = os.path.join(squishinfo.resultDir, squishinfo.testSuiteName,squishinfo.testCaseName,"attachments")
    for video_name in videos:
        test.log(f"Remove video: {video_name}")
        file_name = os.path.join(video_dir,video_name)
        os.remove(file_name)

@contextmanager
def video_capture(message: str, delete_on_success = False) -> None:
    """Allows using Squish's video capture as context managers.
    """

    if(delete_on_success):
        initial_videos = _videos_set()
        initial_result_count = _failures_results_count()
    
    test.startVideoCapture(message)
    
    try:
        yield
    except Exception:
        raise
    finally:
        test.stopVideoCapture(message)
        if(delete_on_success):
            new_failures = _failures_results_count() - initial_result_count
            if (new_failures==0):
                new_videos = _videos_set() - initial_videos
                _remove_videos(new_videos)
                