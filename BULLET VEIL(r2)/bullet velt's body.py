import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 初始化pygame的音频模块
pygame.mixer.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Velt")

# 字体
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

# 加载图像资源
def load_image(filename, size=None):
    try:
        image = pygame.image.load(filename)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        sys.exit()

# 加载图像
player_image = load_image("player.png", (35, 35))
background_image = load_image("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
bullet_red_image = load_image("bullet_red.png", (35, 35))  # 红色子弹
bullet_pink_image = load_image("bullet_pink.png", (35, 35))  # 粉色子弹
power_up_white_image = load_image("power_up_white.png", (35, 35))  # 白色道具
power_up_green_image = load_image("power_up_green.png", (40, 40))  # 绿色道具
power_up_yellow_image = load_image("Power_up_yellow.png", (35, 35))  # 加分道具

# 显示开始界面
def show_start_screen():
    screen.fill(BLACK)
    title_text = title_font.render("Bullet Veil", True, WHITE)
    start_prompt = font.render("Press ENTER to Start", True, BLUE)
    tutorial_prompt = font.render("Press SPACE for Tutorial", True, PINK)  # 新增的提示
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
    screen.blit(start_prompt, (SCREEN_WIDTH // 2 - start_prompt.get_width() // 2, 400))
    screen.blit(tutorial_prompt, (SCREEN_WIDTH // 2 - tutorial_prompt.get_width() // 2, 440))  # 新增位置
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_SPACE:  # 空格键进入教程
                    waiting = False
                    show_tutorial_screen()  # 调用教程页面函数

def show_tutorial_screen():
    screen.fill(BLACK)
    tutorial_text = title_font.render("Tutorial", True, WHITE)
    tutorial_content_lines = [
        "Use WASD to move and avoid bombs.",
        "Green barrel: clear bombs, Blue barrel: invincibility, Star: +10 points.",
        "Level 5: bombs move horizontally, Level 15: tracking bombs."
    ]
    back_prompt = font.render("Press SPACE to go back", True, BLUE)

    # 绘制标题
    screen.blit(tutorial_text, (SCREEN_WIDTH // 2 - tutorial_text.get_width() // 2, 200))

    # 绘制教程内容
    for i, line in enumerate(tutorial_content_lines):
        line_text = font.render(line, True, WHITE)
        screen.blit(line_text, (SCREEN_WIDTH // 2 - line_text.get_width() // 2, 280 + i * 30))  # 每行之间增加一些间距

    # 绘制返回提示
    screen.blit(back_prompt, (SCREEN_WIDTH // 2 - back_prompt.get_width() // 2, 400))

    pygame.display.flip()



    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # 空格键返回主页
                waiting = False
                show_start_screen()

# 显示结算界面
def show_game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = title_font.render("Game Over", True, RED)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    restart_prompt = font.render("Press ENTER to Restart", True, BLUE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(restart_prompt, (SCREEN_WIDTH // 2 - restart_prompt.get_width() // 2, 400))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def play_background_music():
    try:
        pygame.mixer.music.load("background_music.mp3")  # 确保文件路径正确
        pygame.mixer.music.set_volume(1.0)  # 设置音量为最大
        pygame.mixer.music.play(loops=-1, start=0.0)  # 循环播放背景音乐
    except pygame.error as e:
        print(f"Error loading music: {e}")

# 玩家类
class Player:
    def __init__(self, x, y, radius, color, speed, image=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.invincible = False
        self.invincible_timer = 0
        self.image = image

    def move(self, keys):
        if keys[pygame.K_a] and self.x > self.radius:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < SCREEN_WIDTH - self.radius:
            self.x += self.speed
        if keys[pygame.K_w] and self.y > self.radius:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < SCREEN_HEIGHT - self.radius:
            self.y += self.speed

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x - self.radius, self.y - self.radius))
        else:
            color = YELLOW if self.invincible else self.color
            pygame.draw.circle(surface, color, (self.x, self.y), self.radius)

    def check_invincibility(self):
        if self.invincible and pygame.time.get_ticks() - self.invincible_timer > 1500:
            self.invincible = False

    def draw_invincibility_bar(self, surface):
        if self.invincible:
            elapsed_time = pygame.time.get_ticks() - self.invincible_timer
            progress = max(0, 1 - elapsed_time / 1500)
            pygame.draw.rect(surface, (255, 255, 0), (10, 10, 200 * progress, 20))

# 子弹类
class Bullet:
    def __init__(self, x, y, size, color, speed, direction, tracking=False, player=None, image=None):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.direction = direction
        self.tracking = tracking
        self.player = player
        self.tracking_timer = pygame.time.get_ticks()
        self.image = image

    def move(self):
        if self.tracking and self.player:
            if pygame.time.get_ticks() - self.tracking_timer < 1000:
                dx = self.player.x - self.x
                dy = self.player.y - self.y
                dist = (dx**2 + dy**2)**0.5
                if dist != 0:
                    self.x += (dx / dist) * self.speed
                    self.y += (dy / dist) * self.speed
            else:
                self.tracking = False
        else:
            if self.direction == "down":
                self.y += self.speed
            elif self.direction == "right":
                self.x += self.speed

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))  # 使用图像绘制
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def off_screen(self):
        return self.y > SCREEN_HEIGHT or self.x > SCREEN_WIDTH

# 道具类
class PowerUp:
    def __init__(self, x, y, size, color, speed, effect, image=None):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.effect = effect
        self.image = image

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))  # 使用图像绘制
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

# 碰撞检测
def check_collision(obj1, obj2):
    distance = ((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)**0.5
    return distance < obj1.radius + obj2.size // 2

# 初始化游戏变量
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, 15, BLUE, 8, player_image)
bullets = []
power_ups = []
clock = pygame.time.Clock()
score = 0
level = 1
level_timer = pygame.time.get_ticks()
MAX_BULLET_SPEED = 15  # 子弹速度上限

# 游戏主循环
play_background_music()  # 启动时播放背景音乐
show_start_screen()
running = True
while running:
    screen.blit(background_image, (0, 0))

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player.move(keys)

    # 更新子弹
    if random.random() < 0.03 + level * 0.005:
        bullet_speed = min(5 + level, MAX_BULLET_SPEED)
        bullets.append(Bullet(random.randint(0, SCREEN_WIDTH - 15), 0, 15, RED, bullet_speed, "down", image=bullet_red_image))
    if level >= 5 and random.random() < 0.02:
        bullet_speed = min(5 + level, MAX_BULLET_SPEED)
        bullets.append(Bullet(0, random.randint(0, SCREEN_HEIGHT - 15), 15, RED, bullet_speed, "right", image=bullet_red_image))
    if level >= 15 and random.random() < 0.01:
        bullet_speed = min(1 + level * 0.5, MAX_BULLET_SPEED)
        bullets.append(Bullet(random.randint(0, SCREEN_WIDTH - 15), 0, 15, PINK, bullet_speed, "down", tracking=True, player=player, image=bullet_pink_image))

    for bullet in bullets[:]:
        bullet.move()
        if bullet.off_screen():
            bullets.remove(bullet)
            score += 1

    # 更新道具
    if random.random() < 0.01:
        power_ups.append(PowerUp(random.randint(0, SCREEN_WIDTH - 15), 0, 15, WHITE, 3, "invincible", image=power_up_white_image))
    if random.random() < 0.01:
        power_ups.append(PowerUp(random.randint(0, SCREEN_WIDTH - 15), 0, 15, GREEN, 3, "clear", image=power_up_green_image))
    if random.random() < 0.02:  # 增加概率
        power_ups.append(PowerUp(random.randint(0, SCREEN_WIDTH - 15), 0, 15, YELLOW, 3, "score", image=power_up_yellow_image))

    for power_up in power_ups[:]:
        power_up.move()
        if power_up.off_screen():
            power_ups.remove(power_up)

    # 碰撞检测
    for bullet in bullets[:]:
        if not player.invincible and check_collision(player, bullet):
            show_game_over_screen(score)
            bullets.clear()
            power_ups.clear()
            score = 0
            level = 1
            level_timer = pygame.time.get_ticks()
            break

    for power_up in power_ups[:]:
        if check_collision(player, power_up):
            if power_up.effect == "invincible":
                player.invincible = True
                player.invincible_timer = pygame.time.get_ticks()
            elif power_up.effect == "clear":
                bullets.clear()
            elif power_up.effect == "score":
                score += 10  # 加分道具效果
            power_ups.remove(power_up)

    # 绘制玩家、子弹和道具
    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for power_up in power_ups:
        power_up.draw(screen)

    # 无敌状态检查
    player.check_invincibility()
    player.draw_invincibility_bar(screen)

    # 显示分数和关卡
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))

    pygame.display.flip()

    # 增加关卡
    if pygame.time.get_ticks() - level_timer > 5000:
        level += 1
        level_timer = pygame.time.get_ticks()

    clock.tick(30)