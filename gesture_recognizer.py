# EXample from: https://stackoverflow.com/questions/78503084/mediapipe-gesture-recognition-handedness-detects-both-hands-but-result-object-ha

import threading
from enum import Enum

import cv2
import mediapipe as mp
from mediapipe.tasks import python


class Prediction(Enum):
    CLOSED_FIST = "Closed_Fist"
    OPEN_PALM = "Open_Palm"
    POINTING_UP = "Pointing_Up"
    THUMB_DOWN = "Thumb_Down"
    THUMB_UP = "Thumb_Up"
    VICTORY = "Victory"
    I_LOVE_YOU = "ILoveYou"


class GestureRecognizer:
    def __init__(
        self,
        model_path: str = "gesture_recognizer.task",
        num_hands: int = 2,
        gesture_callback=None,
    ):
        """Initializes the gesture recognizer model

        Args:
            model_path: Path to the gesture recognition model
            num_hands: Maximum number of hands to detect
            gesture_callback: Optional callback function that receives (gesture_name: str, prediction: Prediction)
        """
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        self.lock = threading.Lock()
        self.current_gestures = []
        self.gesture_callback = gesture_callback
        self.num_hands = num_hands

        options = GestureRecognizerOptions(
            base_options=python.BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=num_hands,
            result_callback=self.__result_callback,
        )
        self.recognizer = GestureRecognizer.create_from_options(options)

    def record(self, visualize: bool = False, camera_index: int = -1):
        timestamp = 0
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=self.num_hands,
            min_detection_confidence=0.65,
            min_tracking_confidence=0.65,
        )

        cap = cv2.VideoCapture(camera_index)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                    self.recognizer.recognize_async(mp_image, timestamp)
                    timestamp = (
                        timestamp + 1
                    )  # should be monotonically increasing, because in LIVE_STREAM mode

                self.put_gestures(frame)

            if visualize:
                cv2.imshow("MediaPipe Hands", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        hands.close()

    def put_gestures(self, frame):
        """Puts the gestures on the frame."""
        with self.lock:
            gestures = self.current_gestures.copy()

        y_pos = 50
        for gesture_name in gestures:
            cv2.putText(
                frame,
                gesture_name,
                (10, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),  # Green color
                2,
                cv2.LINE_AA,
            )
            y_pos += 50

    def __result_callback(self, result, output_image, timestamp_ms):
        """Callback for processing the result."""
        with self.lock:
            self.current_gestures = []
            if result is not None and any(result.gestures):
                for single_hand_gesture_data in result.gestures:
                    gesture_name = single_hand_gesture_data[0].category_name
                    if gesture_name != "None":
                        pred = Prediction(gesture_name)
                        if self.gesture_callback:
                            self.gesture_callback(pred)
                        self.current_gestures.append(gesture_name)
