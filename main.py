import argparse
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
    parser = argparse.ArgumentParser(
        prog="BluosController", description="Controls the bluos device via the api."
    )
    parser.add_argument("-pi", "--raspberry", action="store_true")
    parser.add_argument("-v", "--visualize", action="store_true")
    args = parser.parse_args()
    with BluOSClient("192.168.2.9") as client:
        recognizer = GestureRecognizer(
            "gesture_recognizer.task",
            gesture_callback=partial(gesture_callback, client),
        )
        recognizer.record(visualize=args.visualize, pi=args.raspberry)
