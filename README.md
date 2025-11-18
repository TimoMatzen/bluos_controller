# BluOS Controller

Repository for controlling BluOS Powernode.

## BluOS Controller

This repository contains a controller which connects to the BluOS Powernode on the local network.

API documentation for the Powernode: [docs](https://bluesound-deutschland.de/wp-content/uploads/2022/01/Custom-Integration-API-v1.0_March-2021.pdf)

## Controlling with Gestures

MediaPipe has been used to create a gesture recognizer which recognizes hands and gestures on 
video. A callable can be passed to pass these gestures to the BluOS device so the device can be controlled with gestures. 

Docs for MediaPipe: [docs](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python)

## WSL

When using WSL, the camera is not directly accessible and first needs to be shared from Windows and then linked in WSL. 

See: [Connect USB devices](https://learn.microsoft.com/en-us/windows/wsl/connect-usb#attach-a-usb-device)

