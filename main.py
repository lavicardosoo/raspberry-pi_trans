import pygame as pg
from emoji import emojize
from random import choice
#build a raspberry pi!🍓

def load(type,sound,img,width, height):
	if type == "sound":
		s = pg.mixer.Sound(sound)
		return s
	elif type == "img":
		i = pg.image.load(img)
		i = pg.transform.scale(i,(width,height))
		return i	
	
pg.init()

#define o tamanho da tela cis
width = 950
height = 700

#ajusta a tela de acordo com as medidas passadas
screen = pg.display.set_mode((width, height))

#posição origem e tamanho dos componentes 
#p - se refere ao local certo onde as peças devem ficar
#t - se referem ao tamanho do rect dessas peças
p_cpu = (294, 298)
t_cpu = (130,100)
p_ram =  (431, 296)
t_ram = (100,100)
p_fonte = (177, 493)
t_fonte = (80,43)
p_usb2 =  (682, 443)
t_usb2 = (150,85)
p_usb3 = (680, 341)
t_usb3 = (150,85)
p_audio = (514, 454)
t_audio = (70,100)
p_ethernet = (643, 216)
t_ethernet = (170,100)
p_w_b = (177, 242)
t_w_b = (93,85)

#carregando imagens e áudios
bg = load("img", False, "media/bg.png", width, height)

tittle = load("img", False, "media/text.png", 300,100)
arrasou = load("img", False, "media/arrasou.png", 300,100)
burra = load("img", False, "media/burra.png", 300,100)
good_lucky = load("img", False, "media/img.png", 300,120)
board_img = load("img",False, "media/board.png", 800,600)
sair = load('img',False,'media/get_out.png',150,70)
join_audio = pg.mixer.Sound("media/put.mp3")
aiqdlc = pg.mixer.Sound("media/aiqdlc.mp3")
inutil = pg.mixer.Sound("media/inutil.mp3")
aiqvergonha = pg.mixer.Sound("media/aiqvergonha.mp3")
aplausos = pg.mixer.Sound("media/aplausos.mp3")

join_audio.set_volume(1.0)
inutil.set_volume(1.0)
aiqdlc.set_volume(1.0)
aplausos.set_volume(0.7)

components_img = {"cpu" : load("img", False, "media/cpu.png", 130, 100), 
"ram" : load("img", False, "media/ram.png", 100,100), 
"fonte" : load("img", False, "media/fonte.png", 80,43), 
"usb2" : load("img", False, "media/usb2.png", 150,85), 
"usb3" : load("img", False, "media/usb3.png", 150,85), 
"w&b" : load("img", False, "media/wifi&blue.png", 93,85), 
"audio" : load("img", False, "media/audio.png", 70,100), 
"ethernet" : load("img", False, "media/ethernet.png", 170,100)
}

sairrect = sair.get_rect()
#função para carregar imagens e áudios.

def load(type,sound,img,width, height):

	if type == "sound":
		s = pg.mixer.Sound(sound)
		return s
	elif type == "img":
		i = pg.image.load(img)
		i = pg.transform.scale(i,(width,height))
		return i		

		
#classe a placa mãe
class Board(pg.sprite.Sprite):
	
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = board_img
		self.rect = self.image.get_rect()
		self.rect[0] = width / 2 - 400
		self.rect[1] = 80

#classe que irá dar vida aos objetos dos componentes 
class Components(pg.sprite.Sprite):
	
	#argumentos:imagem, esquerda, direita, tamanho do rect que vai ser utilizado para definir o local do componente e a sua posição. 
	def __init__(self, img, left,top,rw_rh, rl_rr):
		
		pg.sprite.Sprite.__init__(self)

		self.myplace = pg.Rect(rl_rr,(rw_rh[0] / 2,rw_rh[1] / 2)) 
		self.myplace.top += 20
		self.myplace.left += 30
		
		self.pos = rl_rr
		self.image = img

		self.rect = self.image.get_rect()
		self.rect[0] = left
		self.rect[1] = top
		self.rect[2], self.rect[3] = rw_rh

		self.touched = False
		self.joined = False

		self.mouse = 0
		self.state = [1,2,3]
		self.state[0] = "parado"
		
	def update(self):
		if self.touched and self.joined == False:
			#se o touched for verdadeiro o obj vai se mover de acordo com o movimento do cursor do mouse
			self.rect[0],self.rect[1] = pg.mouse.get_pos()
			self.state[0] = "em movimento"
	
	#testa se a posição do cursor e a do objeto estão se colidindo		
	def touch(self, mouse):
		self.mouse = mouse
		if self.rect.collidepoint(mouse.pos):
			self.touched = True
		

	#testa se o componente está na sua posição de origem e o fixa		
	def join(self,array):
		if self.state[0] == "em movimento":
			self.state[1] = "solto"

		my_audio_choice = choice((join_audio,aiqdlc))
		my_badaudio_choice = choice((inutil,aiqvergonha))

		if self.rect.colliderect(self.myplace) and self.joined == False:
			self.state[1] = "no lugar de origem"
			
			self.rect[0], self.rect[1] = self.pos
			self.joined = True
			array.remove(self)
			join_audio.play()
			my_audio_choice.play()
					
		if self.state[1] == "solto" and self.joined == False:
			img = burra
			my_badaudio_choice.play()
			self.state = [1,2,3]

#criando os objetos
MotherBoard = Board()
cpu = Components(components_img["cpu"], 800,400, t_cpu, p_cpu)
ram = Components(components_img["ram"], 10,220, t_ram, p_ram)
fonte = Components(components_img["fonte"],10,400,(t_fonte[0] + 30,t_fonte[1] + 10), p_fonte)
usb2 = Components(components_img["usb2"], 100,100, t_usb2, p_usb2)
usb3 = Components(components_img["usb3"], 200,600, t_usb3, p_usb3)
w_b = Components(components_img["w&b"], 750,600, t_w_b, p_w_b)
audio = Components(components_img["audio"], 100,600, t_audio, p_audio)
ethernet = Components(components_img["ethernet"], 380,590, t_ethernet, p_ethernet)

#grupo de sprites
group = pg.sprite.Group()
group.add(MotherBoard, cpu, ram, fonte, usb2, usb3, w_b, ethernet, audio)	

#lista que armazena os objetos dos componentes
joined = [cpu,ram,fonte,usb2,usb3,w_b,audio,ethernet]

#contador
ok = 0

while True:
	
	for ev in pg.event.get():
		if ev.type == quit:
			pg.quit()
			
		elif ev.type == pg.MOUSEBUTTONDOWN:
			joinedlen = len(joined)
			cpu.touch(ev)
			ram.touch(ev)
			fonte.touch(ev)
			usb2.touch(ev)
			usb3.touch(ev)
			w_b.touch(ev)
			audio.touch(ev)
			ethernet.touch(ev)

			if sairrect.colliderect(pg.mouse.get_pos()):
				pg.quit()
				
		elif ev.type == pg.KEYDOWN:
			#se clicar na tecla 6 o jogo fecha
			if ev.key == 1073741918:
				pg.quit()
			
		elif ev.type == pg.MOUSEBUTTONUP:

			cpu.touched = False
			ram.touched = False
			fonte.touched = False
			usb2.touched = False
			usb3.touched = False
			w_b.touched = False
			audio.touched = False
			ethernet.touched = False

			cpu.join(joined)
			ram.join(joined)
			fonte.join(joined)
			usb2.join(joined)
			usb3.join(joined)
			w_b.join(joined)
			audio.join(joined)
			ethernet.join(joined)

			print(joinedlen)
			print(len(joined))

			good_lucky = burra

			if joinedlen != len(joined):
				good_lucky = arrasou
				
	if cpu.joined and ram.joined and usb2.joined and usb3.joined and fonte.joined and ethernet.joined and audio. joined and w_b.joined and ok < 1:
		aplausos.play()
		ok+= 1
							
	screen.blit(bg, (0,0))
	screen.blit(tittle,(350,20))
	screen.blit(good_lucky,(350,90))
	screen.blit(sair,(800,20))
	group.draw(screen)
	
	cpu.update()
	ram.update()
	fonte.update()
	usb2.update()
	usb3.update()
	w_b.update()
	audio.update()
	ethernet.update()
	pg.display.update()

