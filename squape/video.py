# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import os
from contextlib import contextmanager

import squishinfo
import test


def _failures_results_count() -> int:
    """
    This function returns the total number of failures in test results by adding up
    all the counts for errors, fatals, xpasses and fails.

    Returns:
        int: The total number of failures in test results.
    """
    return (
        test.resultCount("errors")
        + test.resultCount("fatals")
        + test.resultCount("xpasses")
        + test.resultCount("fails")
    )


def _videos_set() -> set:
    """
    This function returns a set of existing video filenames in video directory
    RESULT_DIR/TEST_SUITE_NAME/TEST_CASE_NAME/attachments.

    Returns:
        set: The set of filenames with mp4 extension
    """
    video_dir = os.path.join(
        squishinfo.resultDir,
        squishinfo.testSuiteName,
        squishinfo.testCaseName,
        "attachments",
    )

    videos_set = set()

    if not os.path.exists(video_dir):
        return videos_set

    for file in os.listdir(video_dir):
        if file.endswith(".mp4"):
            videos_set.add(file)
    return videos_set


def _remove_videos(videos: set) -> None:
    """
    Remove videos from the attachments directory.

    Args:
        videos (set): A set of video names to remove.
    """
    video_dir = os.path.join(
        squishinfo.resultDir,
        squishinfo.testSuiteName,
        squishinfo.testCaseName,
        "attachments",
    )
    for video_name in videos:
        test.log(f"Remove video: {video_name}")
        file_name = os.path.join(video_dir, video_name)
        os.remove(file_name)


@contextmanager
def video_capture(message: str, delete_on_success: bool = False) -> None:
    """Allows using Squish's video capture as context managers.
    https://doc.qt.io/squish/squish-api.html#test-startvideocapture-message
    Optionally delete a captured video when the execution was successful (no failures)

    Args:
        message (str): log a video n the test report using the specified message
        delete_on_success (bool): Whether to delete captured video
        when there were no failures. Defaulting to False.

    """

    if delete_on_success:
        initial_videos = _videos_set()
        initial_result_count = _failures_results_count()

    test.startVideoCapture(message)

    try:
        yield
    except Exception:
        raise
    finally:
        test.stopVideoCapture(message)
        if delete_on_success:
            new_failures = _failures_results_count() - initial_result_count
            if new_failures == 0:
                new_videos = _videos_set() - initial_videos
                _remove_videos(new_videos)
