#!/usr/bin/env python3

# RoomLight Prototype CLI
# A simple hotel lighting prototype.
# The goal is to prove: "Configure once, sync everywhere."

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional


DATA_FILE = "roomlight_data.json"


# -- Domain model entities --

@dataclass
class LightingProfile:
    name: str
    brightness: int
    color: str
    scene: str


@dataclass
class Room:
    room_id: str
    room_type: str
    group_name: str
    default_profile_name: Optional[str] = None
    active_profile_name: Optional[str] = None
    manual_override_active: bool = False


@dataclass
class RoomGroup:
    name: str
    room_ids: List[str] = field(default_factory=list)


@dataclass
class LogEntry:
    message: str


@dataclass
class Hotel:
    rooms: List[Room] = field(default_factory=list)
    room_groups: List[RoomGroup] = field(default_factory=list)
    lighting_profiles: List[LightingProfile] = field(default_factory=list)
    log_entries: List[LogEntry] = field(default_factory=list)


# -- Data storage helpers --

def create_default_hotel() -> Hotel:
    hotel = Hotel()

    hotel.rooms = [
        Room("101", "standard", "standard"),
        Room("102", "standard", "standard"),
        Room("201", "suite", "suites"),
        Room("202", "suite", "suites"),
        Room("301", "restaurant", "restaurant"),
    ]

    hotel.room_groups = [
        RoomGroup("standard", ["101", "102"]),
        RoomGroup("suites", ["201", "202"]),
        RoomGroup("restaurant", ["301"]),
    ]

    hotel.lighting_profiles = [
        LightingProfile("morning", 80, "warm white", "morning"),
        LightingProfile("evening", 50, "soft yellow", "evening"),
        LightingProfile("night", 20, "dim amber", "night"),
    ]

    hotel.log_entries.append(LogEntry("System initialized with demo hotel data."))
    return hotel


def hotel_to_dict(hotel: Hotel) -> dict:
    return {
        "rooms": [asdict(room) for room in hotel.rooms],
        "room_groups": [asdict(group) for group in hotel.room_groups],
        "lighting_profiles": [asdict(profile) for profile in hotel.lighting_profiles],
        "log_entries": [asdict(entry) for entry in hotel.log_entries],
    }


def hotel_from_dict(data: dict) -> Hotel:
    hotel = Hotel()

    hotel.rooms = [Room(**room_data) for room_data in data.get("rooms", [])]
    hotel.room_groups = [RoomGroup(**group_data) for group_data in data.get("room_groups", [])]
    hotel.lighting_profiles = [
        LightingProfile(**profile_data) for profile_data in data.get("lighting_profiles", [])
    ]
    hotel.log_entries = [LogEntry(**entry_data) for entry_data in data.get("log_entries", [])]

    return hotel


def load_hotel() -> Hotel:
    if not os.path.exists(DATA_FILE):
        hotel = create_default_hotel()
        save_hotel(hotel)
        return hotel

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return hotel_from_dict(data)


def save_hotel(hotel: Hotel):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(hotel_to_dict(hotel), file, indent=2)


# -- Find helpers --

def find_profile_by_name(hotel: Hotel, profile_name: str) -> Optional[LightingProfile]:
    return next((profile for profile in hotel.lighting_profiles if profile.name == profile_name), None)


def find_group_by_name(hotel: Hotel, group_name: str) -> Optional[RoomGroup]:
    return next((group for group in hotel.room_groups if group.name == group_name), None)


def find_room_by_id(hotel: Hotel, room_id: str) -> Optional[Room]:
    return next((room for room in hotel.rooms if room.room_id == room_id), None)


# -- Domain logic helpers --

def add_log_entry(hotel: Hotel, message: str):
    hotel.log_entries.append(LogEntry(message))


def create_profile(hotel: Hotel, profile_name: str, brightness: int, color: str, scene: str):
    existing_profile = find_profile_by_name(hotel, profile_name)
    if existing_profile is not None:
        print(f"Profile '{profile_name}' already exists.")
        return

    if brightness < 0 or brightness > 100:
        print("Brightness must be between 0 and 100.")
        return

    profile = LightingProfile(profile_name, brightness, color, scene)
    hotel.lighting_profiles.append(profile)

    # REQ-09: System logs changes made to lighting profiles.
    add_log_entry(hotel, f"Profile '{profile_name}' created.")
    save_hotel(hotel)

    # REQ-001: System allows creation of lighting profiles.
    print(f"Profile '{profile_name}' created successfully.")


def list_profiles(hotel: Hotel):
    if len(hotel.lighting_profiles) == 0:
        print("No lighting profiles found.")
        return

    print("Lighting profiles:")
    for profile in hotel.lighting_profiles:
        print(
            f"- {profile.name}: brightness={profile.brightness}, "
            f"color={profile.color}, scene={profile.scene}"
        )


def list_rooms(hotel: Hotel):
    print("Rooms:")
    for room in hotel.rooms:
        print(
            f"- Room {room.room_id} | type={room.room_type} | group={room.group_name} | "
            f"active_profile={room.active_profile_name} | override={room.manual_override_active}"
        )


def list_groups(hotel: Hotel):
    print("Room groups:")
    for group in hotel.room_groups:
        print(f"- {group.name}: rooms={', '.join(group.room_ids)}")


def apply_profile_to_room(hotel: Hotel, profile_name: str, room_id: str):
    profile = find_profile_by_name(hotel, profile_name)
    room = find_room_by_id(hotel, room_id)

    if profile is None:
        print(f"Profile '{profile_name}' not found.")
        return

    if room is None:
        print(f"Room '{room_id}' not found.")
        return

    room.active_profile_name = profile.name
    if room.default_profile_name is None:
        room.default_profile_name = profile.name
    room.manual_override_active = False

    add_log_entry(hotel, f"Profile '{profile_name}' applied to room {room_id}.")
    save_hotel(hotel)

    print(f"Profile '{profile_name}' applied to room {room_id}.")


def apply_profile_to_group(hotel: Hotel, profile_name: str, group_name: str):
    profile = find_profile_by_name(hotel, profile_name)
    group = find_group_by_name(hotel, group_name)

    if profile is None:
        print(f"Profile '{profile_name}' not found.")
        return

    if group is None:
        print(f"Group '{group_name}' not found.")
        return

    # REQ-002 + REQ-005: One profile can be applied and synced to multiple rooms.
    for room_id in group.room_ids:
        room = find_room_by_id(hotel, room_id)
        if room is not None:
            room.active_profile_name = profile.name
            if room.default_profile_name is None:
                room.default_profile_name = profile.name
            room.manual_override_active = False

    add_log_entry(hotel, f"Profile '{profile_name}' synced to group '{group_name}'.")
    save_hotel(hotel)

    print(f"Profile '{profile_name}' synced to group '{group_name}'.")


def guest_override_room(hotel: Hotel, room_id: str, brightness: int, color: str, scene: str):
    room = find_room_by_id(hotel, room_id)

    if room is None:
        print(f"Room '{room_id}' not found.")
        return

    if brightness < 0 or brightness > 100:
        print("Brightness must be between 0 and 100.")
        return

    # REQ-006: Guest can manually adjust room lighting setup.
    override_profile_name = f"override-{room_id}"
    room.active_profile_name = override_profile_name
    room.manual_override_active = True

    add_log_entry(
        hotel,
        f"Guest override set for room {room_id}: brightness={brightness}, color={color}, scene={scene}."
    )
    save_hotel(hotel)

    print(f"Guest override applied to room {room_id}.")


def checkout_room(hotel: Hotel, room_id: str):
    room = find_room_by_id(hotel, room_id)

    if room is None:
        print(f"Room '{room_id}' not found.")
        return

    # REQ-007: Lighting resets automatically to default profile after guest checkout.
    room.active_profile_name = room.default_profile_name
    room.manual_override_active = False

    add_log_entry(hotel, f"Room {room_id} reset to default profile after checkout.")
    save_hotel(hotel)

    print(f"Room {room_id} reset to default profile.")


def show_logs(hotel: Hotel):
    if len(hotel.log_entries) == 0:
        print("No log entries found.")
        return

    print("Log entries:")
    for entry in hotel.log_entries:
        print(f"- {entry.message}")


# -- CLI helpers --

def print_usage():
    print("RoomLight Prototype CLI")
    print("")
    print("Usage:")
    print("  python roomlight.py init")
    print("  python roomlight.py list-rooms")
    print("  python roomlight.py list-groups")
    print("  python roomlight.py list-profiles")
    print("  python roomlight.py create-profile <name> <brightness> <color> <scene>")
    print("  python roomlight.py apply-profile-room <profile_name> <room_id>")
    print("  python roomlight.py apply-profile-group <profile_name> <group_name>")
    print("  python roomlight.py guest-override <room_id> <brightness> <color> <scene>")
    print("  python roomlight.py checkout <room_id>")
    print("  python roomlight.py logs")
    print("")
    print("Examples:")
    print("  python roomlight.py create-profile relax 40 warm_white relax")
    print("  python roomlight.py apply-profile-group relax standard")
    print("  python roomlight.py guest-override 101 25 blue night")
    print("  python roomlight.py checkout 101")


def main(args):
    if len(args) == 0:
        print_usage()
        return

    command = args[0]

    if command == "init":
        hotel = create_default_hotel()
        save_hotel(hotel)
        print("RoomLight demo data initialized.")
        return

    hotel = load_hotel()

    if command == "list-rooms":
        list_rooms(hotel)
    elif command == "list-groups":
        list_groups(hotel)
    elif command == "list-profiles":
        list_profiles(hotel)
    elif command == "create-profile":
        if len(args) != 5:
            print("Usage: python roomlight.py create-profile <name> <brightness> <color> <scene>")
            return
        profile_name = args[1]
        try:
            brightness = int(args[2])
        except ValueError:
            print("Brightness must be an integer.")
            return
        color = args[3]
        scene = args[4]
        create_profile(hotel, profile_name, brightness, color, scene)
    elif command == "apply-profile-room":
        if len(args) != 3:
            print("Usage: python roomlight.py apply-profile-room <profile_name> <room_id>")
            return
        apply_profile_to_room(hotel, args[1], args[2])
    elif command == "apply-profile-group":
        if len(args) != 3:
            print("Usage: python roomlight.py apply-profile-group <profile_name> <group_name>")
            return
        apply_profile_to_group(hotel, args[1], args[2])
    elif command == "guest-override":
        if len(args) != 5:
            print("Usage: python roomlight.py guest-override <room_id> <brightness> <color> <scene>")
            return
        room_id = args[1]
        try:
            brightness = int(args[2])
        except ValueError:
            print("Brightness must be an integer.")
            return
        color = args[3]
        scene = args[4]
        guest_override_room(hotel, room_id, brightness, color, scene)
    elif command == "checkout":
        if len(args) != 2:
            print("Usage: python roomlight.py checkout <room_id>")
            return
        checkout_room(hotel, args[1])
    elif command == "logs":
        show_logs(hotel)
    else:
        print(f"Unknown command: {command}")
        print("")
        print_usage()


if __name__ == "__main__":
    main(sys.argv[1:])