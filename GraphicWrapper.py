import tkinter as Tkinter
from util import *

WINDOWSIZE = 600
DRAW_DELAY = 1000
class GraphicWrapper:

	def __init__(self, world, per_step_fn, num_steps):
		self.worldszx = len(world)
		self.worldszy = len(world[0])
		self.world = world

		self.update_sim_fn = per_step_fn
		self.num_steps = num_steps
		self.curr_step = 0

		# Setup graphics
		self.tk = Tkinter.Tk()
		self.tk.after(0, self.draw)
		self.canvas = Tkinter.Canvas(self.tk, width=WINDOWSIZE, height=WINDOWSIZE)
		self.canvas.pack()
		rectszx = WINDOWSIZE/self.worldszx
		rectszy = WINDOWSIZE/self.worldszy

		# Create rectangles to represent trees
		self.rects = [[
						self.canvas.create_rectangle(x*rectszx, y*rectszy,
							x*rectszx + rectszx, y*rectszy + rectszy,
							fill="pink", outline="pink")
						for x in range(self.worldszx)] for y in range(self.worldszy)
					]

	def getColor(self, obj):
		color = "#aaaaaa"
		if obj is None:
			pass
		elif obj.getType() == SPECIES_A:
			color = "#ff0000"
		elif obj.getType() == SPECIES_B:
			color = "#0000ff"
		elif obj.getType() == FOOD_1:
			color = "#00ff00"
		elif obj.getType() == FOOD_2:
			color = "#ffff00"
		return color

	def draw(self):
		for x in range(self.worldszx):
			for y in range(self.worldszy):
				self.canvas.itemconfig(self.rects[x][y],
					fill=self.getColor(self.world[x][y]),
					outline='#aaaaaa',
					width=1)

	def update(self):
		self.curr_step += 1
		if self.curr_step > self.num_steps:
			return
		self.draw()
		self.update_sim_fn()
		self.tk.after(DRAW_DELAY, self.update)

	def run(self):
		self.update()
		Tkinter.mainloop()