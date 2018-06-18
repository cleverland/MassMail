#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import logging


campaign = "mc1"
subject = "Aké finty používajú obstarávatelia"
mailgrp = "Domains"
# Logging
class ContextFilter(logging.Filter):
	def filter(self, record):
		record.count = counter
		return True


open('mailer_log.html', 'w').close()
logger = logging.getLogger('mailer')
hdlr = logging.FileHandler('mailer_log.html')
logger.addFilter(ContextFilter())  # Add logger filter for showing counter
formatter = logging.Formatter('%(count)s: %(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Import TEXT only File as Body
t = open('textmsg.txt', 'r')
tmsgfile = t.read()
# Import HTML only File as Body
h = open('htmlmsg.txt', 'r')
hmsgfile = h.read()
# Import E-Mail addresses from file. Separate mail@ddress per line
addr_f = open('mails.txt', 'r')
# This is as second log and it store only emails
addr_s = open('sent.txt', 'a')
addr_list = []

for line in addr_f:
	addr_list.append(str((line).replace("\n", "")))
# addr_list.sort() #Don't sort if you want to remove lines if unexpected error will occur
print addr_list
print "\nE-Mails count : ", len(addr_list)

# Pick Up email recipient from list and send email to address
counter = 1
logger.info("Number of emails : " + str(len(addr_list)))
for mail in addr_list:
	try:
		# From which Email address 
		from_mail = formataddr((str(Header('www.mydomain.sk', 'utf-8')), 'info@mydomain.sk'))
		to_mail = mail  # E-Mail address from list

		msg = MIMEMultipart('alternative')
		msg['Content-Type'] = "text/html; charset=utf-8"
		msg['Subject'] = Header(subject, 'utf-8')
		msg['From'] = from_mail
		msg['To'] = to_mail

		# Send plaintext version of this mail because of old email clients
		text = tmsgfile
		# Send HTML formatted email body with rewriting unsubscribe link for 
		html = hmsgfile.replace('useremail', mail).replace('mailcamp', campaign).replace('mailgroup',mailgrp)
		part1 = MIMEText(text, 'plain', "utf-8")
		part2 = MIMEText(html, 'html', "utf-8")

		msg.attach(part1)
		msg.attach(part2)

		s = smtplib.SMTP('smtp.websupport.sk:25')  # SMTP server DNS (or IP) and Port
		s.starttls()  # Use TLS
		s.login('info@mydomain.sk', 'my_pass')  # Username and Password
		s.sendmail(from_mail, to_mail, msg.as_string())
		logger.info("Sent to : " + mail)  # Log info message about success email sent
		addr_s.write(mail + "\n") # Write email to another file for analysis

		# Print which is processed
		print "\n", counter, "Message sent to :", mail
		time.sleep(1)  # Sleep some second between mails to send
		counter += 1
	except:
		print "\n", counter, "Error in sending email to recipient %s." % mail  # Print Error message but process next mail
		logger.warning("SMTP Error : " + mail)  # Log info message about error in sending
		addr_s.write(mail + "\n") # Write email to another file for analysis
		counter += 1

s.quit()
logger.info("Sending Finished")
print "\nFinish"



#########################
## Example htmlmsg.txt ##
#########################

<!DOCTYPE html>
<html lang="sk_SK">
<meta charset="utf-8">
<html>
<head>
</head>
<body>
<p>Testing EMD

<p style="padding-left: 30px;">•	Point 1.</p>
<p style="padding-left: 30px;">•	Point 2</p>
<p style="padding-left: 30px;">•	Point 3</p>
<p style="padding-left: 30px;">•	Point 4</p>
<p style="padding-left: 30px;">•	Point 5</p><br/>

<p>Testing Testing</p><br/>

<p>Viem, že mnohí ste sa s tým už stretli. Ja len chcem povedať, že ak sa trochu pripravíte budete sa na to dívať ako na akýkoľvek iný obchodný prípad, kde vám chce druhá strana podstrčiť svoje podmienky, tak tie nezrovnalosti uvidíte tiež a hneď sa môžete pýtať a žiadať nápravu. Ktovie, možno to bude Váš prvý veľký „kšeft“.</p><br/>

<p>Volám sa Martin Kolesár a verejné obstarávanie riešim <a href="http://www.abc.com/mailcamp">jednoducho a prakticky</a>. V tomto duchu som pripravil aj príručku, ktorá Vám ozrejmí celé verejné obstarávanie tak ako v skutočnosti prebieha krok za krokom a keď tomu budete rozumieť, už nebudete mať pocit bezmocnosti ale budete vidieť svoje príležitosti.</p>
<p></p><br/>
<p>Príručku Verejné obstarávanie jednoducho a prakticky si môžete objednať na stránke <a href="http://voprakticky.sk/mailcamp">voprakticky.sk</a> kde nájdete aj ďalšie informácie o verejnom obstarávaní.</p>
<p></p><br/>
<p>Robme veci jednoduchšie,</p>
<p> </p><br/>
<p>Ing. Martin Kolesár</p>
<p></p><br/>
<p>tel.: <a style="color: #1155cc;" href="tel:0918%20370%20498" target="_blank">0918 370 498</a></p>
<p>e-mail: <a style="color: #1155cc;" href="mailto:info@mailcamp.io" target="_blank">info@mailcamp.io</a></p>
<p>web: <a style="color: #1155cc;" href="http://www.mailcamp.io/mailcamp" target="_blank">www.mailcamp.io</a></p>
<br/>
<center><p>Želáte si aj nadalej dostávať e-maily od nás? <strong><a style="color: #1155cc;" href="http://mailcamp.io/email/registracia.php?email=useremail&amp;kampan=mailcamp&amp;grp=mailgroup" target="_blank">Ano</a> / </strong><a style="color: #1155cc;" href="http://voprakticky.sk/email/index.php?email=useremail&amp;kampan=mailcamp&amp;grp=mailgroup" target="_blank">Nie</a></p>
<p>V prípade, že nie budete vyradený z našej databázy.</p></center>