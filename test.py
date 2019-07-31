from selenium import webdriver
import time
import sys
class Rekord:
	typ=""
	host=""
	dane=""
	ttl=""



print (sys.argv)
driver=  webdriver.PhantomJS()
driver.get('https://cp.home.pl')
time.sleep(5)

driver.find_element_by_name("user").send_keys(sys.argv[1])

driver.find_element_by_name("password").send_keys(sys.argv[2])
driver.find_element_by_name("login").click()

time.sleep(10)
driver.find_element_by_id("http://www.parallels.com/ccp-domains#domainsapp-navigation").click()
time.sleep(10)
driver.switch_to.frame("http://www.parallels.com/ccp-domains")  #tak korzystają z ramki do parallels






ile=len(driver.find_elements_by_xpath("/html/body/div/div/div[4]/div/div/div[2]/table/tbody/tr"))


print(ile)
for i in range(1, ile+1):


	rekordy=[]
	ns=[]
	text= '$TTL 86400\n'
	print(driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[1]").text)
	domain_name= driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[1]").text
	logfile = open(domain_name, 'w')
	domain_name= driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[1]").text
	text+= '$ORIGIN  '+domain_name+'.\n'
	driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[1]").click()
	time.sleep(5)

	try:

		pom_dns=driver.find_element_by_xpath('//*[@id="viewDomain_di_domainNameservers"]').text
		w_dns=pom_dns.split('\n')
		for dns in w_dns:
			ns.append(dns)
		text+='@		IN		SOA     '+ns[0]+'. root.example.net. (\n'
		text+='			2004022300	;; serial\n'
		text+='			1200		;; refresh\n'
		text+='			1200		;; retry\n'
		text+='			2419200    ;; expire\n'
		text+='			86400	   ;; TTL\n'
		text+='        )\n'
		for rek in ns:
			text+='@               IN      NS      '+rek+'. \n'

	except:
		try:
			time.sleep(15)
			pom_dns=driver.find_element_by_xpath("/html/body/div/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div/div/div/div/p").text
			w_dns=pom_dns.split('\n')
			for dns in w_dns:
				ns.append(dns)
			text+='@		IN		SOA     '+ns[0]+'. root.example.net. (\n'
			text+='			2004022300	;; serial\n'
			text+='			1200		;; refresh\n'
			text+='			1200		;; retry\n'
			text+='			2419200    ;; expire\n'
			text+='			86400	   ;; TTL\n'
			text+='        )\n'
			for rek in ns:
				text+='@               IN      NS      '+rek+'. \n'



		except:
			print("dns prob")
	try:
		url=driver.current_url
		pom=url.split("/")
		link="https://cp.home.pl/ccp/v/pa/ccp-domains/dnsRecords/r/"+pom[-1]
		print(link)
		driver.get(link)
		time.sleep(15)
		driver.switch_to.frame("http://www.parallels.com/ccp-domains")
		ile2=len(driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr"))
		print(ile2)
		w_domain = domain_name.split('.')
		for i in range(1, ile2+1):
			try:



				typ= driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[2]").text
				host= driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[3]").text
				dane= driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[1]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[4]").text
				#if host == domain_name :
				#	host="@"
				#else:
				hos= host.split('.')
				if hos[0]== w_domain[0] :
					text+= "@			IN		"+typ+"	"+dane+"\n"
				else:
					text+= hos[0]+"			IN		"+typ+"	"+dane+"\n"

			except:
				print("problem z pobraniem wpisu domeny ")

	except:
		print("nie ma rekordów")
	driver.switch_to.default_content()
	driver.find_element_by_id("http://www.parallels.com/ccp-domains#domainsapp-navigation").click()
	time.sleep(10)
	driver.switch_to.frame("http://www.parallels.com/ccp-domains")
	logfile.write(text)
	logfile.close()
#driver.stop_client()
#driver.close()
