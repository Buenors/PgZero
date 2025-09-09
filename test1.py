import pgzrun
from pgzero.rect import Rect 

WIDTH = 1280
HEIGHT = 720

velocity_y = 0
gravity = 1

status = 'start'
character_data = [
    {
        "idle": "character_beige_idle",
        "walk": ["character_beige_walk_a", "character_beige_walk_b"],
        "jump": "character_beige_jump",
        "hit": "character_beige_hit",
        "pos": (5 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_green_idle",
        "walk": ["character_green_walk_a", "character_green_walk_b"],
        "jump": "character_green_jump",
        "hit": "character_green_hit",
        "pos": (4 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_pink_idle",
        "walk": ["character_pink_walk_a", "character_pink_walk_b"],
        "jump": "character_pink_jump",
        "hit": "character_pink_hit",
        "pos": (3 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_purple_idle",
        "walk": ["character_purple_walk_a", "character_purple_walk_b"],
        "jump": "character_purple_jump",
        "hit": "character_purple_hit",
        "pos": (2 * WIDTH/6, HEIGHT-128)
    },
    {
        "idle": "character_yellow_idle",
        "walk": ["character_yellow_walk_a", "character_yellow_walk_b"],
        "jump": "character_yellow_jump",
        "hit": "character_yellow_hit",
        "pos": (WIDTH/6, HEIGHT-128)
    },
]
characters = [Actor(data["idle"], pos=data["pos"]) for data in character_data]

alien = None
alien_idle = None
alien_walk_frames = []
alien_jump = None
alien_hit = None

# Variáveis separadas para cada animação
char_walk_timer = 0.0
char_walk_interval = 0.12 
char_current_frame = 0

frog_walk_timer = 0.0
frog_walk_interval = 0.4 
frog_current_frame = 0

bee_fly_timer = 0.0
bee_fly_interval = 0.2
bee_current_frame = 0

gem = Actor('gemgreen')
gem.x = 350
gem.y = 0

clouds = []
for x in range(5):
    cloud = Actor('background_clouds')
    cloud.x = x*256 + 128
    cloud.y = 256 + 128 -64 - 32

    clouds.append(cloud)

trees = [] 
for x in range(5):
    tree = Actor('background_color_trees')
    tree.x = x*256 + 128
    tree.y = 256*2 + 128 - 64 - 32
    
    trees.append(tree)
    
solidskyes = [] 
for x in range(5):
    solidsky = Actor('background_solid_sky')
    solidsky.x = x*256 + 128
    solidsky.y = 128 - 32 - 64
    
    solidskyes.append(solidsky)
    
floor = []
lava = []
for x in range(20):
    if 3 <= x <= 7:
        block = Actor('lava_top')
        lava.append(block)
    else:
        block = Actor("terrain_grass_block_top")
        floor.append(block)
    block.x = x*64 + 32
    block.y = 720-32

bottom_grasses = []
for x in range(20):
    bottom_grass = Actor('terrain_grass_block_top')
    bottom_grass.x = x*64 + 32
    bottom_grass.y = 720-32
    
    bottom_grasses.append(bottom_grass)

platforms = [
    Actor('terrain_grass_cloud_left', (32 + 64 * 4, HEIGHT-64*2)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 5, HEIGHT-64*2)),
    Actor('terrain_grass_cloud_right', (32 + 64 * 6, HEIGHT-64*2)),
    Actor('terrain_grass_cloud', (32 + 64 * 17, HEIGHT-64*2)),
    Actor('terrain_grass_cloud', (32 + 64 * 19, HEIGHT-64*4)),
    Actor('terrain_grass_cloud', (32 + 64 * 17, HEIGHT-64*6)),
    Actor('terrain_grass_cloud_left', (32 + 64 * 14, HEIGHT-64*6)),
    Actor('terrain_grass_cloud', (32 + 64 * 8, HEIGHT-64*6)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 5, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_right', (32 + 64 * 6, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_right', (32 + 64 * 15, HEIGHT-64*6)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 4, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_middle', (32 + 64 * 3, HEIGHT-64*7)),
    Actor('terrain_grass_cloud_left', (32 + 64 * 2, HEIGHT-64*7)),
    Actor('bridge', (32 + 64 * 13, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 12, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 11, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 10, HEIGHT-64*6)),
    Actor('bridge', (32 + 64 * 9, HEIGHT-64*6)),
]

traps = [
    Actor('saw',(32+64* 16, HEIGHT- 64*8)),
    Actor('spikes', (32+64 * 5, HEIGHT-64*3))
]


enemies_data = [{
    'idle_left' : 'frog_idle',
    'movement_1_left' : 'frog_jump',
    'movement_2_left' : 'frog_rest',
    'idle_right' : 'frog_idle_right',
    'movement_1_right' : 'frog_jump_right',
    'movement_2_right': 'frog_rest_right',
    'pos' : (0, HEIGHT - 128 + 32)
},
{
    'idle_left' : 'frog_idle',
    'movement_1_left' : 'frog_jump',
    'movement_2_left' : 'frog_rest',
    'idle_right' : 'frog_idle_right',
    'movement_1_right' : 'frog_jump_right',
    'movement_2_right': 'frog_rest_right',
    'pos' : (32+64*11, HEIGHT - 128 + 32)
},
{
    'idle_left' : 'frog_idle',
    'movement_1_left' : 'frog_jump',
    'movement_2_left' : 'frog_rest',
    'idle_right' : 'frog_idle_right',
    'movement_1_right' : 'frog_jump_right',
    'movement_2_right': 'frog_rest_right',
    'pos' : (32+64*4, HEIGHT - 128 - 64 * 6)
},
{
    'idle_left' : 'bee_rest',
    'movement_1_left' : 'bee_a',
    'movement_2_left' : 'bee_b',
    'idle_right' : 'bee_rest_right',
    'movement_1_right' : 'bee_a_right',
    'movement_2_right': 'bee_b_right',
    'pos' : (32+64*12, HEIGHT - 128 - 64 * 6)
}
    
]

# CRIAÇÃO DOS INIMIGOS E ADIÇÃO DE PROPRIEDADES (CORRIGIDO)
frogs = []
bees = []

for data in enemies_data:
    if 'frog' in data['idle_left']:
        frog = Actor(data['idle_right'], pos=data['pos'])
        frog.speed = 2
        frog.direction = 1 # 1 para a direita, -1 para a esquerda
        frog.right_limit = frog.x + 64 * 2
        frog.left_limit = frog.x - 64 * 2
        frog.frames_right = [data['movement_1_right'], data['movement_2_right'], data['idle_right']]
        frog.frames_left = [data['movement_1_left'], data['movement_2_left'], data['idle_left']]
        frogs.append(frog)
    elif 'bee' in data['idle_left']:
        bee = Actor(data['idle_right'], pos=data['pos'])
        bee.speed = 3
        bee.direction = 1
        bee.right_limit = bee.x + 64 * 3
        bee.left_limit = bee.x - 64 * 3
        bee.frames_right = [data['movement_1_right'], data['movement_2_right'], data['idle_right']]
        bee.frames_left = [data['movement_1_left'], data['movement_2_left'], data['idle_left']]
        bees.append(bee)

solids = floor + platforms

saw = traps[0]
saw.speed = 3
saw.direction = 1 # 1 means move down, -1 means move up
saw.top_limit = HEIGHT - 64 * 7
saw.bottom_limit = HEIGHT - 64 * 2

def draw():
    screen.clear()
    if status == 'start':
        draw_start()
    elif status == 'selection':
        draw_selection()
    elif status == 'game':
        draw_game()

    
    
    
def draw_start():
    screen.fill((0,0,0))
    
    for cloud in clouds:
        cloud.draw()    
        
    for tree in trees:
        tree.draw()
        
    for solidsky in solidskyes:
        solidsky.draw()
    
    for bottom_grass in bottom_grasses:
        bottom_grass.draw()
    
    screen.draw.text('Nome Incrível', center=(WIDTH//2, HEIGHT//3), fontsize=60, color='white')
    screen.draw.text("Pressione SPACE para começar", center=(WIDTH//2, HEIGHT//2), fontsize=40, color="yellow")
    
    

def draw_game():     
    screen.fill((0,0,0))
    
    for cloud in clouds:
        cloud.draw()    
        
    for tree in trees:
        tree.draw()
        
    for solidsky in solidskyes:
        solidsky.draw()
    
    for block in floor:
        block.draw()
        
    for s in solids:
        s.draw()
        
    alien.draw() 
    alien_hitbox = Rect((alien.x-10, alien.y-20), (20,10)) 
    screen.draw.rect(alien_hitbox, (255,0,0))  
      
    for l in lava:
        l.draw()
        #hitbox = Rect((l.x - l.width/2, l.y - l.height/2), (l.width, l.height))
        #screen.draw.rect(hitbox, (255,0,0))
        
    for f in frogs[1:]:
        f.draw()
        #frog_hitbox = Rect((f.x - 32, f.y - 32), (64,64))
        #screen.draw.rect(frog_hitbox, (255,0,0))
        
    for b in bees:
        b.draw()
        #bee_hitbox = Rect((b.x - 32, b.y - 16), (64,32))
        #screen.draw.rect(bee_hitbox, (255,0,0))
        
    for t in traps:
        t.draw()
        trap_hitbox = Rect((t.x - 16, t.y - 16), (32,32))
        screen.draw.rect(trap_hitbox, (255,0,0))
    
    gem.draw()
    
def draw_selection():
    screen.fill((0,0,0))
    
    for cloud in clouds:
        cloud.draw()    
        
    for tree in trees:
        tree.draw()
        
    for solidsky in solidskyes:
        solidsky.draw()
    
    for bottom_grass in bottom_grasses:
        bottom_grass.draw()
    
    screen.draw.text("Select your character", center=(WIDTH//2, 50), fontsize=40, color="red")
    for c in characters:
        c.draw()
    
    for frog in frogs[:1]:
        frog.draw()
    
def update(dt):
    global status, velocity_y, char_walk_timer, char_current_frame, frog_walk_timer, frog_current_frame, bee_fly_timer, bee_current_frame

    # ----- TELA DE SELEÇÃO -----
    if status == 'selection':
        # Movimento dos personagens
        for c in characters:
            c.x += 1
            if c.x > WIDTH:
                c.x = 0
        # Movimento dos inimigos
        for frog in frogs:
            frog.x += 1 
            if frog.x > WIDTH:
                frog.x = 0 
                
        # Lógica de animação
        char_walk_timer += dt
        frog_walk_timer += dt
        bee_fly_timer += dt
        
        # Animação dos personagens
        if char_walk_timer >= char_walk_interval:
            char_current_frame = (char_current_frame + 1) % 2
            for c in characters:
                if "beige" in c.image:
                    c.image = ["character_beige_walk_a", "character_beige_walk_b"][char_current_frame]
                elif "green" in c.image:
                    c.image = ["character_green_walk_a", "character_green_walk_b"][char_current_frame]
                elif "pink" in c.image:
                    c.image = ["character_pink_walk_a", "character_pink_walk_b"][char_current_frame]
                elif "purple" in c.image:
                    c.image = ["character_purple_walk_a", "character_purple_walk_b"][char_current_frame]
                elif "yellow" in c.image:
                    c.image = ["character_yellow_walk_a", "character_yellow_walk_b"][char_current_frame]
            
            char_walk_timer = 0.0

        # Animação dos sapos
        if frog_walk_timer >= frog_walk_interval:
            frog_current_frame = (frog_current_frame + 1) % 3
            for frog in frogs:
                frog.image = ['frog_jump_right','frog_rest_right','frog_idle_right'][frog_current_frame]
            
            frog_walk_timer = 0.0
            
        # Animação das abelhas (ainda sem movimento na tela de seleção)
        if bee_fly_timer >= bee_fly_interval:
            bee_current_frame = (bee_current_frame + 1) % 3
            for bee in bees:
                bee.image = ['bee_a_right', 'bee_b_right', 'bee_rest_right'][bee_current_frame]
            bee_fly_timer = 0.0
            
        return

    # ----- JOGO -----
    if status != 'game' or not alien:
        return

    moved = False

    # estado anterior (para detectar direção de colisão)
    original_x = alien.x
    original_y = alien.y
    prev_bottom = original_y + (alien.height / 2)
    prev_top    = original_y - (alien.height / 2)

    # movimento horizontal
    if keyboard.a:
        alien.x -= 5
        moved = True
    if keyboard.d:
        alien.x += 5
        moved = True

    # física vertical
    alien.y += velocity_y
    velocity_y += gravity

    # colisão com blocos sólidos (sem lava!)
    on_ground = False
    solids = floor + platforms
    
    feet = Rect((alien.x-10, alien.y + alien.height/2 - 5), (20,10))
    head = Rect((alien.x+10, alien.y - alien.height/2 - 5), (20,10))
    
    for block in solids:
        solids_hitbox = Rect((block.x - 32, block.y - 32), (64,64))
        if feet.colliderect(solids_hitbox):
            # caiu sobre o topo do bloco
            if velocity_y >= 0 and prev_bottom <= block.top:
                alien.y = block.top - alien.height / 2
                velocity_y = 0
                on_ground = True
            # bateu por baixo do bloco (cabeçada)
            elif velocity_y < 0 and prev_top >= block.bottom:
                alien.y = block.bottom + alien.height / 2
                velocity_y = 0
            else:
                # colisão lateral: desfaz apenas o deslocamento X
                alien.x = original_x

    for block in lava:
        lava_hitbox = Rect((block.x - 32, block.y - 32), (64,64))
        if feet.colliderect(lava_hitbox):
                alien.image = alien_hit
                if velocity_y < 4:
                    velocity_y = 4
                set_dead()
    
    for t in traps:
        trap_hitbox = Rect((t.x - 16, t.y - 16), (32,32))
        if feet.colliderect(trap_hitbox) or head.colliderect(trap_hitbox):
            alien.image = alien_hit
            set_dead()
            
    for f in frogs[1:]:
        frog_hitbox = Rect((f.x - 32, f.y - 32), (64,32))
        if feet.colliderect(frog_hitbox) or head.colliderect(frog_hitbox):
            alien.image = alien_hit
            set_dead()
            
    for b in bees:
        bee_hitbox = Rect((b.x - 32, b.y - 32), (64,32))
        if feet.colliderect(bee_hitbox) or head.colliderect(bee_hitbox):
            alien.image = alien_hit
            set_dead()

    
    # limites horizontais da tela
    if alien.x < 0:
        alien.x = 0
    if alien.x > WIDTH:
        alien.x = WIDTH


    # pulo: só se estiver no chão
    if keyboard.space and on_ground:
        velocity_y = -18
        alien.image = alien_jump

    # animação
    if on_ground:
        if keyboard.a or keyboard.d:
            char_walk_timer += dt
            if char_walk_timer >= char_walk_interval:
                animate_walk()
                char_walk_timer = 0.0
        else:
            alien.image = alien_idle
            char_walk_timer = 0.0
    else:
        # está no ar
        if velocity_y < 0:
            # subindo -> usar sprite de pulo
            alien.image = alien_jump
        else:
            # caindo -> se tiver sprite de queda, usa, senão mantém jump
            alien.image = alien_idle

    # Move a serra verticalmente
    saw.y += saw.speed * saw.direction
    
    # Checa os limites e inverte a direção
    if saw.y <= saw.top_limit:
        saw.direction = 1 # Muda para descer
    elif saw.y >= saw.bottom_limit:
        saw.direction = -1 # Muda para subir
        
    # Movimento dos sapos (CORRIGIDO)
    for frog in frogs[1:]:
        if frog.direction == 1: # Move para a direita
            frog.x += frog.speed
            if frog.x >= frog.right_limit:
                frog.direction = -1 # Inverte para esquerda
        elif frog.direction == -1: # Move para a esquerda
            frog.x -= frog.speed
            if frog.x <= frog.left_limit:
                frog.direction = 1 # Inverte para direita
    
    # Movimento das abelhas (NOVO E CORRIGIDO)
    for bee in bees:
        if bee.direction == 1:
            bee.x += bee.speed
            if bee.x >= bee.right_limit:
                bee.direction = -1
        elif bee.direction == -1:
            bee.x -= bee.speed
            if bee.x <= bee.left_limit:
                bee.direction = 1

    # Animação dos sapos (CORRIGIDO)
    frog_walk_timer += dt
    if frog_walk_timer >= frog_walk_interval:
        frog_current_frame = (frog_current_frame + 1) % 3
        for frog in frogs:
            if frog.direction == 1:
                frog.image = frog.frames_right[frog_current_frame]
            else:
                frog.image = frog.frames_left[frog_current_frame]
        frog_walk_timer = 0.0
        
    # Animação das abelhas (NOVO E CORRIGIDO)
    bee_fly_timer += dt
    if bee_fly_timer >= bee_fly_interval:
        bee_current_frame = (bee_current_frame + 1) % 3
        for bee in bees:
            if bee.direction == 1:
                bee.image = bee.frames_right[bee_current_frame]
            else:
                bee.image = bee.frames_left[bee_current_frame]
        bee_fly_timer = 0.0


def on_key_down(key):
    global status
    if status == 'start' and key == keys.SPACE:
        status = 'selection'
        
def on_mouse_down(pos):
    global alien, status, alien_idle, alien_walk_frames, alien_jump, alien_hit
    if status == 'selection':
        for i, c in enumerate(characters):
            if c.collidepoint(pos):
                data = character_data[i]
                alien = Actor(data["idle"])
                alien.pos = (128 , HEIGHT-128)
                alien_idle = data["idle"]
                alien_walk_frames = data["walk"]
                alien_jump = data["jump"]
                alien_hit = data["hit"]
                sounds.eep.play()

                clock.schedule_unique(start_game, 1.0)
                
    if status == 'game':
        if alien.collidepoint(pos):
            set_alien_hurt()

def start_game():
    global status
    status ='game'
                     
def set_alien_hurt(): 
    sounds.eep.play()
    alien.image = alien_hit
    
    clock.schedule_unique(set_alien_normal, 1.0) #unique 1 vez, após 1 segundo

def set_alien_normal():
    alien.image = alien_idle
    
def animate_walk():
    global char_current_frame
    alien.image = alien_walk_frames[char_current_frame]
    char_current_frame = (char_current_frame + 1) % len(alien_walk_frames)
    
def set_dead():
    global status
    alien.image = alien_hit
    sounds.eep.play()
    status = "dead"
    clock.schedule_unique(respawn, 2.0)

def respawn():
    global status
    alien.pos = (100, HEIGHT - 128)
    alien.image = alien_idle
    status = "game"
    
pgzrun.go()