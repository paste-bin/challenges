#!/usr/bin/python
import hashlib
import sys
import re
from random import randint


class PrintInColor:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    @classmethod
    def red(cls, s):
        print(cls.RED + s + cls.END)

    @classmethod
    def green(cls, s):
        print(cls.GREEN + s + cls.END)

    @classmethod
    def yellow(cls, s):
        print(cls.YELLOW + s + cls.END)

    @classmethod
    def lightPurple(cls, s):
        print(cls.LIGHT_PURPLE + s + cls.END)

    @classmethod
    def purple(cls, s):
        print(cls.PURPLE + s + cls.END)



keys = ["ZeroCool", "flipbox", "sausage", "Pegasus" , "susageP", "chipping_norton", "puzzleQuest", "basement", "K17", "bananarama", "robots", "monkey", "god", "skeletor", "palm_leaves", "helicopters", "more_explosions", "segfault"]
PrintInColor.purple("Welcome to the totally legit authentication service")

#Flag = flynn{_____________999999999944444444445555555555}
# flag = "flynn{n0w_yoU_kNow_hOw_M4Cs_WorK_nice_pRogr4mMing}"

flag = "xkd"
show = flag
# opti = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
opti = "zzz"
garb = "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM1234567890!_"
while len(re.findall('[^z]',show)) > 0:
	print show
	index = randint(0,len(keys) - 1)
	key = keys[index]
	print "At the moment the key is",
	PrintInColor.green(key)
	msg = raw_input(" Enter your message:\033[33m")
	print "\033[0m",
	mac = raw_input("Enter the MAC:")

	if str(hashlib.sha1(keys[index] + msg).hexdigest()) == mac:

		message = ""
		mac = ""
		characterIndex = 0
		s = set(msg)
		t = set(show) - set('z')
		intersect = s & t # or s.intersection(t)

		#they have input some character that is not been revealed

		if len(intersect) > 0:
			#Tell them something useful
			showIndex = randint(0, len(show) -1 )

			#find something new
			while show[showIndex] == 'z':
				showIndex = randint(0, len(show) -1 )

			#mark it as found
			blob = list(show)
			blob[showIndex] = 'z'
			show = ''.join(blob)

			flagChar = flag[showIndex]
			characterIndex = showIndex + 1

			mac = hashlib.sha1(key + message).hexdigest()
		else:
			#tell them bullshit
			# Print things with the right pronouns
			characterIndex = randint(0, len(garb) -1 )
			flagChar = garb[characterIndex]
			characterIndex = characterIndex%len(flag) + 1
			#garbage
			mac = hashlib.sha1('garbadge' + garb[randint(0, len(garb))]).hexdigest()



		if characterIndex%10 == 1 and characterIndex != 11:
			message = "{0} is the {1}st character of the flag".format(flagChar, characterIndex)
		elif characterIndex%10 == 2 and characterIndex != 12:
			message = "{0} is the {1}nd character of the flag".format(flagChar, characterIndex)
		elif characterIndex%10 == 3 and characterIndex != 13:
			message = "{0} is the {1}rd character of the flag".format(flagChar, characterIndex)
		else:
			message = "{0} is the {1}th character of the flag".format(flagChar, characterIndex)


		print "\033[91m#\033[92m#\033[93m#\033[0m" + message + "\033[93m#\033[92m#\033[91m#\033[0m"
		PrintInColor.lightPurple("Our communications could be intercepted and modified")
		PrintInColor.lightPurple("check the following MAC against the current key")
		print mac
		print "Note: only the message inside ",
		print "\033[91m#\033[92m#\033[93m#  \033[93m#\033[92m#\033[91m#\033[0m",
		print "is included in the mac hash\n"
	else:
		PrintInColor.red("Spys detected! Tinfoil Hats, ACTIVATE!")
		PrintInColor.lightPurple("Hint: the MAC (Message Authentication Code) == sha1(key+message)")
		exit()


