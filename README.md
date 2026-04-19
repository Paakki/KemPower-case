Juha-Matti Paakki

# RoomLight

Homework at /docs
App at /src

Video of running the App: [RoomLight](https://youtu.be/msh1IddQNnQ)
Plain Text Link: https://youtu.be/msh1IddQNnQ

## How to run:

- Python 3 installed
- Terminal

Navigate to the src folder

Initialize demo data:
python roomlight.py init

List data:
python roomlight.py list-rooms
python roomlight.py list-groups
python roomlight.py list-profiles

Create a lighting profile
python roomlight.py create-profile <name> <brightness> <color> <scene>
Example:
python roomlight.py create-profile relax 40 warm_white relax

Apply profile to a single room:
python roomlight.py apply-profile-room <profile_name> <room_id>

Apply profile to a group:
python roomlight.py apply-profile-group <profile_name> <group_name>
Example:
python roomlight.py apply-profile-group relax standard

Guest override:
python roomlight.py guest-override <room_id> <brightness> <color> <scene>

Checkout:
python roomlight.py checkout <room_id>

View logs:
python roomlight.py logs
