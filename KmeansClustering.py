import pygame
from random import randint
import numpy as np 
import math as mt 
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

red = (255,0,0)
lime = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
aqua = (0,255,255)
pink = (255,0,255)
purple = (128,0,128)
red_orange = (255,69,0)

def distance(a,b):
	return mt.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def creat_text(s):
	return font.render(s,True,black)

pygame.init()
screen = pygame.display.set_mode((1100,600)) #set size 
pygame.display.set_caption("Kmeans")
run = True
back = (214,214,214,214)
black = (0,0,0)
panel = (249,255,230)
clock = pygame.time.Clock()
font = pygame.font.SysFont('sans',40)
k = 0
error = 0
font_small = pygame.font.SysFont('sans',15)
points = []
clusters = []
colors = [red,lime,blue,yellow,aqua,pink,purple,red_orange]
labels = []

while (run):
	clock.tick(60) #set FPS
	screen.fill(pink) 

	#draw panel HCN 
	pygame.draw.rect(screen,yellow,(50,50,700,500))
	pygame.draw.rect(screen,panel,(55,55,690,490))

	#K values
	text_k = font.render("K = " + str(k),True,black)
	screen.blit(text_k,(1000,50))

	#error
	error = round(error,3)
	text_e = font.render("Error = " + str(error),True,black)
	screen.blit(text_e,(850,305))

	#add a center
	pygame.draw.rect(screen,yellow,(850,50,40,40))
	screen.blit(creat_text('+'),(860,50))

	#delete a center
	pygame.draw.rect(screen,yellow,(925,50,40,40))
	screen.blit(creat_text('-'),(938,50))

	#run Kmeans buoc 4
	pygame.draw.rect(screen,yellow,(850,135,100,50))
	screen.blit(creat_text('Run'),(860,135))

	#random K center buoc 1
	pygame.draw.rect(screen,yellow,(850,220,150,50))
	screen.blit(creat_text('Random'),(860,220))

	#algo
	pygame.draw.rect(screen,yellow,(850,390,160,50))
	screen.blit(creat_text('Algorithm'),(860,390))

	#reset
	pygame.draw.rect(screen,yellow,(850,475,150,50))
	screen.blit(creat_text('Reset'),(860,475))
	mou_x, mou_y = pygame.mouse.get_pos() #lấy vị trí con chuột đang trỏ tới

	#draw mouse position
	if(50 < mou_x <750 and 50 < mou_y < 550):
		text_m = font_small.render('('+str(mou_x-50)+','+str(mou_y-50)+')',True,black)
		screen.blit(text_m,(mou_x,mou_y))

	for event in pygame.event.get(): #xử lý nút bấm
		if event.type == pygame.QUIT: #tắt màn hình
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if(850 < mou_x < 890 and 50 < mou_y < 90):
				k+=1
			if(925 < mou_x < 965 and 50 < mou_y < 90):
				if(k>0): k-=1
			#run
			if(850 < mou_x < 950 and 135 < mou_y <185):
				if clusters == []:
					continue

				#tìm cluster closet
				labels = []
				for p in points:
					mins = []
					for c in clusters:
						dis = distance(p,c)
						mins.append(dis)
					min_dis = min(mins)
					label = mins.index(min_dis)
					labels.append(label) 

				#cập nhật cluster
				for i in range (k):
					x = 0
					y = 0
					dem = 0
					for j in range (len(points)):
						if(labels[j] == i):
							x += points[j][0]
							y += points[j][1]
							dem+=1
					if dem>0:
						new_x = x/dem
						new_y = y/dem
						clusters[i] = [new_x,new_y]

			#random
			if(850 < mou_x < 1000 and 220 < mou_y <270):
				clusters = []
				labels = []
				for i in range (k):
					cluster = [randint(1,699),randint(1,499)]
					clusters.append(cluster)

			#algo
			if(850 < mou_x < 1010 and 390 <mou_y <440):
				try:
					kmeans = KMeans(n_clusters=k).fit(points)
					clusters = kmeans.cluster_centers_
					labels = kmeans.predict(points)
				except:
					print("Error")

			#reset
			if(850 < mou_x < 1000 and 475 < mou_y < 525):
				k = 0
				error = 0
				points.clear()
				clusters.clear()
				labels.clear()

			#creat point
			if (50 < mou_x <750 and 50 < mou_y < 550):
				labels = []
				point = [mou_x-50,mou_y-50]
				points.append(point)

	#draw cluster
	for i in range (len(clusters)):
		pygame.draw.circle(screen,colors[i],(clusters[i][0]+50,clusters[i][1]+50),10)

	#draw list points
	for i in range(len(points)):
		pygame.draw.circle(screen,black,(points[i][0]+50,points[i][1]+50),6)
		if len(labels) == 0:
			pygame.draw.circle(screen,(255,255,255,255),(points[i][0]+50,points[i][1]+50),5)
		else:
			pygame.draw.circle(screen,colors[labels[i]],(points[i][0]+50,points[i][1]+50),5)
	
	#tính loss funstion
	if len(clusters)>0 and len(labels)>0:
		error = 0
		for i in range(len(points)):
			error += distance(points[i],clusters[labels[i]])
			

	pygame.display.flip() #hiển thị

pygame.quit()
