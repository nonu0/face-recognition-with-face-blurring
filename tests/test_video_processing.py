import unittest
from unittest.mock import patch, MagicMock
import cv2
from fastapi import HTTPException
from app.utils.video_processing import CustomVideoCapture
from config.config import config
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCustomVideoCapture(unittest.TestCase):
    
    @patch('cv2.VideoCapture')
    def test_valid_video_source_initialization(self, mock_videocap):
        mock_videocap.return_value.isOpened.return_value = True
        video_capture = CustomVideoCapture(r'C:\Users\Administrator\work\Blur\face_blur\app\Assets\walk.mp4')
        self.assertTrue(video_capture.cap.isOpened())

    # @patch('cv2.VideoCapture')
    # def test_invalid_video_source_raises_exception(self, mock_videocap):
    #     mock_videocap.return_value.isOpened.return_value = False
    #     with self.assertRaises(HTTPException) as context:
    #         CustomVideoCapture(src='invalid_source.mp4')
    #     self.assertEqual(context.exception.status_code, 400)
        
    # @patch('cv2.VideoCapture')
    # def test_decode_src_valid_webcam(self, mock_videocap):
    #     mock_videocap.return_value.isOpened.return_value = True
    #     video_capture = CustomVideoCapture(src='0')
    #     self.assertEqual(video_capture.src, 0)  # Ensure it converts "0" to an integer

    # @patch('cv2.VideoCapture')
    # @patch('app.models.model_loader')
    # def test_video_stream_yields_frames(self, mock_load_model, mock_videocap):
    #     mock_videocap.return_value.isOpened.return_value = True
        
    #     # Create a fake image frame (black image of 640x480)
    #     dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    #     # Mock read() method to return dummy frame 3 times, then stop
    #     mock_videocap.return_value.read.side_effect = [(True, dummy_frame)] * 3 + [(False, None)]

    #     mock_model = MagicMock()
    #     mock_model.track.return_value = [MagicMock()]
    #     mock_load_model.return_value = mock_model

    #     video_capture = CustomVideoCapture(r'C:\Users\Administrator\work\Blur\face_blur\app\Assets\walk.mp4')
        
    #     stream_generator = video_capture.video_stream()

    #     frame_count = 0
    #     for frame in stream_generator:
    #         assert isinstance(frame, bytes)  # Ensure the output is a byte stream
    #         frame_count += 1
        
    #     assert frame_count == 3  # Ensure exactly 3 frames were processed

    # @patch('cv2.VideoCapture')
    # def test_video_stream_stops_on_no_frame(self, mock_videocap):
    #     mock_videocap.return_value.isOpened.return_value = True
    #     mock_videocap.return_value.read.return_value = (False, None)
        
    #     video_capture = CustomVideoCapture(r'C:\Users\Administrator\work\Blur\face_blur\app\Assets\walk.mp4')
    #     stream_generator = video_capture.video_stream()
        
    #     with self.assertRaises(StopIteration):
    #         next(stream_generator)

if __name__ == '__main__':
    unittest.main()
