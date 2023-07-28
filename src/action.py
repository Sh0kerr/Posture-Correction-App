import mediapipe as mp
import numpy as np
import cv2

from time import time
from threading import Thread
from playsound import playsound

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class Manage:
    def y_coords_difference(p1: list[float, float], p2: list[float, float]) -> float:
        y1 = p1[1]
        y2 = p2[1]

        return abs(y2 - y1)

    def calc_angle(p1: list[float, float], p2: list[float, float], p3: list[float, float]) -> float:
        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)

        radians = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
        angle = np.abs(radians * 180 / np.pi)

        return angle

    def calc_angle_posture(p1: list[float, float], p2: list[float, float], p3: list[float, float]) -> float:
        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)

        radians = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
        angle = np.abs(radians * 180 / np.pi)
        angle = 180 - angle % 180

        return angle

    def is_back_straight(p1: list[float, float], p2: list[float, float]) -> bool:
        x1 = p1[0]
        x2 = p2[0]

        return True if (abs(x2 - x1) < 0.05) else False


class Action:
    host = "127.0.0.1"
    port = 8888
    exitFlag = False
    reps = 0
    plank_time = 0

    def play_sound(self, way):
        playsound(way)

    def get_reps(self):
        return self.reps

    def pushups(self) -> None:
        _cap = cv2.VideoCapture(0)
        state = "up"
        with mp_pose.Pose(min_detection_confidence=0.757, min_tracking_confidence=0.5) as pose:
            while (_cap.isOpened()):
                if self.exitFlag:
                    _cap.release()
                    cv2.destroyAllWindows()
                    break
                ret, img = _cap.read()

                img = cv2.resize(img, (1280, 1024))

                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                results = pose.process(img)

                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark

                    l_shoulder_z = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z
                    r_shoulder_z = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z

                    # If camera's facing the right users' side
                    if r_shoulder_z < l_shoulder_z:
                        r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                        r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                        angle = Manage.calc_angle(r_shoulder, r_elbow, r_wrist)
                        shoulder_ankle_difference = Manage.y_coords_difference(r_shoulder, r_ankle)

                    else:
                        l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                        l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                        angle = Manage.calc_angle(l_shoulder, l_elbow, l_wrist)
                        shoulder_ankle_difference = Manage.y_coords_difference(l_shoulder, l_ankle)

                    # Angle logic
                    angle %= 180
                    if angle >= 75 and state == "up" and shoulder_ankle_difference < 0.5:
                        state = "down"
                        self.reps += 1
                        print("Ты сделал отжимание!!!")
                    elif angle < 20 and state == "down":
                        state = "up"

                except:
                    pass

                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                cv2.imshow("IP", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

    def squats(self) -> None:
        _cap = cv2.VideoCapture(0)
        state = "up"
        self.reps = 0
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while (_cap.isOpened()):
                if self.exitFlag:
                    _cap.release()
                    cv2.destroyAllWindows()
                    break

                ret, img = _cap.read()

                img = cv2.resize(img, (1280, 1024))

                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                results = pose.process(img)

                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark

                    l_knee_z = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].z
                    r_knee_z = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].z

                    # If camera's facing the right users' side
                    if r_knee_z < l_knee_z:
                        r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                        angle = Manage.calc_angle(r_hip, r_knee, r_ankle)

                    else:
                        l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                        angle = Manage.calc_angle(l_hip, l_knee, l_ankle)

                    if angle <= 90 and state == "up" and Manage.y_coords_difference(r_ankle, l_ankle) < 0.07:
                        state = "down"
                        self.reps += 1
                        print(f"squat {self.reps}")
                    elif angle > 190 and state == "down" and Manage.y_coords_difference(r_ankle, l_ankle) < 0.07:
                        state = "up"

                except:
                    pass

                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                cv2.imshow("IP", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

    def plank(self) -> None:
        _cap = cv2.VideoCapture(0)
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            start_time = 0
            timeStarted = False
            show_time = 0
            time_after_stop, time_when_time_stopped = 0, 0
            while (_cap.isOpened()):
                if self.exitFlag:
                    _cap.release()
                    cv2.destroyAllWindows()
                    break

                ret, img = _cap.read()

                img = cv2.resize(img, (1280, 1024))

                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                results = pose.process(img)

                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark

                    l_shoulder_z = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z
                    r_shoulder_z = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z

                    # If camera's facing the right users' side
                    if r_shoulder_z < l_shoulder_z:
                        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                        angle = Manage.calc_angle_posture(r_shoulder, r_hip, r_ankle)
                        shoulder_ankle_difference = Manage.y_coords_difference(r_shoulder, r_ankle)
                        shoulder_hip_difference = r_shoulder[1] - r_hip[1]

                    else:
                        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                        angle = Manage.calc_angle_posture(l_shoulder, l_hip, l_ankle)
                        shoulder_ankle_difference = Manage.y_coords_difference(l_shoulder, l_ankle)
                        shoulder_hip_difference = l_shoulder[1] - l_hip[1]

                    next_time = time()
                    if not (160 <= angle and shoulder_ankle_difference < 0.4):
                        if timeStarted:
                            if time_after_stop == 0:
                                time_when_time_stopped = time()
                                time_after_stop = 0.1
                            if next_time - time_when_time_stopped >= time_after_stop + 0.1:
                                time_after_stop = round(next_time - time_when_time_stopped, 1)
                            if time_after_stop >= 5:
                                time_after_stop = 0
                                if shoulder_hip_difference < 0:
                                    t = Thread(target=self.play_sound, args=("../sounds/rise_up_hip.mp3",))
                                    t.start()
                                    t.join()
                                else:
                                    t = Thread(target=self.play_sound, args=("../sounds/rise_down_hip.mp3",))
                                    t.start()
                                    t.join()
                    else:
                        if not timeStarted:
                            start_time = time()
                            timeStarted = True
                        time_after_stop = 0
                        if next_time - start_time >= show_time + 0.1:
                            show_time = round(next_time - start_time, 1)
                            self.reps = show_time

                except:
                    pass

                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                cv2.imshow("IP", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

    def posture(self) -> None:
        cap = cv2.VideoCapture(0)
        good_posture, good_knee = True, True
        bad_posture_time, bad_knee_time = 0, 0
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while(cap.isOpened()):
                if self.exitFlag:
                    cap.release()
                    cv2.destroyAllWindows()
                    break

                ret, img = cap.read()

                img = cv2.resize(img, (1280, 1024))

                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                results = pose.process(img)

                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark
                    l_shoulder_z = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z
                    r_shoulder_z = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z
                    if r_shoulder_z < l_shoulder_z:
                        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                        angle_24 = Manage.calc_angle_posture(r_shoulder, r_hip, r_knee)
                        if not(80 <= angle_24 <= 100):
                            if good_posture:
                                good_posture = False
                                bad_posture_time = time()
                            if time() - bad_posture_time >= 5:
                                t = Thread(target=self.play_sound, args=("../sounds/lean.mp3",))
                                t.start()
                                t.join()
                                good_posture = True
                        else:
                            good_posture = True

                        angle_26 = Manage.calc_angle_posture(r_hip, r_knee, r_ankle)
                        if not(80 <= angle_26 <= 100):
                            if good_knee:
                                good_knee = False
                                bad_knee_time = time()
                            if time() - bad_knee_time >= 5:
                                t = Thread(target=self.play_sound, args=("../sounds/knee_angle.mp3",))
                                t.start()
                                t.join()
                                good_knee = True
                        else:
                            good_knee = True

                    else:
                        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                        angle_23 = Manage.calc_angle_posture(l_shoulder, l_hip, l_knee)
                        if not (80 <= angle_23 <= 100):
                            if good_posture:
                                good_posture = False
                                bad_posture_time = time()
                            if time() - bad_posture_time >= 5:
                                t = Thread(target=self.play_sound, args=("../sounds/lean.mp3",))
                                t.start()
                                t.join()
                                good_posture = True
                        else:
                            good_posture = True

                        angle_25 = Manage.calc_angle_posture(l_hip, l_knee, l_ankle)
                        if not(80 <= angle_25 <= 100):
                            if good_knee:
                                good_knee = False
                                bad_knee_time = time()
                            if time() - bad_knee_time >= 5:
                                t = Thread(target=self.play_sound, args=("../sounds/knee_angle.mp3",))
                                t.start()
                                t.join()
                                good_knee = True
                        else:
                            good_knee = True

                except:
                    pass


                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

                cv2.imshow("IP", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
