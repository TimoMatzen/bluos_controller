from functools import partial

from bluos_controller import BluOSClient
from gesture_recognizer import GestureRecognizer, Prediction


def gesture_callback(bluos_client: BluOSClient, prediction: Prediction):
    """Gesture callback.

    When a gesture is recognized the bluos_client is used to make a call to the client.

    Currently implemented:
      - Play on open palm gesture
      - Pause on closed fist gesture
    """
    if prediction == Prediction.OPEN_PALM:
        bluos_client.play()
    if prediction == Prediction.CLOSED_FIST:
        bluos_client.pause()


if __name__ == "__main__":
    with BluOSClient("192.168.2.9") as client:
        GestureRecognizer(
            "gesture_recognizer.task",
            gesture_callback=partial(gesture_callback, client),
        )
