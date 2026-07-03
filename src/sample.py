import math

def calculate_angle(a, b, c):
    """Angle at vertex b, formed by rays b→a and b→c."""
    ang = math.degrees(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
    return abs(ang + 360) % 360

def is_standing_straight(frame):
    if frame["landmarks"] is None:
        return False

    landmarks = frame["landmarks"]
    hip      = landmarks[23]
    knee     = landmarks[25]
    ankle    = landmarks[27]
    shoulder = landmarks[11]

    leg_angle   = calculate_angle(hip, knee, ankle)
    torso_angle = calculate_angle(shoulder, hip, knee)

    return (165 <= leg_angle <= 180) and (80 <= torso_angle <= 100)
