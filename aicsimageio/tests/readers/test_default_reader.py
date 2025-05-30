#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Tuple

import numpy as np
import pytest

from aicsimageio import exceptions
from aicsimageio.readers.default_reader import DefaultReader

from ..conftest import get_resource_full_path, host
from ..image_container_test_utils import run_image_file_checks


@host
@pytest.mark.parametrize(
    "filename, set_scene, expected_shape, expected_dims_order",
    [
        ("example.bmp", "Image:0", (480, 640, 4), "YXS"),
        ("example.png", "Image:0", (800, 537, 4), "YXS"),
        ("example.jpg", "Image:0", (452, 400, 3), "YXS"),
        ("example.gif", "Image:0", (72, 268, 268, 4), "TYXS"),
        (
            "example_invalid_frame_count.mp4",
            "Image:0",
            (55, 1080, 1920, 3),
            "TYXS",
        ),
        (
            "example_valid_frame_count.mp4",
            "Image:0",
            (72, 272, 272, 3),
            "TYXS",
        ),
        pytest.param(
            "example.txt",
            None,
            None,
            None,
            marks=pytest.mark.raises(exception=exceptions.UnsupportedFileFormatError),
        ),
        pytest.param(
            "example.png",
            "Image:1",
            None,
            None,
            marks=pytest.mark.raises(exception=IndexError),
        ),
    ],
)
def test_default_reader(
    filename: str,
    host: str,
    set_scene: str,
    expected_shape: Tuple[int, ...],
    expected_dims_order: str,
) -> None:
    # Construct full filepath
    uri = get_resource_full_path(filename, host)

    # Run checks
    run_image_file_checks(
        ImageContainer=DefaultReader,
        image=uri,
        set_scene=set_scene,
        expected_scenes=("Image:0",),
        expected_current_scene="Image:0",
        expected_shape=expected_shape,
        expected_dtype=np.dtype(np.uint8),
        expected_dims_order=expected_dims_order,
        expected_channel_names=None,
        expected_physical_pixel_sizes=(None, None, None),
        expected_metadata_type=dict,
    )


def test_ffmpeg_header_fail() -> None:
    with pytest.raises(IOError):
        # Big Buck Bunny
        DefaultReader("https://archive.org/embed/archive-video-files/test.mp4")
