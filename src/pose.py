from pathlib import Path

import mediapipe as mp

# Resolved relative to this file, not the caller's cwd, so it works regardless of
# whether the caller is run from the repo root, src/, or a notebook.
MODEL_PATH = str(Path(__file__).resolve().parent.parent / "models" / "pose_landmarker_full.task")


def build_landmarker(model_path: str = MODEL_PATH) -> mp.tasks.vision.PoseLandmarker:
    base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
    options = mp.tasks.vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_poses=1,
    )
    return mp.tasks.vision.PoseLandmarker.create_from_options(options)


def detect_pose(landmarker, rgb_frame, frame_index, fps):
    # VIDEO mode needs a strictly increasing timestamp per frame; CAP_PROP_POS_MSEC is
    # flaky on phone footage, so we derive it from frame index instead.
    timestamp_ms = int(frame_index * (1000 / fps))
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    if not result.pose_landmarks:
        return None

    return {
        "landmarks": result.pose_landmarks[0],         # normalized x/y in [0,1], per-joint visibility/presence
        "world_landmarks": result.pose_world_landmarks[0],  # meters, origin at hips
    }
