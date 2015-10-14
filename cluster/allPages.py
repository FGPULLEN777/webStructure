from page import Page
import os
import math

class allPages:
	def __init__(self,path_list):
		self.pages = []
		self.category = []
		self.full_xpaths = []
		self.idf = {}
		self.addPages(path_list)
		self.expandXpaths()
		self.updateidf()
		self.updatetfidf()
	
	def update_full_xpaths(self,_page_):
		for xpath in _page_.xpaths.keys():
			if xpath not in self.full_xpaths:
				self.full_xpaths.append(xpath)

	def addPages(self,folder_path_list):
		category_num = 0
		for folder_path in folder_path_list:
			folder_pages = []
			for html_file in os.listdir(folder_path):
				if ".DS_Store" not in html_file:
					file_path = folder_path + html_file
					file_page = Page(file_path)
					# the same number for pags & category
					self.pages.append(file_page)
					self.category.append(category_num)
					self.update_full_xpaths(file_page)
			category_num+=1

	def expandXpaths(self):
		for page in self.pages:
			page.expandXpaths(self.full_xpaths)

	def updateidf(self):
		N = len(self.pages)
		# initiate
		for xpath in self.full_xpaths:
			self.idf[xpath] = 0
		# count document frequency
		for page in self.pages:
			for xpath in self.full_xpaths:
				if page.xpaths[xpath] !=0:
					self.idf[xpath] +=1
		# log(n/N)
		for xpath in self.full_xpaths:
			self.idf[xpath] = math.log((float(N))/(float(self.idf[xpath])),2)


	def updatetfidf(self):
		for page in self.pages:
			page.updatetfidf(self.idf)

if __name__=='__main__':
	UP_pages = allPages(["../Crawler/toy_data/users/","../Crawler/toy_data/questions/"])
	count_zero = 0
	count_one = 0
	for item in UP_pages.category:
		if item == 0:
			count_zero+=1
		elif item == 1:
			count_one+=1
	print "users group has " + str(count_zero)
	print "questions group has " + str(count_one)	
	#for page in UP_pages.pages:
	#	print len(page.xpaths)
	#page_example = UP_pages.pages[0]
	#page_example.outputtfidf()
