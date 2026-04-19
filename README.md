Juha-Matti Paakki

# RoomLight

Homework at /docs
App at /src

Video of running the App: [RoomLight](https://youtu.be/msh1IddQNnQ)
Plain Text Link: https://youtu.be/msh1IddQNnQ

---

## Requirements:

- Python 3 installed
- Terminal

---

## How to run:

Navigate to the src folder ->

Initialize demo data:

```bash
python roomlight.py init
```

List data:

```bash
python roomlight.py list-rooms

python roomlight.py list-groups

python roomlight.py list-profiles
```

Create a lighting profile

```bash
python roomlight.py create-profile <name> <brightness> <color> <scene>
```

Example:

```bash
python roomlight.py create-profile relax 40 warm_white relax
```

Apply profile to a single room:

```bash
python roomlight.py apply-profile-room <profile_name> <room_id>
```

Apply profile to a group:

```bash
python roomlight.py apply-profile-group <profile_name> <group_name>
```

Example:

```bash
python roomlight.py apply-profile-group relax standard
```

Guest override:

```bash
python roomlight.py guest-override <room_id> <brightness> <color> <scene>
```

Checkout:

```bash
python roomlight.py checkout <room_id>
```

View logs:

```bash
python roomlight.py logs
```
