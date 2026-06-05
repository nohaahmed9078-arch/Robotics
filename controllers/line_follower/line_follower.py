"""from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# ================= MOTORS =================
lm = robot.getDevice('left wheel motor')
rm = robot.getDevice('right wheel motor')

lm.setPosition(float('inf'))
rm.setPosition(float('inf'))

# ================= GROUND SENSORS =================
# gs0 = left
# gs1 = center
# gs2 = right
gs = [robot.getDevice(f'gs{i}') for i in range(3)]

for s in gs:
    s.enable(timestep)

# ================= DISTANCE SENSORS =================
# ps0,ps1 = front-right
# ps6,ps7 = front-left
ps_names = ['ps0', 'ps1', 'ps6', 'ps7']

ps = [robot.getDevice(name) for name in ps_names]

for s in ps:
    s.enable(timestep)

# ================= PARAMETERS =================

# REAL VALUES FROM YOUR ENVIRONMENT:
# White ≈ 760
# Black ≈ 400
LINE_THRESHOLD = 580

OBSTACLE_THRESHOLD = 80

MAX_SPEED = 3.0
TURN_SPEED = 1.2
SEARCH_SPEED = 0.8

# ================= STATES =================
FOLLOW = 0
AVOID = 1
SEARCH = 2

state = FOLLOW

avoid_direction = 1
avoid_counter = 0

# ================= HELPER =================
def set_speed(left, right):

    left = max(-6.28, min(6.28, left))
    right = max(-6.28, min(6.28, right))

    lm.setVelocity(left)
    rm.setVelocity(right)

# ================= MAIN LOOP =================
while robot.step(timestep) != -1:

    # =====================================================
    # READ GROUND SENSORS
    # =====================================================
    g = [s.getValue() for s in gs]

    left_sensor = g[0]
    center_sensor = g[1]
    right_sensor = g[2]

    # BLACK = value lower than threshold
    on_left = left_sensor < LINE_THRESHOLD
    on_center = center_sensor < LINE_THRESHOLD
    on_right = right_sensor < LINE_THRESHOLD

    line_detected = on_left or on_center or on_right

    # =====================================================
    # READ DISTANCE SENSORS
    # =====================================================
    d = [s.getValue() for s in ps]

    front_right = d[0] > OBSTACLE_THRESHOLD or d[1] > OBSTACLE_THRESHOLD
    front_left = d[2] > OBSTACLE_THRESHOLD or d[3] > OBSTACLE_THRESHOLD

    obstacle_detected = front_right or front_left

    # =====================================================
    # DEBUG PRINTS
    # =====================================================
    print("=================================================")

    print("GROUND:", g)
    print("DISTANCE:", d)

    print(
        "LINE:",
        "L =", on_left,
        "C =", on_center,
        "R =", on_right
    )

    print("OBSTACLE:", obstacle_detected)

    if state == FOLLOW:
        print("STATE = FOLLOW")

    elif state == AVOID:
        print("STATE = AVOID")

    elif state == SEARCH:
        print("STATE = SEARCH")

    # =====================================================
    # FOLLOW LINE
    # =====================================================
    if state == FOLLOW:

        # ---------------- OBSTACLE DETECTED ----------------
        if obstacle_detected:

            print("Obstacle detected!")

            avoid_counter = 0

            # Choose direction away from obstacle
            if front_right:
                avoid_direction = 1
            else:
                avoid_direction = -1

            state = AVOID

        # ---------------- LINE FOLLOWING ----------------
        else:

            # CENTERED
            if on_center and not on_left and not on_right:

                print("Moving FORWARD")

                set_speed(MAX_SPEED, MAX_SPEED)

            # TURN LEFT
            elif on_left and not on_right:

                print("Turning LEFT")

                set_speed(TURN_SPEED, MAX_SPEED)

            # TURN RIGHT
            elif on_right and not on_left:

                print("Turning RIGHT")

                set_speed(MAX_SPEED, TURN_SPEED)

            # INTERSECTION
            elif on_left and on_center and on_right:

                print("Intersection detected")

                set_speed(MAX_SPEED, MAX_SPEED)

            # LINE LOST
            else:

                print("LINE LOST -> SEARCH")

                state = SEARCH

    # =====================================================
    # OBSTACLE AVOIDANCE
    # =====================================================
    elif state == AVOID:

        avoid_counter += 1

        print("Avoid Counter =", avoid_counter)

        # STEP 1: TURN AWAY
        if avoid_counter < 20:

            print("Rotating around obstacle")

            if avoid_direction == 1:
                # smooth left curve
                set_speed(1.0, MAX_SPEED)
            else:
                # smooth right curve
                set_speed(MAX_SPEED, 1.0)
 
        # STEP 2: MOVE FORWARD
        elif avoid_counter < 50:

            print("Passing obstacle")

            set_speed(MAX_SPEED, MAX_SPEED)

            # If line found again return immediately
            if line_detected:

                print("Line found after obstacle!")

                state = FOLLOW

        # STEP 3: SEARCH LINE
        else:

            print("Searching for line again")

            state = SEARCH

    # =====================================================
    # SEARCH FOR LINE
    # =====================================================
    elif state == SEARCH:

        # LINE FOUND
        if line_detected:

            print("LINE FOUND!")

            state = FOLLOW

        else:

            print("Searching slowly...")

            # IMPORTANT:
            # NO FAST SPINNING

            if avoid_direction == 1:
                set_speed(SEARCH_SPEED, MAX_SPEED)
            else:
                set_speed(MAX_SPEED, SEARCH_SPEED)
  """
from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# =====================================================
# MOTORS
# =====================================================
lm = robot.getDevice('left wheel motor')
rm = robot.getDevice('right wheel motor')

lm.setPosition(float('inf'))
rm.setPosition(float('inf'))

# =====================================================
# GROUND SENSORS
# =====================================================
# gs0 = left
# gs1 = center
# gs2 = right
gs = [robot.getDevice(f'gs{i}') for i in range(3)]

for s in gs:
    s.enable(timestep)

# =====================================================
# DISTANCE SENSORS
# =====================================================
# ps0,ps1 = front-right
# ps6,ps7 = front-left
ps_names = ['ps0', 'ps1', 'ps6', 'ps7']

ps = [robot.getDevice(name) for name in ps_names]

for s in ps:
    s.enable(timestep)

# =====================================================
# PARAMETERS
# =====================================================

LINE_THRESHOLD = 580
OBSTACLE_THRESHOLD = 150


MAX_SPEED = 5.0
TURN_SPEED = 2.5
SEARCH_SPEED = 1.5
# =====================================================
# STATES
# =====================================================

FOLLOW = 0
AVOID = 1
RETURN = 2
SEARCH = 3

state = FOLLOW

# obstacle side memory
avoid_direction = 1

# timers
avoid_counter = 0
return_counter = 0

# last line direction
last_direction = 1

# =====================================================
# HELPER
# =====================================================

def set_speed(left, right):

    left = max(-6.28, min(6.28, left))
    right = max(-6.28, min(6.28, right))

    lm.setVelocity(left)
    rm.setVelocity(right)

# =====================================================
# MAIN LOOP
# =====================================================

while robot.step(timestep) != -1:

    # =====================================================
    # READ GROUND SENSORS
    # =====================================================

    g = [s.getValue() for s in gs]

    left_sensor = g[0]
    center_sensor = g[1]
    right_sensor = g[2]

    on_left = left_sensor < LINE_THRESHOLD
    on_center = center_sensor < LINE_THRESHOLD
    on_right = right_sensor < LINE_THRESHOLD

    line_detected = on_left or on_center or on_right

    # remember line side
    if on_left:
        last_direction = -1

    elif on_right:
        last_direction = 1

    # =====================================================
    # READ DISTANCE SENSORS
    # =====================================================

    d = [s.getValue() for s in ps]

    front_right = d[0] > OBSTACLE_THRESHOLD or d[1] > OBSTACLE_THRESHOLD
    front_left = d[2] > OBSTACLE_THRESHOLD or d[3] > OBSTACLE_THRESHOLD

    obstacle_detected = front_right or front_left

    # =====================================================
    # DEBUGGING
    # =====================================================

    print("=================================================")

    print("GROUND:", g)
    print("DISTANCE:", d)

    print(
        "LINE:",
        "L =", on_left,
        "C =", on_center,
        "R =", on_right
    )

    print("OBSTACLE:", obstacle_detected)

    if state == FOLLOW:
        print("STATE = FOLLOW")

    elif state == AVOID:
        print("STATE = AVOID")

    elif state == RETURN:
        print("STATE = RETURN")

    elif state == SEARCH:
        print("STATE = SEARCH")

    # =====================================================
    # FOLLOW STATE
    # =====================================================

    if state == FOLLOW:

        # obstacle found
        if obstacle_detected:

            print("Obstacle detected!")

            avoid_counter = 0

            # choose opposite direction
            if front_right:
                avoid_direction = -1

            elif front_left:
                avoid_direction = 1

            state = AVOID

        else:

            # centered
            if on_center and not on_left and not on_right:

                print("FORWARD")

                set_speed(MAX_SPEED, MAX_SPEED)

            # left correction
            elif on_left and not on_right:

                print("LEFT")

                set_speed(1.0, MAX_SPEED)

            # right correction
            elif on_right and not on_left:

                print("RIGHT")

                set_speed(MAX_SPEED, 1.0)

            # intersection
            elif on_left and on_center and on_right:

                print("INTERSECTION")

                set_speed(MAX_SPEED, MAX_SPEED)

            # line lost
            else:

                print("LINE LOST")

                state = SEARCH

    # =====================================================
    # AVOID STATE
    # =====================================================

    elif state == AVOID:

        avoid_counter += 1

        print("Avoid Counter:", avoid_counter)

        # IMPORTANT:
        # always move FORWARD while turning
        # NEVER spin in place

        if avoid_direction == 1:

            # smooth RIGHT curve
            set_speed(MAX_SPEED, 1.0)

        else:

            # smooth LEFT curve
            set_speed(1.0, MAX_SPEED)

        # after enough movement
        # ignore sensors temporarily
        if avoid_counter > 25:

            print("Obstacle bypassed")

            return_counter = 0

            state = RETURN

    # =====================================================
    # RETURN TO LINE
    # =====================================================

    elif state == RETURN:

        return_counter += 1

        print("Returning to line...")

        # line found again
        if line_detected:

            print("LINE FOUND AGAIN!")

            state = FOLLOW

        else:

            # IMPORTANT:
            # controlled smooth arc
            # no spinning

            if avoid_direction == 1:

                # reconnect from RIGHT
                set_speed(1.0, MAX_SPEED)

            else:

                # reconnect from LEFT
                set_speed(MAX_SPEED, 1.0)

        # safety fallback
        if return_counter > 80:

            print("RETURN FAILED -> SEARCH")

            state = SEARCH

    # =====================================================
    # SEARCH STATE
    # =====================================================

    elif state == SEARCH:

        print("Searching...")

        # found line
        if line_detected:

            print("LINE RECOVERED")

            state = FOLLOW

        else:

            # IMPORTANT:
            # slow gentle search
            # NOT spinning

            if last_direction == -1:

                set_speed(0.5, SEARCH_SPEED)

            else:

                set_speed(SEARCH_SPEED, 0.5)