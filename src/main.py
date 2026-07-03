
import metrics
import sample
video_path = "data/raw/spike.mp4"
def find_contact_angle(video_path):
    frame_data = metrics.collect_frame_data(video_path)
    contact_frame = metrics.find_contact_frame(frame_data)
    contact_angle =  metrics.find_contact_angle(contact_frame)
    return contact_angle

def find_contact_height(is_standing_straight, video_path):
    frame_data = metrics.collect_frame_data(video_path)
    frame = metrics.find_straight_frame(is_standing_straight, frame_data)
    contact_frame = metrics.find_contact_frame(frame_data)
    height = metrics.contact_height(frame, contact_frame)
    return height


print(find_contact_angle(video_path))
print(find_contact_height(sample.is_standing_straight, video_path))