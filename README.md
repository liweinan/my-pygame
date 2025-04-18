![88001744893903_ pic](https://github.com/user-attachments/assets/d9c299e1-90aa-439d-abee-840c12288f4d)

---

![image](https://github.com/user-attachments/assets/6c6c6eee-3da6-4bfd-8625-e556ad17fac7)

---

![image](https://github.com/user-attachments/assets/a154d6c5-2dd7-4a12-8920-aa12a756a242)

---

# Isometric RPG Game

A simple isometric RPG game built with Pygame featuring smooth character movement and isometric rendering.

## Prerequisites

- Python 3.11 (required for compatibility with Pygame 2.5.2)
- SDL2 and related libraries (for macOS users)

## Setup

1. Install uv if you haven't already:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. For macOS users, install SDL2 and related libraries:
```bash
brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_ttf pkg-config
```

3. Create a virtual environment and install dependencies:
```bash
# For bash/zsh users
uv venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt

# For fish shell users
uv venv --python 3.11
source .venv/bin/activate.fish
uv pip install -r requirements.txt
```

4. Run the game:
```bash
python main.py
```

## Controls
- W/Up Arrow: Move character up
- S/Down Arrow: Move character down
- A/Left Arrow: Move character left
- D/Right Arrow: Move character right
- ESC: Quit the game

## Features
- Isometric tile-based rendering
- Smooth character movement with 8-directional controls
- Character direction facing (up, down, left, right)
- Frame-rate independent movement
- Basic character animation system
- Simple camera system
- Diagonal movement normalization for consistent speed

## Technical Details
- Built with Python 3.11 and Pygame 2.5.2
- Uses isometric projection for 2.5D rendering
- Implements delta-time based movement for smooth gameplay
- Character movement system with proper direction tracking
- Basic animation state management

## Future Enhancements
- Sprite-based character animation
- Character stats and inventory system
- Object interaction system
- Character customization
- Advanced movement patterns (running, jumping)
- NPCs and enemies
- Quest system
- Save/Load functionality 
