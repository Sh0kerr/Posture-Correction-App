import mediapipe as mp
import numpy as np
import cv2

from time import sleep, time
from playsound import playsound

_cap = cv2.VideoCapture(0)
user_type = {} # @TODO Определение типа пользователя, а также последующая рекомендация количества упражнений

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


class Training:
    def squats() -> None:
        state = "up"
        counter = 0
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while(_cap.isOpened()):
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
                        r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        
                        angle = Manage.calc_angle(r_hip, r_knee, r_ankle)
                    
                    else:
                        l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        
                        angle = Manage.calc_angle(l_hip, l_knee, l_ankle)

                    if angle <= 90 and state == "up" and Manage.y_coords_difference(r_ankle, l_ankle) < 0.07:
                        state = "down"
                        counter += 1
                    elif angle > 165 and state == "down" and Manage.y_coords_difference(r_ankle, l_ankle) < 0.07:
                        state = "up"

                    cv2.putText(img, str(counter) + ' ' + str(angle), [640, 512], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
                except:
                    pass


                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

                cv2.imshow("IP", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            _cap.release()
            cv2.destroyAllWindows()


    def pushups() -> None:
        state = "up"
        counter = 0
        with mp_pose.Pose(min_detection_confidence=0.757, min_tracking_confidence=0.5) as pose:
            while(_cap.isOpened()):
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
                        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                        r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        
                        angle = Manage.calc_angle(r_shoulder, r_elbow, r_wrist)
                        shoulder_ankle_difference = Manage.y_coords_difference(r_shoulder, r_ankle)

                    else:
                        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                        l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        
                        angle = Manage.calc_angle(l_shoulder, l_elbow, l_wrist)
                        shoulder_ankle_difference = Manage.y_coords_difference(l_shoulder, l_ankle)

                    # Angle logic
                    angle %= 180
                    if angle >= 90 and state == "up" and shoulder_ankle_difference < 0.5:
                        state = "down"
                        counter += 1
                    elif angle < 20 and state == "down":
                        state = "up"

                except:
                    pass


                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

                cv2.imshow("IP", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            _cap.release()
            cv2.destroyAllWindows()


    def plank() -> None:
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            start_time = 0
            timeStarted = False
            show_time = 0
            time_after_stop, time_when_time_stopped = 0, 0
            while(_cap.isOpened()):
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
                        r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        
                        angle = Manage.calc_angle(r_shoulder, r_hip, r_ankle)
                        shoulder_ankle_difference = Manage.y_coords_difference(r_shoulder, r_ankle)

                    else:
                        l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                        
                        angle = Manage.calc_angle(l_shoulder, l_hip, l_ankle)
                        shoulder_ankle_difference = Manage.y_coords_difference(l_shoulder, l_ankle)

                    next_time = time()
                    if not (170 <= angle <= 190 and shoulder_ankle_difference < 0.4):
                        if timeStarted:
                            if time_after_stop == 0:
                                time_when_time_stopped = time()
                                time_after_stop = 0.1
                            if next_time - time_when_time_stopped >= time_after_stop + 0.1:
                                time_after_stop = round(next_time - time_when_time_stopped, 1)
                                print("time_after_stop:", time_after_stop)
                                cv2.putText(img, str(angle), 
                                    tuple(np.multiply(r_hip, [1280, 1024]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                            if time_after_stop >= 5:
                                break
                            
                    else:
                        if not timeStarted:
                            start_time = time()
                            timeStarted = True
                        time_after_stop = 0
                        if next_time - start_time >= show_time + 0.1:
                            show_time = round(next_time - start_time, 1)
                            print(show_time)
                            cv2.putText(img, str(show_time), tuple(np.multiply(r_hip, [1280, 800]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                except:
                    pass


                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

                cv2.imshow("IP", img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            _cap.release()
            cv2.destroyAllWindows()
