# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import os
import shutil
from contextlib import contextmanager
from importlib import resources
from pathlib import Path

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
    Remove videos from the attachments directory. The original video will be replaced
    with a placeholder video with size of 10.6 KB.

    Args:
        videos (set): A set of video names to remove.
        Does nothing when the set is empty.
    """

    if not len(videos):
        return None

    video_dir = os.path.join(
        squishinfo.resultDir,
        squishinfo.testSuiteName,
        squishinfo.testCaseName,
        "attachments",
    )

    res_container = Path(resources.files(__package__), Path("resources"))
    empty_video = Path(res_container, "empty_video_with_message.mp4")

    for video_name in videos:
        test.log(f"Remove video: {video_name}")
        orig_video = Path(video_dir, video_name)
        shutil.copy(empty_video, orig_video)


@contextmanager
def video_capture(message: str = None, delete_on_success: bool = False) -> None:
    """Allows using Squish's video capture as context managers.
    https://doc.qt.io/squish/squish-api.html#test-startvideocapture-message
    Optionally remove a captured video when the execution was successful (no failures)

    Args:
        message (str): log a video n the test report using the specified message.
        Defaulting to None.
        delete_on_success (bool): Whether to remove captured video
        when there were no failures. Defaulting to False.

    Example:
        with video_capture(delete_on_success=True):
            # code with actions and verifications

    """

    if delete_on_success:
        initial_videos = _videos_set()
        initial_result_count = _failures_results_count()

    if message is not None:
        test.startVideoCapture(message)
    else:
        test.startVideoCapture()

    try:
        yield
    except Exception:
        raise
    finally:

        if message is not None:
            test.stopVideoCapture(message)
        else:
            test.stopVideoCapture()

        if delete_on_success:
            new_failures = _failures_results_count() - initial_result_count
            if new_failures == 0:
                new_videos = _videos_set() - initial_videos
                _remove_videos(new_videos)


def remove_videos_on_success() -> None:
    """
    Remove all captured videos when the execution was successful (no failures)
    """
    if _failures_results_count() == 0:
        videos_to_remove = _videos_set()
        _remove_videos(videos_to_remove)
