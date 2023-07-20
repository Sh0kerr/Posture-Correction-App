import mediapipe as mp
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
side: bool

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class Manage:
    def calc_angle(p1: list[float, float], p2: list[float, float], p3: list[float, float]) -> float:
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


def work() -> None:
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while(cap.isOpened()):
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
                    side = True
                else:
                    side = False

                if not side:
                    l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    angle_23 = Manage.calc_angle(l_shoulder, l_hip, l_knee)
                    if not(80 <= angle_23 <= 100):
                        cv2.putText(img, str(angle_23), 
                                tuple(np.multiply(l_hip, [1280, 1024]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
                    angle_25 = Manage.calc_angle(l_hip, l_knee, l_ankle)
                    if not(80 <= angle_25 <= 100):
                        cv2.putText(img, str(angle_25), 
                                    tuple(np.multiply(l_knee, [1280, 1024]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                        
                    line_11_23 = Manage.is_back_straight(l_shoulder, l_hip)
                    if not(line_11_23):
                        cv2.putText(img, "Left", 
                                tuple(np.multiply(l_shoulder, [1280, 1024]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                if side:
                    r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    
                    angle_24 = Manage.calc_angle(r_shoulder, r_hip, r_knee)
                    if not(80 <= angle_24 <= 100):
                        cv2.putText(img, str(angle_24), 
                                tuple(np.multiply(r_hip, [1280, 1024]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
                    angle_26 = Manage.calc_angle(r_hip, r_knee, r_ankle)
                    if not(80 <= angle_26 <= 100):
                        cv2.putText(img, str(angle_26), 
                                    tuple(np.multiply(r_knee, [1280, 1024]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    
                    line_12_24 = Manage.is_back_straight(r_shoulder, r_hip) 
                    if not (line_12_24):
                        cv2.putText(img, "Right", 
                                tuple(np.multiply(r_shoulder, [1280, 1024]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass


            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            cv2.imshow("IP", img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
