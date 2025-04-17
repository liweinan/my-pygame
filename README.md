
![88001744893903_ pic](https://github.com/user-attachments/assets/d9c299e1-90aa-439d-abee-840c12288f4d)

# Isometric RPG Game

A simple isometric RPG game built with Pygame featuring smooth character movement and isometric rendering.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
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
- Built with Python 3.x and Pygame 2.5.2
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
