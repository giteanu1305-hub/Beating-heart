import random
import tkinter as tk
from math import sin, cos, pi, log

# Window Canvas Dimensions
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 550
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 12

# =========================================================================
# 🛠️ CUSTOMIZE YOUR PROGRAM HERE:
# =========================================================================
# 1. Subtle, elegant shade of crimson red for the heart particles
HEART_COLOR = "#A21111" 

# 2. Type your custom messages here! Wrap each message in quotation marks.
TEXT_POOL = [
    "I Love You", 
    "Forever 💖"
]
# =========================================================================

# Interactive State Arrays
mouse_trail = []
click_bursts = []
floating_texts = []  

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """Mathematical formula for the core heart shape layout"""
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    x *= shrink_ratio
    y *= shrink_ratio
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """Fills the interior with scattered inner particles"""
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def shrink(x, y, ratio):
    """Calculates contraction forces for organic beating"""
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * sin(force) * (x - CANVAS_CENTER_X)
    dy = ratio * sin(force) * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):
    """Smooth transition timing function for the heartbeat rhythm"""
    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()  
        self._edge_diffusion_points = set()  
        self._center_diffusion_points = set()  
        self.all_pframe = {}  
        self.build(2000)

        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))

        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    def calc_position(self, x, y, ratio, frame):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, frame):
        ratio = 10 * curve(frame / 10 * pi)  
        halo_radius = int(4 + 6 * (1 + curve(frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(frame / 10 * pi) ** 2))

        all_rect = []

        # 1. Background halo glow
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=12.5)
            x, y = shrink(x, y, ratio)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-halo_radius, halo_radius)
                y += random.randint(-halo_radius, halo_radius)
                size = random.choice([1, 2])  # FIXED: Added particle choices
                all_rect.append((x, y, size))

        # 2. Main outline core particles
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio, frame)
            size = random.choice([1, 2, 3])  # FIXED: Added particle choices
            all_rect.append((x, y, size))

        # 3. Outer structural scatter
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio, frame)
            size = random.choice([1, 2])  # FIXED: Added particle choices
            all_rect.append((x, y, size))

        # 4. Interior structural filler
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio, frame)
            size = random.choice([1, 2])  # FIXED: Added particle choices
            all_rect.append((x, y, size))

        self.all_pframe[frame] = all_rect

    def render(self, canvas, render_frame):
        # Draw main core breathing heart using your subtle red
        for x, y, size in self.all_pframe[render_frame % self.generate_frame]:
            canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def handle_mouse_move(event):
    """Tracks mouse movement to spawn trailing subtle dust particles"""
    global mouse_trail
    mouse_trail.append({"x": event.x, "y": event.y, "life": 15, "size": random.randint(2, 4)})


def handle_mouse_click(event):
    """Spawns interactive explosion particles AND a floating text block on click"""
    global click_bursts, floating_texts
    
    # 1. Spawn a random phrase from your customized text inputs pool
    chosen_text = random.choice(TEXT_POOL)
    floating_texts.append({
        "x": event.x,
        "y": event.y,
        "text": chosen_text,
        "life": 45,  
        "size": random.randint(13, 16)
    })
    
    # 2. Keep the explosion particle wave active
    for _ in range(25):
        angle = random.uniform(0, 2 * pi)
        speed = random.uniform(2, 5)
        click_bursts.append({
            "x": event.x, 
            "y": event.y, 
            "vx": speed * sin(angle), 
            "vy": speed * cos(angle), 
            "life": 20,
            "size": random.randint(2, 4)
        })


def draw(main_window, canvas, heart, frame=0):
    global mouse_trail, click_bursts, floating_texts
    canvas.delete("all")
    
    # 1. Render the main subtle red heart
    heart.render(canvas, frame)
    
    # 2. Update and render interactive Mouse Trailing Dust using the subtle red
    active_trail = []
    for p in mouse_trail:
        p["life"] -= 1
        if p["life"] > 0:
            canvas.create_rectangle(p["x"], p["y"], p["x"] + p["size"], p["y"] + p["size"], width=0, fill=HEART_COLOR)
            p["y"] -= 0.5 
            active_trail.append(p)
    mouse_trail = active_trail

    # 3. Update and render interactive Click Explosion Bursts
    active_bursts = []
    for p in click_bursts:
        p["life"] -= 1
        if p["life"] > 0:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] *= 0.95
            p["vy"] *= 0.95
            p["vy"] += 0.08 
            canvas.create_rectangle(p["x"], p["y"], p["x"] + p["size"], p["y"] + p["size"], width=0, fill=HEART_COLOR)
            active_bursts.append(p)
    click_bursts = active_bursts

    # 4. Render the interactive Floating Inputs Text
    active_texts = []
    text_color = "#FFE4E1" 
    for t in floating_texts:
        t["life"] -= 1
        if t["life"] > 0:
            font_style = f"Courier {t['size']} bold"
            canvas.create_text(t["x"], t["y"], text=t["text"], fill=text_color, font=font_style)
            t["y"] -= 1.0  
            active_texts.append(t)
    floating_texts = active_texts

    # Keep loop running smoothly
    main_window.after(16, draw, main_window, canvas, heart, frame + 1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interactive Custom Heart")
    
    cvs = tk.Canvas(root, bg="black", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    cvs.pack()
    
    # Bind interactive mouse trigger events
    cvs.bind("<Motion>", handle_mouse_move)
    cvs.bind("<Button-1>", handle_mouse_click)
    
    heart_object = Heart()
    draw(root, cvs, heart_object)
    root.mainloop()
