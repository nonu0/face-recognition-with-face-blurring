import sys
import os

# Add the project root to sys.path so Python can find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import cv2
import numpy as np
from app.services.face_blur import roi_blur, face_roi
import pytest

from unittest.mock import MagicMock


@pytest.fixture
def dummy_frame():
    """Creates a dummy 100x100 black frame for testing."""
    return np.zeros((100, 100, 3), dtype=np.uint8)



@pytest.fixture
def dummy_detection():
    class DummyBox:  #Create dummy bounding box
        def __init__(self, x1, y1, x2, y2):
            self.xyxy = np.array([[x1,y1,x2,y2]])
            
        
    class DummyDetection:
        def __init__(self, boxes):
            self.boxes = boxes
            
    return DummyDetection([DummyBox(10,10,50,50)])


def test_face_roi_vlid(dummy_frame):
    x1,y1,x2,y2 = 10,10,50,50
    result = face_roi(dummy_frame,x1,y1,x2,y2)
    assert result is not None
    assert len(result) == 5
    assert isinstance(result,tuple)
    assert result[4].shape == (y2-y1,x2-x1,3)
    
def test_face_roi_zero_size(dummy_frame):
    result = face_roi(dummy_frame,20,20,20,40)
    assert result is None
    
    result = face_roi(dummy_frame,20,20,40,20)
    assert result is None
    
# def test_face_empty_roi(dummy_frame):
#     result = face_roi(dummy_frame,90,90,110,110,blur_level='strong')
#     assert result is None

def test_face_roi_invalid_blur_level(dummy_frame):
    result = face_roi(dummy_frame,10,10,50,50,blur_level='invalid')
    assert result is not None
    assert result[4].shape == (40,40,3)

def test_roi_blur(dummy_detection,dummy_frame,monkeypatch):
    def mock_face_roi(frame,x1,y1,x2,y2,blur_level='strong'):
        return x1,y1,x2,y2, np.full((y2-y1,x2-x1,3),255,dtype=np.uint8) # fake white blurred roi
    monkeypatch.setattr('app.services.face_blur.face_roi', mock_face_roi)
    
    roi_blur(dummy_detection,dummy_frame)
    
    assert np.array_equal(dummy_frame[10:50,10:50],np.full((40,40,3),255)) # should be white
    
def test_roi_blur_no_dewtections(dummy_frame):
    class EmptyDetections:
        def __init__(self):
            self.boxes = []
    empty_detections = EmptyDetections()
    roi_blur(empty_detections,dummy_frame)
    
    assert np.array_equal(dummy_frame,np.zeros((100,100,3),dtype=np.uint8))