import cv2

# --- config: where to read from and write to ---
INPUT_PATH  = "data/raw/spike.mp4"
OUTPUT_PATH = "data/outputs/spike_annotated.mp4"

# JOB 1 (setup): open the video file
cap = cv2.VideoCapture(INPUT_PATH)
if not cap.isOpened():                     # fail loudly if the path is wrong
    raise FileNotFoundError(f"Could not open {INPUT_PATH}")

# read the video's properties — we need these to write a matching output
fps    = cap.get(cv2.CAP_PROP_FPS) or 30   # some files report 0; fall back to 30
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# JOB 4 (setup): prepare a writer with the same size and fps as the input
fourcc = cv2.VideoWriter_fourcc(*"mp4v")   # the .mp4 codec
writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

frame_count = 0
while True:
    # JOB 1: grab the next frame. `ok` is False when the video runs out.
    ok, frame = cap.read()
    if not ok:
        break

    # JOB 2: convert BGR (OpenCV's order) -> RGB (what a pose model wants).
    # Nothing reads `rgb` yet — this just shows the conversion step.
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # JOB 3: draw on the frame to prove drawing works.
    # (Placeholder — the real skeleton gets drawn once we have pose data.)
    cv2.putText(frame, f"frame {frame_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)  # green text

    # JOB 4: write the annotated frame into the output video
    writer.write(frame)
    frame_count += 1

# always release resources when done
cap.release()
writer.release()
print(f"done: processed {frame_count} frames -> {OUTPUT_PATH}")