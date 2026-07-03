import cv2
import math
import pose
import sample
video_path = "data/raw/spike.mp4"

def collect_frame_data(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    landmarker = pose.build_landmarker()

    frame_data = []
    frame_index = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.detect_pose(landmarker, rgb, frame_index, fps)

        frame_data.append({
            "frame_index": frame_index,
            "timestamp_ms": int(frame_index * (1000 / fps)),
            "landmarks": result["landmarks"] if result else None,
            "world_landmarks": result["world_landmarks"] if result else None,
        })
        frame_index += 1

    landmarker.close()
    cap.release()
    return frame_data


def find_contact_frame(frame_data):

    # right_wrist_y = []
    frame_i = []
    index = 0
    # highest_index = 0
    highest_y = 1
    for frame in frame_data:
        frame_i.append(index)
        
        if frame["landmarks"] is None:
            index += 1
            continue
        else:
            highest = frame["landmarks"]
            if highest[16].visibility < 0.5:
                index += 1
                continue
            if highest[16].y < highest_y:
                highest_y = highest[16].y
                highest_index = index
            index += 1
            # highest_y = highest[16].y
            



            # right_wrist_y.append(highest_y)
    
    return frame_data[highest_index]
        # both = zip(index, right_wrist_y)
        # dict_i = both[min(right_wrist_y) - 1]
        # return frame_data[dict_i]



def find_contact_angle(contact_frame):
    landmarks = contact_frame["landmarks"]
    shoulder = landmarks[12]
    wrist = landmarks[16]

    if shoulder.visibility < 0.5 or wrist.visibility < 0.5:
        return None

    dx = wrist.x - shoulder.x
    dy = wrist.y - shoulder.y

    # atan2(dx, -dy) measures from straight up (0,-1), not from the x-axis (atan2's
    # usual 0). Sign convention for forward-vs-behind is camera-setup-specific and
    # hasn't been empirically verified against this footage yet.
    angle_radians = math.atan2(dx, -dy)
    return math.degrees(angle_radians)

def find_straight_frame(is_standing_straight, frame_data):
    for frame in frame_data:
        if sample.is_standing_straight(frame):
            return frame
        if frame is frame_data[-1]:
            return "The user does not stand straight in the video"
        continue


def contact_height(frame, contact_frame):
    real_height = int(input("What is the height of your nose in cm's:"))
    nose = landmarks[0]
    wrist = landmarks[16]
    heel = landmarks[30]
    nose_height = frame.heel.y - frame.nose.y
    fake_contact_height = frame.heel.y - contact_frame.wrist.y
    real_contact_height = (real_height/nose_height)*fake_contact_height
    return real_contact_height


