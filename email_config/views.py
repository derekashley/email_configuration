from .models import Reports
from .models import EmailReports
from django.http import JsonResponse
from django.db import connection
from rest_framework.parsers import JSONParser 
import pandas as pd
import json
import datetime
from .import managment_reports
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import io
import pandas as pd
import psycopg2
current_date = datetime.datetime.today().date()	
yesterday = current_date.replace(day=1)	

def add_email_request(request):
	try:
		if request.method == 'POST':
			data = JSONParser().parse(request)
			if data is not None:
				for dat in data:
					b = EmailReports(reports_id=dat['reports_id'],customer_id=dat['customer_id'],frequency=dat['frequency'], email_id=dat['email_id'])
					b.save()
			json_output = json.loads('{"success":"true", "message":"success" }')

	except Exception as e:
		#print(e)
		json_output = json.loads('{"success":"false", "message":"unsuccessful","reason":str(%s) }'%(e))
	
	return JsonResponse(json_output)


def all_reports(request):
	try:
		if request.method == 'GET':
			all_reports = Reports.objects.filter().values()
			all_reports = pd.DataFrame(all_reports)
			json_output = json.loads('{"data":[],"success":"true", "message":"success" }')
			json_output['data']=json.loads(all_reports.to_json(orient='records'))
			return JsonResponse(json_output)
		
		elif request.method == 'POST':
			data = JSONParser().parse(request)
			if data is not None:
				for dat in data:
					b = Reports(reports_name=dat['reports_name'],reports_description=dat['reports_description'])
					b.save()
			json_output = json.loads('{"success":"true", "message":"success" }')
			return JsonResponse(json_output)
	except Exception as e:
		json_output = json.loads('{"success":"false", "message":"unsuccessful","reason":str(%s) }'%(e))
		


def export_excel(df):
	with io.BytesIO() as buffer:
		with pd.ExcelWriter(buffer) as writer:
			df.to_excel(writer)
	return buffer.getvalue()

def export_csv(df,df_columns):
	with io.StringIO() as buffer:
		df = pd.DataFrame(df,columns=df_columns)
		#print(df)
		df.to_csv(buffer, index=False)
		return buffer.getvalue()

#'dataframe.csv': export_csv,

def send_dataframe(send_to, subject, body, df):
	SEND_FROM = 'misfleet.hyd@nittsu.in'
	SENDER_PASSWORD = 'nein*0001'

	multipart = MIMEMultipart()
	multipart['From'] = SEND_FROM
	multipart['To'] = send_to
	multipart['Subject'] = subject
	for filename in EXPORTERS:    
		attachment = MIMEApplication(EXPORTERS[filename](df))
		attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
		multipart.attach(attachment)
		part1 = MIMEText(body, "plain")
		multipart.attach(part1)

	server = smtplib.SMTP('smtp.nittsu.in:587')
	server.ehlo()
	server.starttls()
	server.login(SEND_FROM, SENDER_PASSWORD)
	server.sendmail(SEND_FROM, send_to, multipart.as_string())
	server.quit()

try:
	conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
	cur1 = conn1.cursor()
	total_trips=""" select email_reports.name,reports.reports_name,reports.reports_id,email_reports.customer_id,email_reports.frequency,email_reports.email_id
	 from email_reports join reports on reports.reports_id = email_reports.reports_id where frequency = 'daily'
		""".format(yesterday)
	cur1.execute(total_trips)
	result = cur1.fetchall()
	result=pd.DataFrame(result,columns=["name","reports_name","report_id","customer_id","frequency","email_id"])
		#print(result)
	
	
	#send_to = ['derek.ashley@transo.in']
	#send_to = ["shanthala@transo.in","jayanta.km@nittsu.co.in",'jeo.joseph@nittsu.co.in','kishan.gowda@nipponexpress.com',"dhananjeyans@tupperware.com","praveenkumarbandaru@tupperware.com","derek.ashley@transo.in"]
	send_to = list(result['email_id'])
	

except Exception as e:
	print(e)
	conn1.rollback()
else:
	conn1.commit()
finally:
	cur1.close()
	conn1.close()

for i in result.index:

	subject = '{} from {} to {}'.format(result.loc[i,"reports_name"],yesterday.strftime("%d-%m-%Y"),current_date.strftime("%d-%m-%Y"))	
	#my_dict = '{"%s.csv": export_csv}'%(result.loc[i,"reports_name"])
	EXPORTERS = {"report.csv": export_csv}
	body = """Please find the attachment of the {} Report from the date {} to {}""".format(result.loc[i,"reports_name"],yesterday.strftime("%d-%m-%Y"),current_date.strftime("%d-%m-%Y"))	

	receiver_name = str(result.loc[i,"reports_name"])#.split("@", 1)[0]
	receiver_name = str.title(receiver_name)#.replace("."," "))
	my_func = globals()[result.loc[i,"reports_name"]]
	df_result = managment_reports.my_func(current_date,current_date)

	if result is not None:
		print("--------------------------------------",len(df_result))
		send_dataframe(str(result.loc[i,"reports_name"]),subject,body,df_result)

