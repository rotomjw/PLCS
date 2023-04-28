import os, base64, hashlib, smtplib, ssl, random, time
from email.message import EmailMessage
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

# This is used to check to make sure if the info file which will store the information exists. If not then create it.
def checkexist():
	if os.path.exists("/etc/passwdman/info.txt"):
		pass
	else:
		file = open("/etc/passwdman/info.txt", 'w')
		file.close()

#This is used to make sure the user is who they say they are.
def checkuser():
	#Setting up the email capability
	port = 465
	sender_email = "plcsproject1@gmail.com"
	email_password = "aibpixuxmwmxegag"
	subject = "passwdman code"
	#Get the username and password for the user.
	print("What is your username?")
	name = input("")
	print("What is your password for this manager?")
	passwd = input("")
	passwd = passwd + "\n"
	#Generate the code
	code = random.randint(100000, 999999)
	message = "Hello there this is Passwdman. Your code is " + str(code)
	with open("/etc/passwdman/profile.txt", 'r') as f:
		flist = list(f)
		for line in flist:
			if line == passwd:
				print("That's great.")
			else:
				return 1
	access = 0
	#This not only allows the user to input the email code and even will resend the email.
	while access < 2:
		print("Now please enter your email address so that we can varify that it is you.")
		receiver_email = input("")
		em = EmailMessage()
		em['From'] = sender_email
		em['to'] = receiver_email
		em['subject'] = subject
		em.set_content(message)
		context = ssl.create_default_context()

		#Sets up the smtp server using SSL for security too.
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			server.login(sender_email, email_password)
			server.sendmail(sender_email, receiver_email, em.as_string())
		
		print("Now please enter the code you have received.")
		user_code = int(input(""))
		if user_code == code:
			return 0
		else:
			print("That is incorrect, resending email.")
	print("It seems you could not validate your email please try again when you have checked our email.")
	return 1
	
#This is used to check if an entry in storage already exists.
def checkentry(webname):
	webname = webname + "\n"	
	with open("/etc/passwdman/info.txt", 'r') as info:
		infolist = list(info)
		lines = []
		exist = False
		for line in infolist:
			if line == webname:
				exist = True
				num = infolist.index(line)
				break
			else:
				pass
		if exist == True:
			return 1
		else:
			return 0
		
#This performs AES encryption on the password.
def encrypt(text):
	privatekey = bytes("xxxxxxxxxxxxxxxx", 'utf-8')
	iv = bytes("yyyyyyyyyyyyyyyy", 'utf-8')
	cipher = AES.new(privatekey, AES.MODE_CBC, iv)
	encrypted = cipher.encrypt(pad(text.encode("UTF-8"), AES.block_size))	#Apply the cipher to the text.
	return b64encode(encrypted).decode('utf-8')	
	
#This performs AES decryption on the password.
def decrypt(ciphertext):
	privatekey = bytes("xxxxxxxxxxxxxxxx", 'utf-8')
	iv = bytes("yyyyyyyyyyyyyyyy", 'utf-8')
	ciphertext = base64.b64decode(ciphertext)
	cipher = AES.new(privatekey, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(ciphertext), AES.block_size)	#Make the text decrypted.
	
#This allows the user to add a new entry to storage.
def appendnew():
	print()
	print()
	#Gets the username, password and website name.
	username = input("Please enter the username: ")
	password = input("Please enter the password: ")
	cpassword = encrypt(password)
	website = input("Please enter the website name: ").lower()
	#Check if the entry already exists.
	check = checkentry(website)
	if check == 0:
		file = open("/etc/passwdman/info.txt", 'a')
	
		print()
		print()
		
		file.write("-----------------------------------------\n")
		file.write(username)
		file.write("\n")
		file.write(cpassword)
		file.write("\n")
		file.write(website)
		file.write("\n")
		file.write("-----------------------------------------\n")
		file.close()
	else:
		print("An entry under that website name already exists.")
		
#This allows to user to read the storage file. However, it keeps all the passwords encrypted.
def readpassword():
	file = open("/etc/passwdman/info.txt", 'r')
	content = file.read()
	file.close()
	print(content)
	
#This allows the user to select an entry and then view the username and password for that website.
def passencryption():
	print("Please enter the name of the website you wish to know your details for.")
	webname = input("").lower()
	webname = webname + "\n"
	with open("/etc/passwdman/info.txt", 'r') as info:
		infolist = list(info)
		lines = []
		exist = False
		for line in infolist:
			if line == webname:
				exist = True
				num = infolist.index(line)
				break
			else:
				pass
		if exist == True:
			#Based on the number of the line the user wishes to see then reveal the lines before it.
			username = infolist[num - 2]
			password = decrypt(infolist[num - 1])
			readable_pass = password.decode('utf-8')
			print("Username: ")
			print(username)
			print("Password: ")
			print(readable_pass)
		else:
			print("That website doesn't seem to exist, either try again or view all the entries to check the entered website name.")
		
#This allows the user to change the password to the tool	
def changepasswd():
	print("In this you will chnage the password that you use to enter this password manager.")
	#Checks the old password first for security.
	print("First, just to check please enter your current password.")
	old_pass = input("")
	old_pass = old_pass + "\n"
	f = open("/etc/passwdman/profile.txt", 'r')
	flist = list(f)
	for line in flist:
		if line == old_pass:
			print("Great that's right.")
		else:
			print("Sorry, that is incorrect.")
			optionselector()
	f.close()
	#Lets the user input a new password.
	print("Okay now please enter the new password you'd like to change your current one to.")
	new_pass = input("")
	new_pass = new_pass + "\n"
	f = open("/etc/passwdman/profile.txt", 'w')
	f.write(new_pass)
	f.close()
	
#This allows the user to remove a specific entry from storage.
def removeentry():
	print("Please enter the website name of the entry.")
	webname = input("").lower()
	webname = webname + "\n"
	info = open("/etc/passwdman/info.txt", 'r')
	infolist = list(info)
	lines = []
	exist = False
	for line in infolist:
		if line == webname:
			exist = True
			num = infolist.index(line)
			break
		else:
			pass
	info.close()
	info = open("/etc/passwdman/info.txt", 'w')
	if exist == True:
		#This removes the entry based on the index of the line that matched
		for i in range(len(infolist)):
			if i >= (num - 3) and i < (num + 2):
				pass
			else:
				lines.append(infolist[i])
		for line in lines:
			info.write(line)
	else:
		print("That website doesn't seem to exist, either try again or view all the entries to check the entered website name.")
	info.close()
	
#This allows a user to change an already existing entry.
def modify():
	print("Starting modification.")
	#Removes the entry
	removeentry()
	print("Please enter the details of the entry to be updated.")
	#Lets the user enter the updated details
	appendnew()
	print("Modification complete.")
	
#This allows a user to remove all existing entries.
def removeall():
	print("Removing all entries.")
	info = open("/etc/passwdman/info.txt", 'w')
	info.write(" ")
	info.close()
	
#This is a menu for the tool. To allow the user to navigate to all its features.
def optionselector():
	active = True
	while active == True:
		time.sleep(3)
		print("What would you like to do?")
		print("""
--------------------------------------------
Enter:
1 - Add new entry
2 - View whole file (passwords will be encrypted)
3 - View data for specific website, password visible
4 - Change your password for the password manager
5 - Remove entry
6 - Change entry
7 - Remove all entries
8 - Exit
--------------------------------------------""")
		print("Which option would you like to do?")
		option = input("")
		if option == "1":
			appendnew()
		elif option == "2":
			readpassword()
		elif option == "3":
			passencryption()
		elif option == "4":
			changepasswd()
		elif option == "5":
			removeentry()
		elif option == "6":
			modify()
		elif option == "7":
			removeall()
		elif option == "8":
			active = False
		else:
			print("Not a valid option.")
	
print("Welcome to my Password Manager")
#Introduction to the tool.
BLOCK_SIZE = 16
print("In this program you will be able to store various usernames and passwords to different websites and then retreive them using this program.")
print("Oh and do not worry this password manager is super duper safe so no need to worry about that.")
#Performs a check first before going into the option selector.
print("First enter the user and your personal password.")
check = checkuser()
if check == 1:
	print("Sorry, that is wrong.")
else:
	print("Okay, you passed the test.")
	#Go to the option selector.
	optionselector()

