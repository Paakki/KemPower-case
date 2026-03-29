# RoomLight – Domain Model

## 1. Key Concepts

### Hotel

Represents the whole environment where the system will be used. Contains all rooms and room groups.

### Room

A single physical space (hotel room, suite, restaurant area). Lighting can be controlled per room.

### Room Group

A collection of rooms (standard rooms, suites, restaurant). Used to apply configurations efficiently.

### Lighting Profile

A reusable lighting configuration that defines brightness, color and scene.

### Scene

Represents a predefined lighting mood (morning, evening, night). Part of a lighting profile.

### Schedule

Defines when a lighting profile is active (breakfast time, evening mode).

### Manager (User)

A hotel staff member who creates profiles and applies them to rooms or room groups.

### Guest

A person staying in a room. Can temporarily override lighting settings.

### Manual Override

A temporary change made by a guest to room lighting. Does not affect other rooms.

### Default Profile

The standard lighting configuration assigned to a room. Restored after guest checkout.

### Sync

The process of applying a lighting profile to multiple rooms or room groups.

### Log Entry

Represents a recorded change in the system (profile update, sync operation).

---

## 2. Relationships

- A **Hotel** contains multiple **Rooms**
- A **Hotel** contains multiple **Room Groups**
- A **Room Group** contains multiple **Rooms**
- A **Room** belongs to one **Room Group**
- A **Lighting Profile** can be applied to one or many **Rooms**
- A **Lighting Profile** can be applied to one or many **Room Groups**

- A **Schedule** activates a **Lighting Profile**
- A **Manager** creates **Lighting Profiles**
- A **Manager** applies **Lighting Profiles** to **Rooms / Room Groups**

- A **Guest** can create a **Manual Override**
- A **Manual Override** affects one **Room**
- A **Manual Override** is temporary

- A **Room** has a **Default Profile**
- After checkout the **Room** resets to **Default Profile**
- A **Sync** applies a **Lighting Profile** to multiple **Rooms**
- A **Log Entry** records changes (profile updates, syncs, resets)

---
