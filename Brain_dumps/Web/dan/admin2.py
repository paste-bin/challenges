#!/usr/bin/python

import mechanize
import hashlib

import sys

def dump(obj):
  for attr in dir(obj):
	print "obj.%s = %s" % (attr, getattr(obj, attr))
url = "http://testxss.ap-northeast-1.elasticbeanstalk.com/index.php"

br = mechanize.Browser()
# br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # ignore robots
# br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')]

response = br.open(url)

html = response.read()      # the text of the page

br.form = list(br.forms())[1] 
control = br.form.controls[0]
control.value = "SUBJECT2"
# btn = br.form.controls[1]
# req = btn.submit()
req = br.submit()

# print html
# for form in br.forms():
#     print "Form name:", form.name
#     print form
# def is_view_form(form):
# 	print form
# 	return "id" in form.attrs and form.attrs['id'] == "view"

# br.select_form(predicate=is_view_form)

# br.form = list(br.forms())[1] 
# control = br.form.controls[0]
# control.value = "subject2"
# req = br.submit()

	# print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
# # while True:

# # for form in br.forms():
# #     print "Form name:", form.name
# #     print form

# br.select_form(nr=0)
# br.form = list(br.forms())[0] 

# # print html

# # print form
# # print form.click()

# nonceIndex = html.find("$str")
# print html
# # nonce = html[nonceIndex + 7 : nonceIndex + 17]

# exit()
# # print "!!" + nonce + "!!"

# # print form

# #  substr(sha1($pow . $nonce), 0, 5) === '00000'
# # nonce = "6b3ee69656"
# crack = 'Jordan Rocks'
# m = hashlib.sha1(crack + nonce).hexdigest()
# while m.find("00000") != 0:
# 	crack = m
# 	m = hashlib.sha1(crack + nonce).hexdigest()
# # print crack
# # print m

# sql = raw_input("SQL:")



# # form['crack'] = crack
# # form['sql'] = "SELECT current_database()"

# br.form['pow'] = crack
# br.form['sql'] = sql


# req = br.submit()
# html = req.read()
# print html



