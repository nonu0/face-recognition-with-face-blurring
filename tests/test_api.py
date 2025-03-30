import pytest
import time
from fastapi.testclient import TestClient
import requests
BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def wait_for_server():
    """Waits for the FastAPI server to start before running tests."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/docs", timeout=3)
            if response.status_code == 200:
                return  # Server is up
        except requests.ConnectionError:
            time.sleep(2)  # Wait before retrying
    pytest.fail("FastAPI server did not start.")


# def test_video_stream():
#     """Tests if the /video/0 endpoint starts a video stream."""
#     url = f"{BASE_URL}/video/0"
    
#     response = requests.get(url, stream=True, timeout=10)
    
#     assert response.status_code == 200, f"Failed with status: {response.status_code}"
#     assert response.headers["Content-Type"].startswith("multipart/x-mixed-replace"), "Invalid content type"

#     # Read first chunk to verify stream
#     first_chunk = next(response.iter_content(chunk_size=1024), None)
#     assert first_chunk, "No data received from the video stream"

#     # Stop streaming after receiving some data
#     response.close()




# @pytest.mark.parametrize("source", ["invalid_path.mp4", "999"])
# def test_invalid_video_source(client, source):
#     """
#     Tests handling of invalid video sources (non-existent file & incorrect webcam ID).
#     """
#     response = client.get(f"/video/{source}")
    
#     assert response.status_code == 400
#     assert "Could not open video source" 

# def test_video_stream_performance(client):
#     """
#     Measures response time for video stream startup (should be < 3s).
#     """
#     start_time = time.time()
#     response = client.get("/video/0")
#     end_time = time.time()

#     assert response.status_code == 200
#     assert (end_time - start_time) < 3, "Video stream took too long to start"
