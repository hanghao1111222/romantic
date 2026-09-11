import turtle
import math
import random

# ================= 1. 窗口与画笔初始化 =================
screen = turtle.Screen()
screen.title("浪漫玫瑰与漫天落瓣 (点击窗口任意位置可关闭)")
screen.bgcolor("#0a0f1d")  # 深邃暗夜蓝
screen.setup(1000, 800)
screen.tracer(0)           # 关闭自动刷新，提升绘制效率和动画流畅度

# 确保窗口弹到 macOS 前台
try:
    root = screen._root
    root.lift()
    root.attributes('-topmost', True)
    root.after(500, lambda: root.attributes('-topmost', False))
    root.focus_force()
except Exception:
    pass

# 绘制花茎与叶片的画笔
stem = turtle.Turtle()
stem.hideturtle()
stem.speed(0)

# 绘制玫瑰花朵的画笔
flower = turtle.Turtle()
flower.hideturtle()
flower.speed(0)

# 提示文字画笔
text_pen = turtle.Turtle()
text_pen.hideturtle()
text_pen.penup()
text_pen.color("#f7d6e0")
text_pen.goto(0, -350)
text_pen.write("A Rose For You", align="center", font=("Snell Roundhand", 24, "italic"))

# ================= 2. 绘制花茎与叶子 =================
def draw_stem_and_leaves():
    # 绘制花茎
    stem.penup()
    stem.goto(0, -30)
    stem.pendown()
    stem.color("#2d6a4f")  # 茎的深绿
    stem.pensize(5)
    stem.setheading(-90)
    
    # 优雅的微弯花茎
    for _ in range(30):
        stem.forward(8)
        stem.right(0.3)
    
    # 绘制左侧叶子
    stem.penup()
    stem.goto(-10, -130)
    stem.setheading(150)
    stem.color("#40916c")
    stem.begin_fill()
    stem.pendown()
    stem.circle(60, 70)
    stem.left(110)
    stem.circle(60, 70)
    stem.end_fill()
    
    # 绘制右侧叶子
    stem.penup()
    stem.goto(15, -190)
    stem.setheading(30)
    stem.color("#52b788")
    stem.begin_fill()
    stem.pendown()
    stem.circle(70, 65)
    stem.left(115)
    stem.circle(70, 65)
    stem.end_fill()

# ================= 3. 绘制多层多角度玫瑰花 =================
def draw_rose():
    # 花瓣层级配置：(层半径, 旋转偏移角度, 颜色)
    # 通过角度交错（让花瓣层层错开），营造更加立体饱满的玫瑰形态
    layers_config = [
        (130, 0,  "#d90429"),   # 外层：深绯红
        (115, 25, "#e63946"),   # 中外层：亮红
        (100, 50, "#ff4d6d"),   # 中层：瑰红
        (85,  75, "#ff758f"),   # 中内层：柔粉红
        (70,  15, "#ff8fa3"),   # 内层：粉色
        (55,  40, "#ffb3c1"),   # 花心外圈：浅粉
        (40,  65, "#ffccd5"),   # 花心中央：嫩粉
    ]
    
    for radius, offset_deg, col in layers_config:
        flower.color(col)
        flower.fillcolor(col)
        flower.begin_fill()
        
        rot_rad = math.radians(offset_deg)
        cos_rot = math.cos(rot_rad)
        sin_rot = math.sin(rot_rad)
        
        # 360 度平滑绘制闭合花瓣
        for deg in range(0, 361, 4):
            rad = math.radians(deg)
            # 自然曲线参数方程
            x_base = radius * math.sin(rad) * (abs(math.cos(rad)) ** 0.5)
            y_base = radius * math.cos(rad) * (abs(math.sin(rad)) ** 0.5)
            
            # 对当前层施加旋转，使层与层之间错位重叠
            x = x_base * cos_rot - y_base * sin_rot
            y = x_base * sin_rot + y_base * cos_rot + 30  # 稍微向上移动花朵中心
            
            if deg == 0:
                flower.penup()
                flower.goto(x, y)
                flower.pendown()
            else:
                flower.goto(x, y)
                
        flower.end_fill()

# ================= 4. 连续飘落花瓣粒子系统 =================
# 创建花瓣粒子群（支持多片花瓣同时随风轻柔飘落，不阻塞界面）
PETAL_COUNT = 32
petals = []
petal_colors = ["#ffccd5", "#ffb3c1", "#ff8fa3", "#ffa8b6", "#ffe5ec"]

for _ in range(PETAL_COUNT):
    p = turtle.Turtle()
    p.hideturtle()
    p.speed(0)
    p.shape("circle")
    p.penup()
    
    # 随机初始属性
    p_color = random.choice(petal_colors)
    p.color(p_color)
    
    # 给小圆变形模拟椭圆花瓣
    w = random.uniform(0.3, 0.7)
    h = random.uniform(0.6, 1.1)
    p.shapesize(h, w)
    
    x = random.randint(-480, 480)
    y = random.randint(-350, 400)
    vx = random.uniform(-0.8, 0.8)   # 水平飘摆
    vy = random.uniform(1.8, 4.2)    # 飘落速度
    p.goto(x, y)
    p.showturtle()
    
    petals.append({"pen": p, "x": x, "y": y, "vx": vx, "vy": vy, "angle": random.randint(0, 360)})

is_running = True

def on_close(x=0, y=0):
    global is_running
    is_running = False
    try:
        screen.bye()
    except Exception:
        pass

# 点击屏幕可直接关闭
screen.onscreenclick(on_close)

def animate():
    """动画更新函数：逐帧更新每片花瓣的位置"""
    if not is_running:
        return
    for item in petals:
        # 下落与飘荡
        item["y"] -= item["vy"]
        item["x"] += item["vx"] + math.sin(item["y"] * 0.03) * 0.7  # 模拟正弦微风摆动
        item["angle"] = (item["angle"] + 2) % 360
        item["pen"].setheading(item["angle"])
        
        # 若飘出底端或侧边，重置到顶部再次飘落
        if item["y"] < -400 or item["x"] < -520 or item["x"] > 520:
            item["y"] = random.randint(380, 430)
            item["x"] = random.randint(-480, 480)
            item["vy"] = random.uniform(1.8, 4.2)
            item["vx"] = random.uniform(-0.8, 0.8)
            
        item["pen"].goto(item["x"], item["y"])
    
    try:
        screen.update()
        screen.ontimer(animate, 30)  # 每 30 毫秒刷新一帧 (~33 FPS)
    except turtle.Terminator:
        pass

# ================= 5. 启动程序 =================
if __name__ == "__main__":
    draw_stem_and_leaves()
    draw_rose()
    screen.update()  # 先显示绘制完成的玫瑰
    animate()        # 开启花瓣飘落动画
    screen.mainloop()
