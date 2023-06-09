import pygame
from data.support import import_folder
from random import choice
import time


class AnimationPlayer:
	def __init__(self):
		self.time = 0
		self.frames = {
			# magic
			'flame': import_folder('./graphics/particles/flame/frames'),
			'aura': import_folder('./graphics/particles/aura'),
			'heal': import_folder('./graphics/particles/heal/frames'),
			'fireball': import_folder('./graphics/particles/fireball'),
			
			# attacks 
			'claw': import_folder('./graphics/particles/claw'),
			'slash': import_folder('./graphics/particles/slash'),
			'sparkle': import_folder('./graphics/particles/sparkle'),
			'leaf_attack': import_folder('./graphics/particles/leaf_attack'),
			'thunder': import_folder('./graphics/particles/thunder'),
			'fireball': import_folder('./graphics/particles/fireball'),

			# monster deaths
			'smallbee': import_folder('./graphics/particles/smoke_orange'),
			'squid': import_folder('./graphics/particles/smoke_orange'),
			'raccoon': import_folder('./graphics/particles/raccoon'),
			'worm': import_folder('./graphics/particles/worm'),
			'spirit': import_folder('./graphics/particles/nova'),
			'slime': import_folder('./graphics/particles/slime'),
			'bamboo': import_folder('./graphics/particles/bamboo'),
			
			# leafs 
			'leaf': (
				import_folder('./graphics/particles/leaf1'),
				import_folder('./graphics/particles/leaf2'),
				import_folder('./graphics/particles/leaf3'),
				import_folder('./graphics/particles/leaf4'),
				import_folder('./graphics/particles/leaf5'),
				import_folder('./graphics/particles/leaf6'),
				self.reflect_images(import_folder('./graphics/particles/leaf1')),
				self.reflect_images(import_folder('./graphics/particles/leaf2')),
				self.reflect_images(import_folder('./graphics/particles/leaf3')),
				self.reflect_images(import_folder('./graphics/particles/leaf4')),
				self.reflect_images(import_folder('./graphics/particles/leaf5')),
				self.reflect_images(import_folder('./graphics/particles/leaf6'))
				)
			}
	
	def reflect_images(self,frames):
		new_frames = []

		for frame in frames:
			flipped_frame = pygame.transform.flip(frame,True,False)
			new_frames.append(flipped_frame)
		return new_frames

	def create_grass_particles(self,pos,groups):
		animation_frames = choice(self.frames['leaf'])
		ParticleEffect(pos,animation_frames,groups)

	def create_particles(self,animation_type,pos,groups):
		animation_frames = self.frames[animation_type]
		print(animation_frames)
		ParticleEffect(pos,animation_frames,groups,animation_type)


class ParticleEffect(pygame.sprite.Sprite):
	
	
	def __init__(self,pos,animation_frames,groups,animation_type):
		super().__init__(groups)
		self.attacktype = 'blaze_bolt_' + str(int(time.time()))
		self.animation_type = animation_type

		self.pos = pos
		self.startup = 0
		self.hit_delay = 0
		self.startup = 0
		if animation_type == 'flame':
			self.hit_delay = 600
			self.startup = 20
		self.frame_index = 0
		self.animation_speed = 0.15
		self.frames = animation_frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect()
		
	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self):
		self.animate()
		if self.startup > 0:
			self.startup -= 1
		else:			
			self.rect = self.image.get_rect(center = self.pos)			
			self.startup = 20
			
