import random
import math
import pygame
from pygame.locals import *

# Initiate
pygame.init()
pygame.mixer.init()
# variables
width, height = 640, 480
# represents for wasd 
keys = [False, False, False, False]
playerpos = [100, 100]
# accuracy: hitted / fired
acc = [0, 0]
arrows = []
screen = pygame.display.set_mode((width, height))
# badgers
badtimer = 100
badtimerarg = 0
badguys = [[640, 100]]
healthvalue = 194

# Load the image
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg = badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# Load the audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)





# Keep looping through
exitcode = 0
running = 1
while running:
	badtimer -= 1

	# dark background
	screen.fill(0)

	# grass
	for x in range(width / grass.get_width() + 1):
		for y in range(height / grass.get_height() + 1):
			screen.blit(grass, (x * 100, y * 100))
	# castle 
	for y in [30, 135, 240, 345]:
		screen.blit(castle, (0, y))

	# player with rotation ability
	mousepos = pygame.mouse.get_pos()
	center_x = playerpos[0] + 26
	center_y = playerpos[1] + 32
	angle = math.atan2(mousepos[1] - center_y, mousepos[0] - center_x)
	player_rotate = pygame.transform.rotate(player, -angle * 57.29)
	playerpos1 = (playerpos[0] - player_rotate.get_rect().width / 2,
			playerpos[1] - player_rotate.get_rect().height / 2)
	screen.blit(player_rotate, playerpos1)
	# arrows
	for index, bullet in enumerate(arrows):
		velx = math.cos(bullet[0]) * 10
		vely = math.sin(bullet[0]) * 10
		bullet[1] += velx
		bullet[2] += vely
		if bullet[1] < -64 or bullet[1] > 640 or \
			bullet[2] < -64 or bullet[2] > 480:
			arrows.pop(index)
	for projectile in arrows:
		arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
		screen.blit(arrow1, (projectile[1], projectile[2]))
	# badger timer settings
	if badtimer == 0:
		badguys.append([640, random.randint(50, 430)])
		badtimer = 100 - 2 * badtimerarg
		if badtimerarg >= 35:
			badtimerarg = 35
		else:
			badtimerarg += 5

	# show the badgers
	for index_badger, badguy in enumerate(badguys):
		if badguy[0] < -64:
			badguys.pop(index_badger)
		badguy[0] -= 7	
		badrect = pygame.Rect(badguyimg.get_rect())
		badrect.top = badguy[1]
		badrect.left = badguy[0]
		if badrect.left < 64:
			hit.play()
			healthvalue -= random.randint(5, 20)
			badguys.pop(index_badger)
		for index_arrow, bullet in enumerate(arrows):
			bullrect = pygame.Rect(arrow.get_rect())
			bullrect.left = bullet[1]
			bullrect.top = bullet[2]
			if badrect.colliderect(bullrect):
				acc[0] += 1
				badguys.pop(index_badger)
				arrows.pop(index_arrow)
				enemy.play()

	for badguy in badguys:
		screen.blit(badguyimg, badguy)

	# draw clock
	font = pygame.font.Font(None, 24)
	survivedtext = font.render(str((90000 - pygame.time.get_ticks())/60000)+":"+ \
			str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright = [635, 5]
	screen.blit(survivedtext, textRect)

	# draw health bar
	screen.blit(healthbar, (5, 5))
	for i in range(healthvalue):
		screen.blit(health, (i+8, 8))
				
	# show
	pygame.display.flip()
	
	# listening for the input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			elif event.key == K_a:
				keys[1] = True
			elif event.key == K_s:
				keys[2] = True
			elif event.key == K_d:
				keys[3] = True
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				keys[0] = False
			elif event.key == K_a:
				keys[1] = False
			elif event.key == K_s:
				keys[2] = False
			elif event.key == K_d:
				keys[3] = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			shoot.play()
			position = pygame.mouse.get_pos()
			acc[1] += 1
			arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
		if keys[0]: # w
			playerpos[1] -= 5
		elif keys[2]: # s
			playerpos[1] += 5
		if keys[1]: # a
			playerpos[0] -= 5
		elif keys[3]: # d
			playerpos[0] += 5
	if pygame.time.get_ticks() >= 90000:
		running = 0
		exitcode = 1
	if healthvalue <= 0:
		running = 0
		exitcode = 0
	if acc[1] != 0:
		accuracy = acc[0] * 1.0 / acc[1] * 100
	else:
		accuracy = 0

# prepare to show the result
pygame.font.init()
font = pygame.font.Font(None, 24)
text = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 0, 0))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

if exitcode == 0:
	screen.blit(gameover, (0, 0))
else:
	screen.blit(youwin, (0, 0))

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
	pygame.display.flip()
