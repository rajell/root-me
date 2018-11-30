import requests,base64,re
import pytesseract
import subprocess,Image,string,time

url="http://challenge01.root-me.org/programmation/ch8/"
src="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"
sre=""

r=requests.get(url,data={'cametu':'jksdf'})

print r.cookies
cook=r.cookies
i=0

while(1):
	data=re.findall('data:image/png;base64,(.*) /><br>',r.text)

	sd=base64.b64decode(data[0])
	f=open('img.png','wb')
	f.write(sd)
	f.close()


	tet=pytesseract.image_to_string(Image.open('img.png'))
	r=requests.post(url,data={'cametu':tet},cookies=cook)
	if r.text.find('retente ta chance')!=-1:
		print 'waiting.....',i
	else:
		print r.text
		break;
	i+=1

