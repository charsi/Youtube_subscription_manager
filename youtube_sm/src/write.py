import time
import os

from .time import since
from .tools import print_debug

class Write_file():
	def __init__(self, output='sub.html', path_cache='', mode='html', method='0'):
		if output != '':
			self.output = output
		else:
			if mode == 'html':
				self.output = 'sub.html'
			elif mode == 'list':
				self.output = 'sub_list'
			elif mode == 'raw':
				self.output = 'sub_raw'
			elif mode == 'view':
				self.output = 'sub_view'
			elif mode == 'json':
				self.output = 'sub.json'
			else:
				self.output = 'sub'
		self.mode = mode
		self.method = method
		self.path_cache = path_cache # The path where the data and the sub are stock

	def write(self, url='', title='', url_channel='', url_img='', channel='', date='', data_file='', view=''):
		"""Write the information in a file"""
		if self.mode == 'html':
			return self.append_html(url, title, url_channel, url_img, channel, date, data_file)
		elif self.mode == 'raw':
			return self.append_raw(url, title, url_channel, url_img, channel, date, data_file)
		elif self.mode == 'list':
			return self.append_list(url, data_file)
		elif self.mode == 'view':
			return self.append_view(view)
		elif self.mode == 'json':
			return self.append_json(title, url, url_channel, channel, date, url_img, view, data_file)

	def json_init(self):
		print_debug('[*] Init json')
		try:
			os.makedirs(self.path_cache + 'data/' + self.mode + '/' + self.method)
		except:
			print_debug('[!] Cache folder already exist or can\'t be create')
			pass
		open(self.output, 'w', encoding='utf8').write('{\n"items" : [\n')

	def html_init(self):
		"""To init the html file"""
		print_debug('[*] Init html')
		try:
			os.makedirs(self.path_cache + 'data/' + self.mode + '/' + self.method)
		except:
			print_debug('[!] Cache folder already exist or can\'t be create')
			pass
		open(self.output, 'w', encoding='utf8').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="css/sub.css" />
		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>
		<title>Abonnements</title>
	</head>
	<body>
		<!-- {} -->""".format(time.ctime()) + """
		<div class="But"><input value="" id="but" type="submit" onclick="lol()"></div>
		<div id="first"></div>
		<script type="text/javascript" src="css/button.js"></script>
		""")

	def append_raw(self, url, title, url_channel, url_img, channel, date, data_file):
		"""Append the informations wich are been recover 
		in the file 'sub_raw'."""
		var = data_file[0] + data_file[1] + '\t' + date + '\t' + url + '\t' + url_channel + '\t' + title + '\t' + channel + '\t' + url_img
		if '\n' in var:
			return False
		open(self.output, 'a', encoding='utf8').write(var + '\n')
		var = ""
		return True

	def append_list(self, url, data_file):
		""""Append the informations wich are been recover
		in the file 'sub_raw'. The date is add to sort the
		videos, but it's deleted"""
		var = data_file[0] + data_file[1] + ' ' + url
		if not '\n' in var:
			open(self.output, 'a', encoding='utf8').write(var + '\n')
			return True
		else:
			return False

	def append_view(self, view):
		""" Write the views in a file"""
		if view != None:
			open(self.output, 'a', encoding='utf8').write(view + '\n')

	def append_html(self, url, title, url_channel, url_img,  channel, date, data_file):
		"""Append the informations wich are been recover
		in a file in '.../data/[date]/.' """
		try:
			data = open(self.path_c(data_file, False), 'rb+').read().decode("utf8")
			if url in data:
				return False
		except:
			try:
				os.mkdir(self.path_c(data_file, True))
			except:
				pass
		open(self.path_c(data_file, False), 'a', encoding='utf-8').write("""<!--NEXT -->
		<div class="video">
			<a class="left" href="{}"> <img src="{}" ></a>
			<a href="{}"><h4>{}</h4> </a>
			<a href="{}"> <p>{}</p> </a>
			<p>{}</p>
			<p class="clear"></p>
		</div>\n""".format(url, url_img, url, title, url_channel, channel, date))
		return True

	def append_json(self, title, url, url_channel, channel, date, url_img, view, data_file):
		try:
			data = open(self.path_c(data_file, False), 'rb+').read().decode("utf8")
			if url in data:
				return False
		except:
			try:
				os.mkdir(self.path_c(data_file, True))
			except:
				pass
		open(self.path_c(data_file, False), 'a', encoding='utf8').write("{" + """
	"title": "{}",
	"id": "{}",
	"idChannel": "{}",
	"uploader": "{}",
	"uploaded": "{}",
	"image": "{}",
	"views": "{}"\n""".format(title, url, url_channel, channel, date, url_img, view) + "}\n")

	def path_c(self, data_file, folder=True):
		if folder:
			return '{}data/{}/{}/{}/'.format(self.path_cache, self.mode, self.method, data_file[0])
		else:
			return '{}data/{}/{}/{}/{}'.format(self.path_cache, self.mode, self.method, data_file[0], data_file[1])

	def sort_file(self, count=7):
		""" To sort the videos by date or add the videos in the file"""
		if self.mode == 'html' or self.mode == 'json':
			self.html_json_end(count)
		elif self.mode == 'list' or self.mode == 'raw':
			self.raw_list_end(count)

	def html_json_end(self, count=7, play=True):
		"""Recover the file in '.../data/.' with all the
		informations, sort by date and add the informations
		in './sub.html'. """
		print_debug('[*] Start sort of {}'.format(self.mode))
		first = True
		fch = sorted(os.listdir(self.path_cache + 'data/' + self.mode + '/' + self.method + '/'))
		if len(fch) < count:
			date = 0
		elif count == -1:
			date = -1
		else:
			date = int(since(count)[:8])
		sub_file = open(self.output, 'a', encoding='utf-8')
		i = -1
		while True:
			i += 1
			try:
				folder_date = int(fch[-1-i])
			except IndexError:
				break
			except:
				if play:
					folder_date = 0
				else:
					continue
			if folder_date > date:
				fch_in = sorted(os.listdir(self.path_cache + 'data/' + self.mode + '/' + self.method + '/' + fch[-1-i]))
				for a in range(len(fch_in)):
					data = open(self.path_cache + 'data/' + self.mode + '/' + self.method + '/' + fch[-1-i] + '/' + fch_in[-1-a], 'r', encoding='utf-8').read()
					if first == False and self.mode == 'json':
						sub_file.write(',')
					else:
						first = False
					sub_file.write(data)
		sub_file.close()
		if self.mode == 'html':
			open(self.output, 'a').write('</body></html>')
		elif self.mode == 'json':
			open(self.output, 'a').write(']}')

	def raw_list_end(self, count=7):
		"""Sorted the videos by date"""
		print('[*] Start sort of {}'.format(self.mode))
		try:
			linfo = sorted(open(self.output, 'rb').read().decode('utf8').replace('\r', '').split('\n'))
		except FileNotFoundError:
			return 
		fichier = open(self.output, 'w', encoding='utf8')
		if count == -1:
			date = -1
		else:
			date = int(since(count)[:8])
		i = -1
		while True:
			i += 1
			try:
				folder_date = int(linfo[-1-i][:8])
			except IndexError:
				break
			except:
				continue
			if folder_date > date:
				fichier.write(linfo[-1-i][15:] + '\n')
			else:
				break

def write_css(arg):
	if arg == '' or arg == 'light' or arg[0] == '-':
		open('css/sub.css', 'w').write(':root {\n	--Back: white;\n	--DivHover : #e9edf3;\n	--Div: white;\n	--ColorH4: black;\n	--ColorP: grey;\n	--ColorBut: #e2e5e9;\n 	--HeightBut: 0px;\n	--HeightButMob: 0px }\n')
	elif arg == 'dark':
		open('css/sub.css', 'w').write(':root {\n	--Back: #181a1d;\n	--DivHover : #1c1e21;\n	--Div: #26292e;\n	--ColorH4: #dcdddf;\n	--ColorP: grey;\n	--ColorBut: #e2e5e9;\n	--HeightBut: 0px;\n	--HeightButMob: 0px }\n')
	elif arg == 'switch':
		open('css/button.js', 'w').write('function lol() {\n	if (lel == "1") {\n		document.documentElement.style.setProperty("--Back", "#181a1d");\n		document.documentElement.style.setProperty("--Div", "#1c1e21");\n		document.documentElement.style.setProperty("--DivHover", "#26292e");\n		document.documentElement.style.setProperty("--ColorH4", "#dcdddf");\n		document.documentElement.style.setProperty("--ColorP", "grey");\n		document.documentElement.style.setProperty("--ColorBut", "#292c30");\n		document.cookie = "lel=1";\n		lel = "2"\n	} else if (lel == "2"){\n		document.documentElement.style.setProperty("--Back", "white");\n		document.documentElement.style.setProperty("--Div", "white");\n		document.documentElement.style.setProperty("--DivHover", "white");\n		document.documentElement.style.setProperty("--ColorH4", "black");\n		document.documentElement.style.setProperty("--ColorP", "grey");\n		document.documentElement.style.setProperty("--ColorBut", "#e2e5e9");\n		document.cookie = "lel=2";\n		lel = "1"} }\ndocument.documentElement.style.setProperty("--HeightBut", "25px");\ndocument.documentElement.style.setProperty("--HeightButMob", "50px");\nif (document.cookie == ""){	var lel = "1"\n} else { lel = document.cookie.replace("lel=", "")}\nlol();')
		open('css/sub.css', 'w').write(':root {\n	--Back: white;\n	--DivHover : #e9edf3;\n	--Div: white;\n	--ColorH4: black;\n	--ColorP: grey;\n	--ColorBut: #e2e5e9;\n 	--HeightBut: 0px;\n	--HeightButMob: 0px }\n')
	else:
		exit('[!] No such argument: ' + arg)
	open('css/sub.css', 'a').write('.left { float: left; }\n.clear { clear: both; }\n* { font-family: Arial;}\n\nbody {\n	margin: 0 0 0 0;\n	background-color: var(--Back);}\n\n.But {\n	width: 100%;\n	position: fixed;}\n\n#but {\n	-webkit-appearance: none;\n	border: none;\n	background-color: var(--ColorBut);\n	width: 100%;\n	height: var(--HeightBut); }\n\n#first{\n	margin: 0 27% 0 27%;\n	height: var(--HeightBut); }\n\ndiv.video:hover{ \n	background-color: var(--DivHover); }\n\ndiv.video {\n	background-color: var(--Div);\n	margin: 5px 27% 5px 27%; }\n\nimg {\n	width: 280px;\n	height: 157px;\n	margin-right: 5px; }\n\nh4 {\n	color: var(--ColorH4);\n	line-height: 18px;\n	font-size: 18px;\n	margin: 0px 0px -5px 0px; }\n\np {\n	color: var(--ColorP);\n	line-height: 7px; }\n\na{\n	text-decoration: none;\n	color: black; }\n')
	open('css/sub_mobile.css', 'w').write('.left { float:left; }\n.clear { clear: both; }\n* { font-family: Arial; }\n\n\n#But{\n	margin: 0 0 0 0;\n	position: fixed;\n	width: 100%;\n}\n\n#but {\n	height: var(--HeightButMob);\n	margin: 0 0 0 0;}\n\n#first{\n	margin: 0 0 0 0;\n	width: 100%;\n	height: var(--HeightButMob);\n}\ndiv.video {\n	margin-left: 0%;\n	margin-right: 0%;\n	margin: 10px 10px 10px 10px; }\n\nimg {\n	width: 380px;\n	height: 214px; }\n\nh4 {\n	line-height: 30px;\n	font-size: 30px;\n	margin: 0px 0px -10px 0px; }\n\np {\n	color: grey;\n	line-height: 5px;\n	font-size: 1.9em; }\n\na {\n	text-decoration: none;\n	color: black; }\n')

def write_log(arg, path, passe):
	var = ''
	for i in arg:
		var += i + ' '
	open(path + 'log', 'a', encoding='utf8').write(time.strftime("%H%M") + '\t' + str(time.time() - passe)[:4] + '\t' + var + '\n')

