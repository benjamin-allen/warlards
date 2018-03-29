import pygame as pg
import time
"""
Debugging Quadrantmap
+----+----+
| P1 | P2 |
|    |    |
+----+----+
| P3 | P4 |
|    |    |
+----+----+

Debugging keymap:
Player: <- | B | K | ->
P1    :  a | w | s | d
P2    :  f | t | g | h
P3    :  i | j | k | l
P4    :  4 | 8 | 5 | 6
"""
# CONSTANTS
SCREEN_H = 868
SCREEN_W = 1392
C_SIZE = SCREEN_H / 4
FG_SIZE = SCREEN_H if SCREEN_H < SCREEN_W else SCREEN_W
#			 R    G    B
P1_COLOR = (209,  18,  76)
P2_COLOR = (234, 181,  20)
P3_COLOR = ( 37,  37, 164)
P4_COLOR = (104, 209,  18)
BG_COLOR = ( 32,  32,  32)

FPS = 60 		# Target framerate

def main():
	global FPSCLOCK, DISP, FONT
	
	pg.init()
	FPSCLOCK = pg.time.Clock()
	DISP = pg.display.set_mode((SCREEN_W, SCREEN_H), pg.FULLSCREEN)
	FONT = pg.font.SysFont('Monospace', 24)
	
	colors = [P1_COLOR, P2_COLOR, P3_COLOR, P4_COLOR]
	
	ais = []
	players = []
	
	while len(ais) + len(players) < 2:
		DISP.fill((0, 0, 0))
		pg.display.update()
		player_setup = showStart()		# [plr/com/none, plr/com/none,...]
		
		castles = []
		ais = []
		players = []
		
		k = 0
		l = 0
		for i in [0, FG_SIZE - C_SIZE]:
			for j in [0, FG_SIZE - C_SIZE]:
				if player_setup[k] != 0:
					castles.append({"rect": pg.Rect(j, i, C_SIZE, C_SIZE), "color": colors[k]})
				if player_setup[k] == 1:
					players.append({"player": k+1, "index": l})
					l += 1
				elif player_setup[k] == -1:
					ais.append({"player": k+1, "index": l})
					l += 1
				k+=1
	game(players, ais, castles)

def showStart():
	FPS = 30
	title_font = pg.font.Font('Ringbearer.TTF', 36)
	under = title_font.render("Press the button to play, or press the knob to make a computer player", True, P2_COLOR)
	title_font = pg.font.Font('Carolingia.TTF', 144)
	title = title_font.render("WARLARDS", True, P1_COLOR)
	
	pg.event.get() # Clear the event buffer
	
	DISP.blit(title, (SCREEN_W / 2 - title.get_size()[0] / 2, SCREEN_H / 4 - title.get_size()[1]))
	DISP.blit(under, (SCREEN_W / 2 - under.get_size()[0] / 2, SCREEN_H / 4))
	
	frame_down = 300
	int_timer = 10
	player_status = [0, 0, 0, 0]
	previous_status = player_status * 1
	while frame_down > 0 and player_status != [1, 1, 1, 1]:
		changed = False
		for e in pg.event.get():
			if e.type == pg.KEYDOWN:
				if e.key == pg.K_w:
					player_status[0] = 1
				if e.key == pg.K_s:
					player_status[0] = 0 if player_status[0] == 1 else -1
				if e.key == pg.K_t:
					player_status[1] = 1
				if e.key == pg.K_g:
					player_status[1] = 0 if player_status[1] == 1 else -1
				if e.key == pg.K_i:
					player_status[2] = 1
				if e.key == pg.K_k: 
					player_status[2] = 0 if player_status[2] == 1 else -1
				if e.key == pg.K_KP8:
					player_status[3] = 1
				if e.key == pg.K_KP5:
					player_status[3] = 0 if player_status[3] == 1 else -1
		if player_status != previous_status:
			if player_status[0] == 1:
				pg.draw.circle(DISP, P1_COLOR, (75, 75), 50, 0)
			elif player_status[0] == -1:
				pg.draw.circle(DISP, P1_COLOR, (75, 75), 49, 5)
			else:
				pg.draw.circle(DISP, (0, 0, 0), (75, 75), 50, 0)
			if player_status[1] == 1:
				pg.draw.circle(DISP, P2_COLOR, (SCREEN_W - 75, 75), 50, 0)
			elif player_status[1] == -1:
				pg.draw.circle(DISP, P2_COLOR, (SCREEN_W - 75, 75), 49, 5)
			else:
				pg.draw.circle(DISP, (0, 0, 0), (SCREEN_W - 75, 75), 50, 0)
			if player_status[2] == 1:
				pg.draw.circle(DISP, P3_COLOR, (75, SCREEN_H - 75), 50, 0)
			elif player_status[2] == -1:
				pg.draw.circle(DISP, P3_COLOR, (75, SCREEN_H - 75), 49, 5)
			else:
				pg.draw.circle(DISP, (0, 0, 0), (75, SCREEN_H - 75), 50, 0)
			if player_status[3] == 1:
				pg.draw.circle(DISP, P4_COLOR, (SCREEN_W - 75, SCREEN_H - 75), 50, 0)
			elif player_status[3] == -1:
				pg.draw.circle(DISP, P4_COLOR, (SCREEN_W - 75, SCREEN_H - 75), 49, 5)
			else:
				pg.draw.circle(DISP, (0, 0, 0), (SCREEN_W - 75, SCREEN_H - 75), 50, 0)
			changed = True
		if frame_down % 30 == 0:
			int_timer = frame_down // 30
			timer = title_font.render(str(int_timer), True, P1_COLOR)
			number_rect = pg.Rect(SCREEN_W / 2 - timer.get_size()[0]-100, SCREEN_H / 2, timer.get_size()[0]+200, 144)
			pg.draw.rect(DISP, (0, 0, 0), number_rect, 0)
			DISP.blit(timer, (SCREEN_W / 2 - timer.get_size()[0] / 2, SCREEN_H / 2))
			changed = True
		if changed:
			pg.display.update()
		frame_down -= 1
		previous_status = 1 * player_status
		FPSCLOCK.tick(FPS)
	return player_status


if __name__ == "__main__":
	main()
