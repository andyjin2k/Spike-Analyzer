# Project: Volleyball Spike Analyzer

## ⚠️ WORKING AGREEMENT — READ FIRST, NON-NEGOTIABLE
I am building this to learn, not to ship fast. The volleyball-specific logic is MINE to write.
- DO NOT write metrics.py logic for me — not the volleyball math, none of it.
- Your job on metrics.py: explain concepts, point me to the right tools/methods/docs, debug
  code I wrote. Give me a CONCEPTUAL MAP — numbered steps + exact method/class names — NOT
  working code.
- EXCEPTION (decided after starting pose.py): pose.py is Claude's to implement directly.
  It's API plumbing against a documented MediaPipe interface (build detector, wrap frame,
  call detect_for_video, handle None) — not project-specific reasoning, so hand-typing it
  didn't teach transferable skills. Claude writes it, then explains it function-by-function
  so I can still defend/explain the code later even though I didn't type it.
- Boilerplate is also exempt (e.g. a standard video-read loop, like video.py). If unsure
  whether something is boilerplate/plumbing vs load-bearing volleyball logic, ASK before writing.
- metrics.py HYBRID SPLIT (decided when starting metrics.py): Claude writes the data-wiring
  boilerplate only — `collect_frame_data()`, which loops frames, calls pose.py, and
  assembles a plain list of per-frame dicts. It does NOT interpret the data (no
  wrist-picking, no thresholds, no volleyball logic). I design and write every
  decision/scoring function myself (find_contact_frame, compute_contact_height, etc.) —
  this is NOT an opening to hand off more of metrics.py the way pose.py got handed off;
  the logic functions stay mine, full stop.
- If I'm stuck on metrics.py, lead me to the answer with questions and pointers. Don't hand me the solution.
- If the metrics.py task requires little to no logic then implement it yourself
- If i directly tell you to code in metrics.py, push back once, but if I still insist then do as I say.

## What this is
A computer-vision tool: phone video of a volleyball spike in → measured technique numbers out
(contact height, arm-swing timing, approach tempo). NOT a chatbot/LLM wrapper. A real CV pipeline.
I play volleyball — I know what's worth measuring. Target: a technically deep project for college apps.

PIVOTED from a serve analyzer (do not relitigate, decided and reasoned through):
serves vary too much in mechanics (float, topspin, standing, jump serve) for a metric like
contact height to mean the same thing across them. A spike's swing is structurally the same
move for everyone, so the same metrics are actually comparable across attempts.

v1 = SELF-TOSS spike only: one person tosses the ball to themselves, approaches/jumps, hits it.
One body in frame the whole time → num_poses=1 stays correct as-is, no pose.py changes needed.
Real-set spikes (a setter delivers the ball, multiple people in frame, need to identify which
detected pose is the hitter) is a later version, not v1 — flagged here so it isn't forgotten,
not because it needs solving now.

## Architecture (settled — three layers, one job each)
- video.py  → OpenCV ("the hands"): opens the .mp4, pulls frames one by one, BGR→RGB,
              draws overlays, writes output video. Knows NOTHING about MediaPipe.  ✅ DONE
- pose.py   → MediaPipe ("the eyes"): one RGB frame + timestamp in → 33 body landmarks out.
              Knows NOTHING about volleyball.  ⬅️ Claude-implemented (see working agreement above).
- metrics.py → my code ("the brain"): turns landmarks into volleyball meaning. The
              decision/scoring logic is mine to write; Claude wrote only the data-wiring
              loop (`collect_frame_data`) that feeds it.  ⬅️ IN PROGRESS

## Key decision already made (do not relitigate)
Using MediaPipe's **Tasks API** (`PoseLandmarker`), NOT the legacy `mp.solutions.pose`.
Running mode = VIDEO (model tracks the body frame-to-frame instead of re-detecting each time).
NOTE: "VIDEO mode" does NOT mean MediaPipe reads the video file — OpenCV still decodes frames
and feeds them in one at a time. MediaPipe only ever sees one already-decoded frame per call.
Most online tutorials show the LEGACY api (.process(), raw numpy, no .task file) — ignore those.

## Environment (already set up)
macOS, M3 Pro. Python 3.12 venv, VS Code w/ venv interpreter selected.
git + GitHub (gh CLI). Installed: mediapipe, opencv-python, pandas, matplotlib.
Folder: spike-analyzer/ with data/raw/ and data/outputs/. Structure kept minimal on purpose —
only split into src/ when a file starts to hurt.

## My immediate task: write find_contact_frame() and compute_contact_height()
pose.py is done (Claude-implemented, understood and verified). Claude also wrote
`collect_frame_data()` in metrics.py — pure wiring, loops the video and calls pose.py,
returns `list[dict]` with keys `frame_index`, `timestamp_ms`, `landmarks`,
`world_landmarks` (the latter two are `None` on frames with no detected pose). My job
now: write the actual logic functions described in Milestone 1 below, consuming that
list myself.

Conceptual map pose.py was built from (for reference, already implemented):
1. Download the pose model .task file (full variant), keep in models/.
2. Build the detector ONCE outside the loop: BaseOptions(model path) → PoseLandmarkerOptions
   (mode=VIDEO, num_poses=1) → PoseLandmarker.create_from_options.
3. Per frame: wrap the RGB array in mp.Image (ImageFormat.SRGB).
4. Compute timestamp in integer ms from frame_index × (1000/fps) — NOT CAP_PROP_POS_MSEC
   (flaky on phone video; must be strictly increasing or VIDEO mode errors).
5. Call detect_for_video(image, timestamp_ms). Read PoseLandmarkerResult.
6. Handle the empty case (some frames return no pose) — return None so metrics.py can skip.

Output structure I need to keep straight:
- pose_landmarks       → normalized image coords, x/y in [0,1]. (Use for "which frame is highest".)
- pose_world_landmarks → meters, origin at hips. (Use for body-relative heights.)
- each landmark has visibility/presence scores → filter out low-confidence joints.
- 33 landmarks, indexed via the PoseLandmark enum (e.g. right/left wrist).

## After pose.py works — Milestone 1 payoff (also mine to write)
Find the contact frame = frame where the hitting wrist's image-y is SMALLEST during the spike
swing (y grows downward, so smallest y = highest reach). Gate on wrist visibility first so a
bad detection can't win. Then turn it into my first real number: contact height relative to a
body landmark (quick version in normalized coords, honest version in world/meters).
Known limitation to keep as a code comment: "highest wrist" is a PROXY for contact — exact contact
needs ball detection, which is v2. That limitation is the motivation for v2, not a flaw to hide.
v1 scope is just contact height. Approach tempo (tracking footwork/steps across frames) is a
real metric on the roadmap but is meaningfully harder (multi-frame tracking, not a single
extremum) — v2+, not now.

## My background (calibrate explanations to this)
Did Karpathy's micrograd, have PyTorch basics. Comfortable with Python fundamentals.
Newish to structuring a real project and to git. Learn best by writing it myself with guided
explanation. I respond well to direct pushback. I dislike passive consumption / inauthentic work.