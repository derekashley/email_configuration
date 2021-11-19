import pandas as pd
import json
from numpy import nan
import psycopg2
import logging
from urllib.request import urlopen


def getplace(lat, lon):
	url = "http://maps.googleapis.com/maps/api/geocode/json?"
	url += "latlng=%s,%s&sensor=false" % (lat, lon)
	v = urlopen(url).read()
	j = json.loads(v)
	components = j['results'][0]['address_components']
	country = town = None
	for c in components:
		if "country" in c['types']:
			country = c['long_name']
		if "postal_town" in c['types']:
			town = c['long_name']
	return town, country

def p_l_report(from_date,to_date):
	try:
		
		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query1='''
		select * from 
	(select
		branch.branch_name as region,
		warehouse.warehouse_name as branch,
		trip_consignment.customer_lr_number,
		(case when customer_lr_numbers.used_datetime IS NULL then customer_lr_numbers.added_datetime else customer_lr_numbers.used_datetime end)::date as lr_date,
		customer.customer_company as customer,
		source.address_name as from_location,
		drops.address_name as to_location,
		booking_commercial.logistic_booking_type as service,
		trip_consignment.weight as actual_weight,
		shipment_details.charged_shipment_weight as carrier_charged_weight,
		booking_commercial.customer_sub_total,
		booking_commercial.carrier_sub_total,
		(booking_commercial.customer_sub_total - booking_commercial.carrier_sub_total) as p_and_l,
		trip.trip_status as trip_status
	from booking_commercial
	join trip_consignment on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
	inner join vehicle on vehicle_booking_details.vehicle_id = vehicle.id		
	inner join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
	inner join trip on trip.vehicle_booking_details = vehicle_booking_details.id
	join trip_track on trip_track.trip_id = trip.id
	inner join booking on booking.id = vehicle_booking_details.booking_id
	inner join source on booking.source_id = source.id
	inner join drops on booking.final_drop_id = drops.id
	inner join branch on branch.id = booking.branch_id
	 join warehouse on booking.warehouse_id::int = warehouse.id
	inner join shipment_details on booking.final_drop_id = shipment_details.drop_id
	inner join customer on booking_commercial.customer_id = customer.id
	inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id

	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id
	where booking_commercial.logistic_booking_type = 'LTL' and trip_track.status != 'Cancelled'
	UNION
	select
		branch.branch_name as region,
		warehouse.warehouse_name as branch,
		trip_consignment.customer_lr_number,
		(case when customer_lr_numbers.used_datetime IS NULL then customer_lr_numbers.added_datetime else customer_lr_numbers.used_datetime end)::date as lr_date,
		customer.customer_company as customer,
		source.address_name as from_location,
		drops.address_name as to_location,
		booking_commercial.logistic_booking_type as service,
		trip_consignment.weight as actual_weight,
		shipment_details.charged_shipment_weight as carrier_charged_weight,
		booking_commercial.customer_price as customer_sub_total,
		booking_commercial.carrier_price as carrier_sub_total,
		(booking_commercial.customer_price - booking_commercial.carrier_price) as p_and_l,
		trip.trip_status as trip_status
	from booking_commercial
	join trip_consignment on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
	inner join vehicle on vehicle_booking_details.vehicle_id = vehicle.id		
	inner join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
	inner join trip on trip.vehicle_booking_details = vehicle_booking_details.id
	join trip_track on trip_track.trip_id = trip.id
	inner join booking on booking.id = vehicle_booking_details.booking_id
	inner join source on booking.source_id = source.id
	inner join drops on booking.final_drop_id = drops.id
	inner join branch on branch.id = booking.branch_id
	 join warehouse on booking.warehouse_id::int = warehouse.id
	inner join shipment_details on booking.final_drop_id = shipment_details.drop_id
	inner join customer on booking_commercial.customer_id = customer.id
	inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id
	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id
	where booking_commercial.logistic_booking_type = 'FTL' and trip_track.status != 'Cancelled'
	)mytable
	where lr_date BETWEEN '{0}' AND '{1}'
		'''.format(from_date,to_date)
			#print(query)
			cur1.execute(query1)
			result1 = cur1.fetchall()
			
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
		
		result=pd.DataFrame(result1,columns = ['Region', 'branch','customer_lr_number', 'lr_date', 'customer', 'from_location', 'to_location', 'service', 'actual_weight', 'carrier_charged_weight', 'customer_sub_total', 'carrier_sub_total', 'p_and_l','trip_status'])
		print("checking length \n ",len(result))
		#print(result.customer)
			#newdf = result[(result.Region=="{0}") & (result.Branch=="{1}") & (result.customer_name=="{2}") & result.lr_date > '2020-11-10' & result.lr_date : '2020-11-15']
			#filtered_df=result.query(lr_date >= '2020-11-10' )
			#print(newdf)
		filters = result

		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['lr_date']=filters['lr_date'].astype(str)
		print("entering")
		#result = list(filter)
		# df = filters.to_json(orient="records")
		# df = json.loads(df)
		# s = {'cells':df,"success":"true"}
		
		return filters
	except Exception as e:
		print(e)		
		return str(e)




def pod_report(from_date,to_date):
	try:
	
		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
		select * from
	(select 
		branch.branch_name as Region,
		warehouse.warehouse_name as Branch,
		customer.customer_company as customer, 
		trip_consignment.customer_lr_number as lr_number,
		shipment_details.time_stamp::date as lr_date,
		source.address_name as from_location,
		drops.address_name as to_location,
		booking.logistic_booking_type as service,
		to_char(t2.eta,'dd/mm/yyyy') as eta,
		t3.actual_delivery_date,
		(case when shipment_details.customer_pod_copy_link IS NOT NULL then shipment_details.customer_pod_copy_link else 'Not Uploaded' end ) as POD_status,
		trip.trip_status as trip_status

	from trip_track 
	inner join trip on trip.id = trip_track.trip_id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip.vehicle_booking_details
	inner join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
	inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id

	inner join vehicle on vehicle_booking_details.vehicle_id = vehicle.id		
	inner join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
	inner join booking on booking.id = vehicle_booking_details.booking_id
	inner join source on booking.source_id = source.id
	inner join drops on booking.final_drop_id = drops.id
	inner join branch on branch.id = booking.branch_id
	join warehouse on booking.warehouse_id::int = warehouse.id 
	inner join shipment_details on booking.final_drop_id = shipment_details.drop_id
	inner join customer on booking_commercial.customer_id = customer.id

	join
		(
			SELECT 
				booking_commercial.id as booking_commercial_id,
				(t_a.time_stamp::timestamp::date) + make_interval(days => booking_commercial.customer_tat) AS eta
			from trip_consignment
			inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
			inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
			inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
			inner join trip_events t_a on tr.id = t_a.trip_id
			where  t_a.event_id = 4
		)as t2 
	on t2.booking_commercial_id = booking_commercial.id
	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
			inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
			inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
			inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
			inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id
	where trip_track.status != 'Cancelled'
	)mytable
	where lr_date BETWEEN '{0}' AND '{1}';
		'''.format(from_date,to_date)
			#print(query)
			cur1.execute(query)
			result = cur1.fetchall()
			#print(result)
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
			
		#result=pd.DataFrame(result)
		result=pd.DataFrame(result,columns = ["Region",'branch',"customer","lr_number","lr_date","from_location","to_location","service","eta","actual_delivery_date","POD_status","trip_status"])
		print("checking length \n ",len(result))
		#print(result.customer)
			#newdf = result[(result.Region=="{0}") & (result.Branch=="{1}") & (result.customer_name=="{2}") & result.lr_date > '2020-11-10' & result.lr_date : '2020-11-15']
			#filtered_df=result.query(lr_date >= '2020-11-10' )
			#print(newdf)
		filters = result
			
		#filt = 'Region =="{0}"  & customer == "{1}" & branch == "{2}" |Region =="{0}"  & customer == "{1}" '.format(region,customer,branch)
		#filters = result.query(filt)
		#print("checking 1 \n ",result[['Region','customer']])
		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['actual_delivery_date'] = pd.to_datetime(filters['actual_delivery_date']).dt.strftime('%d/%m/%Y')
		filters['eta'] = pd.to_datetime(filters['eta']).dt.strftime('%d/%m/%Y')

		filters['lr_date']=filters['lr_date'].astype(str)
		filters['actual_delivery_date']=filters['actual_delivery_date'].astype(str)
		filters['eta']=filters['eta'].astype(str)
		return filters
	except Exception as e:
		print(e)
		return str(e)


def annexure_report_invoicing(from_date,to_date):
	try:

		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
		select * from
	(select
	warehouse.warehouse_name as branch,
	booking_commercial.id as booking_commercial_id,	
	booking_commercial.logistic_booking_type as service,
	shipment_details.charged_shipment_weight as customer_charged_weight,
	booking_commercial.customer_price_per_kg,
	booking_commercial.customer_basic_freight,
	booking_commercial.customer_fsc_value,
	booking_commercial.customer_fov_value,
	booking_commercial.customer_docket_charge,
	booking_commercial.customer_oda_value as oda_charges,
	booking_commercial.customer_loading_charge,
	booking_commercial.customer_unloading_charge,
	booking_commercial.customer_other_charge,
	booking_commercial.customer_management_fee,
	(booking_commercial.customer_basic_freight + booking_commercial.customer_fsc_value + booking_commercial.customer_fov_value + booking_commercial.customer_docket_charge + shipment_details.handling_charges + booking_commercial.customer_oda_value  + booking_commercial.customer_loading_charge + booking_commercial.customer_unloading_charge + booking_commercial.customer_other_charge + booking_commercial.customer_management_fee) as sub,
	booking_commercial.customer_sgst,
	booking_commercial.customer_cgst,
	booking_commercial.customer_igst,
	(booking_commercial.customer_basic_freight + booking_commercial.customer_fsc_value + booking_commercial.customer_fov_value + booking_commercial.customer_docket_charge + shipment_details.handling_charges + booking_commercial.customer_oda_value + booking_commercial.customer_loading_charge + booking_commercial.customer_unloading_charge + booking_commercial.customer_other_charge + booking_commercial.customer_management_fee + booking_commercial.customer_sgst + booking_commercial.customer_cgst + booking_commercial.customer_igst) as total,
	branch.branch_name as Region,
	--	warehouse.warehouse_name as Branch,
	customer.customer_company,
	trip_consignment.customer_lr_number,
	trip_consignment.material_quantity as packages,
	trip_consignment.weight as actual_weight,
	shipment_details.time_stamp::date as lr_date,
	source.address_name as from_location,
	drops.address_name as to_location,
	shipment_details.handling_charges as detention_charges,
	shipment_details.invoice_no,
	(case when shipment_details.customer_pod_copy_link IS NOT NULL then shipment_details.customer_pod_copy_link else 'Not Uploaded' end ) as POD_status,
	shipment_details.invoice_value,
	t3.actual_delivery_date,
	one.invoice_date,
	--trip_documents.added_on_datetime::date as invoice_date,
	trip.trip_status as trip_status

	from trip_track 
	inner join trip on trip.id = trip_track.trip_id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip.vehicle_booking_details
	inner join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
	inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id

	inner join vehicle on vehicle_booking_details.vehicle_id = vehicle.id	
	inner join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
	inner join booking on booking.id = vehicle_booking_details.booking_id
	inner join source on booking.source_id = source.id
	inner join drops on booking.final_drop_id = drops.id
	inner join branch on branch.id = booking.branch_id
	join warehouse on booking.warehouse_id::int = warehouse.id 
	inner join shipment_details on booking.final_drop_id = shipment_details.drop_id
	-- inner join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
	inner join customer on booking_commercial.customer_id = customer.id

	left join (select trip_id,added_on_datetime::date as invoice_date from trip_documents where trip_documents.document_type = 'invoice' group by trip_id,added_on_datetime)one on one.trip_id= trip_track.trip_id
	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id
	where trip_track.status != 'Cancelled'

	)mytable
	where lr_date BETWEEN '{0}' AND '{1}';
		
		'''.format(from_date,to_date)
			#print(query)
			cur1.execute(query)
			result = cur1.fetchall()
			#print(result)
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
			
		#result=pd.DataFrame(result)
		result=pd.DataFrame(result,columns = ['branch','booking_commercial_id', 'service', 'customer_charged_weight', 'customer_price_per_kg', 'customer_basic_freight', 'customer_fsc_value', 'customer_fov_value', 'customer_docket_charge', 'oda_charges', 'customer_loading_charge', 'customer_unloading_charge', 'customer_other_charge', 'customer_management_fee', 'sub', 'customer_sgst', 'customer_cgst', 'customer_igst', 'total', 'region', 'customer_name', 'customer_lr_number', 'packages', 'actual_weight', 'lr_date', 'from_location', 'to_location', 'detention_charges', 'invoice_no', 'pod_status', 'invoice_value', 'actual_delivery_date', 'invoice_date','trip_status'])
		print("checking length \n ",len(result))
		#print(result.customer)
			#newdf = result[(result.Region=="{0}") & (result.Branch=="{1}") & (result.customer_name=="{2}") & result.lr_date > '2020-11-10' & result.lr_date : '2020-11-15']
			#filtered_df=result.query(lr_date >= '2020-11-10' )
			#print(newdf)
		filters = result

		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['actual_delivery_date'] = pd.to_datetime(filters['actual_delivery_date']).dt.strftime('%d/%m/%Y')
		filters['invoice_date'] = pd.to_datetime(filters['invoice_date']).dt.strftime('%d/%m/%Y')

		filters['lr_date']=filters['lr_date'].astype(str)
		filters['actual_delivery_date']=filters['actual_delivery_date'].astype(str)
		filters['invoice_date']=filters['invoice_date'].astype(str)
		return filters
	except Exception as e:
		print(e)
		return str(e)


def annexure_report_vendor(from_date,to_date):
	try:
		
		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
		select * from
	(
	select
		
		booking_commercial.id as booking_commercial_id,
		branch.branch_name as region,
		warehouse.warehouse_name as Branch,
		trip_consignment.customer_lr_number,
		shipment_details.time_stamp::date as lr_date,
		-- customer_lr_numbers.customer_lr_number,
		--(case when customer_lr_numbers.used_datetime IS NULL then customer_lr_numbers.added_datetime else customer_lr_numbers.used_datetime end)::date as lr_date,
		carrier_company.company_name as vendor,
		shipment_details.vendor_lr_number,
		shipment_details.vendor_lr_date as vendor_lr_date,
		source.address_name as from_location,
		drops.address_name as to_location,
		booking_commercial.logistic_booking_type as service,
		trip_consignment.material_quantity as packages,
		trip_consignment.weight as actual_weight,
		booking_commercial.carrier_charged_weight,
		booking_commercial.carrier_price_per_kg,
		booking_commercial.carrier_basic_freight,
		booking_commercial.carrier_fsc_value,
		booking_commercial.carrier_fov_value,
		booking_commercial.carrier_docket_charge,
		shipment_details.handling_charges as detention_charges,
		booking_commercial.carrier_oda_value as oda_charges,
		booking_commercial.carrier_loading_charge,
		booking_commercial.carrier_unloading_charge,
		booking_commercial.carrier_other_charge,
		(booking_commercial.carrier_basic_freight + booking_commercial.carrier_fsc_value + booking_commercial.carrier_fov_value + booking_commercial.carrier_docket_charge + shipment_details.handling_charges + booking_commercial.carrier_oda_value  + booking_commercial.carrier_loading_charge + booking_commercial.carrier_unloading_charge + booking_commercial.carrier_other_charge ) as sub,
		booking_commercial.carrier_sgst,
		booking_commercial.carrier_cgst,
		booking_commercial.carrier_igst,
		(booking_commercial.carrier_igst + booking_commercial.carrier_cgst + booking_commercial.carrier_sgst + booking_commercial.carrier_basic_freight + booking_commercial.carrier_fsc_value + booking_commercial.carrier_fov_value + booking_commercial.carrier_docket_charge + shipment_details.handling_charges + booking_commercial.carrier_oda_value  + booking_commercial.carrier_loading_charge + booking_commercial.carrier_unloading_charge + booking_commercial.carrier_other_charge )as total_expense,
		shipment_details.invoice_no,
		shipment_details.invoice_value,
		one.invoice_date,
		(booking_commercial.carrier_igst + booking_commercial.carrier_cgst + booking_commercial.carrier_sgst+shipment_details.invoice_value::numeric) as total_amount,
		trip.trip_status as trip_status
	 
	from trip_track 
	inner join trip on trip.id = trip_track.trip_id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip.vehicle_booking_details
	inner join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
	inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id

	inner join vehicle on vehicle_booking_details.vehicle_id = vehicle.id		
	inner join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
	inner join booking on booking.id = vehicle_booking_details.booking_id
	inner join source on booking.source_id = source.id
	inner join drops on booking.final_drop_id = drops.id
	inner join branch on branch.id = booking.branch_id
	join warehouse on booking.warehouse_id::int = warehouse.id 
	inner join shipment_details on booking.final_drop_id = shipment_details.drop_id
	-- inner join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
	inner join customer on booking_commercial.customer_id = customer.id

	left join (select trip_id,added_on_datetime::date as invoice_date from trip_documents where trip_documents.document_type = 'invoice' group by trip_id,added_on_datetime)one on one.trip_id= trip_track.trip_id

	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id

	where trip_track.status != 'Cancelled'
	)mytable
	where lr_date BETWEEN '{0}' AND '{1}'
	ORDER BY lr_date ;
		
		'''.format(from_date,to_date)
			#print(query)
			cur1.execute(query)
			result = cur1.fetchall()
			#print(result)
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
			
		#result=pd.DataFrame(result)
		result=pd.DataFrame(result,columns = ['booking_commercial_id', 'region','branch', 'customer_lr_number', 'lr_date', 'vendor', 'vendor_lr_number', 'vendor_lr_date', 'from_location', 'to_location', 'service', 'packages', 'actual_weight', 'carrier_charged_weight', 'carrier_price_per_kg', 'carrier_basic_freight', 'carrier_fsc_value', 'carrier_fov_value', 'carrier_docket_charge', 'detention_charges', 'oda_charges', 'carrier_loading_charge', 'carrier_unloading_charge', 'carrier_other_charge', 'sub', 'carrier_sgst', 'carrier_cgst', 'carrier_igst', 'total_expense', 'invoice_no', 'invoice_value', 'invoice_date', 'total_amount','trip_status'])
		print("checking length \n ",len(result))
		#print(result.customer)
			#newdf = result[(result.Region=="{0}") & (result.Branch=="{1}") & (result.customer_name=="{2}") & result.lr_date > '2020-11-10' & result.lr_date : '2020-11-15']
			#filtered_df=result.query(lr_date >= '2020-11-10' )
			#print(newdf)

		filters = result
		

		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['invoice_date'] = pd.to_datetime(filters['invoice_date']).dt.strftime('%d/%m/%Y')

		filters['lr_date']=filters['lr_date'].astype(str)
		filters['invoice_date']=filters['invoice_date'].astype(str)
		
		return filters
	except Exception as e:
		print(e)
		return str(e)


def thc_report(from_date,to_date):
	try:

		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''select * from 
	(
	select
		booking_commercial.logistic_booking_type as service,
		thc_details.branch as region,
		warehouse.warehouse_name as branch,
		thc_details.lr_no,
		thc_details.lr_date::date as lr_date,
		thc_details.thc_number,
		thc_details.vendor as vendor_name,
		thc_details.vendor_code,
		thc_details.thc_creation_time as thc_date,
		thc_details.vehicle_number,
		thc_details.vehicle_type,
		thc_payment_charges.loading_charges,
		thc_payment_charges.final_amount as thc_cost,
		
	--	(case when thc_payments.payment_type = 'Advance' then thc_payments.time_stamp else Null end)as advance_date, 
		--adv.advance_date,
		thc_payment_charges.halting_charges,
		thc_payment_charges.unloading_charges,
		thc_payment_charges.Police_RTO,
		thc_payment_charges.misc_charges,
		(thc_payment_charges.loading_charges+thc_payment_charges.advance_amount+thc_payment_charges.halting_charges+thc_payment_charges.unloading_charges+thc_payment_charges.Police_RTO+thc_payment_charges.misc_charges) as sub_total,
		thc_payment_charges.tds,
		thc_payment_charges.advance_check_no as advance_amount_check_no,
		thc_payment_charges.advance_check_date as advance_amount_check_date,
		-- done --thc_payment_charges.time_stamp::date as advance_amount_check_date,
		thc_payment_charges.advance_amount,
		 (case when thc_payment_charges.advance_check_no is NOT NULL  then thc_payment_charges.advance_amount else Null end) advance_check_amount,
		thc_payment_charges.balance,
		thc_payment_charges.final_check_no as final_amount_check_no,
		--fadv.final_payment_date,
		thc_payment_charges.final_check_date as final_payment_date,
		-- done--(case when thc_payments.payment_type = 'Final' then thc_payment_charges.final_amount else Null end) as amount,
		(case when thc_payments.payment_status = 'Completed' then thc_payment_charges.balance else NULL end)as amount,
		(case when thc_payments.payment_status = 'Completed' then 'THC closed' else 'THC open' end)as remarks,
		trip.trip_status as trip_status
		from thc_masters 
		join trip_track on thc_masters.master_trip_id = trip_track.master_trip_id
		join trip on trip.id = trip_track.trip_id
	 join thc_details on thc_masters.thc_masters_id = thc_details.thc_masters_id
	 join thc_payments on thc_payments.thc_masters_id = thc_masters.thc_masters_id
	 join thc_payment_charges on thc_payment_charges.thc_masters_id = thc_masters.thc_masters_id
	inner join branch on branch.id = thc_masters.branch_id
	join booking on thc_details.drop_id = booking.final_drop_id
	 join trip_consignment on thc_details.drop_id = trip_consignment.drop_id
	 join booking_commercial on trip_consignment.trip_consignment_id = booking_commercial.trip_consignment_id
	 join warehouse on booking.warehouse_id::int = warehouse.id 
	)mytable
		WHERE	 
			lr_date BETWEEN '{0}' AND '{1}'
		ORDER BY lr_date;
		
		'''.format(from_date,to_date)
			##print(query)
			cur1.execute(query)
			result = cur1.fetchall()
			print(result)
			result=pd.DataFrame(result,columns = ['service', 'region','branch', 'lr_no', 'lr_date', 'thc_number', 'vendor_name', 'vendor_code', 'thc_date', 'vehicle_number', 'vehicle_type', 'loading_charges', 'thc_cost', 'halting_charges', 'unloading_charges', 'police_rto', 'misc_charges', 'sub_total', 'tds', 'advance_amount_check_no', 'advance_amount_check_date', 'advance_amount', 'advance_check_amount', 'balance', 'final_amount_check_no', 'final_payment_date', 'amount', 'remarks','trip_status'])
			print("checking length \n ",len(result))
			#print(result.customer)
				#newdf = result[(result.Region=="{0}") & (result.Branch=="{1}") & (result.vendor_name=="{2}") & result.lr_date > '2020-11-10' & result.lr_date : '2020-11-15']
				#filtered_df=result.query(lr_date >= '2020-11-10' )
				#print(newdf)
			filters = result

			filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
			filters['thc_date'] = pd.to_datetime(filters['thc_date']).dt.strftime('%d/%m/%Y')
			#filters['advance_date'] = pd.to_datetime(filters['advance_date']).dt.strftime('%d/%m/%Y')
			filters['advance_amount_check_date'] = pd.to_datetime(filters['advance_amount_check_date']).dt.strftime('%d/%m/%Y')
			filters['final_payment_date'] = pd.to_datetime(filters['final_payment_date']).dt.strftime('%d/%m/%Y')
			
			filters['lr_date']=filters['lr_date'].astype(str)
			filters['thc_date']=filters['thc_date'].astype(str)
			#filters['advance_date']=filters['advance_date'].astype(str)	
			filters['advance_amount_check_date']=filters['advance_amount_check_date'].astype(str)
			filters['final_payment_date']=filters['final_payment_date'].astype(str)
			
		except Exception as e:
			conn1.rollback()
			logging.error("Database connection error")

		finally:
			cur1.close()
			conn1.close()

		return filters
	except Exception as e:
		print(e)
		return str(e)


def lr_report(from_date,to_date):
	try:
		conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
		cur1 = conn1.cursor()
		query='''
select * from 
(
	select booking.with_driver_application,drops.id as drop_id,
	t2.eta as expected,
	trip_consignment.road_distance as tot_kms,
	t3.actual_delivery_date::date as to_date,
	t3.actual_delivery_date::time as actual_delivery_time,
	EXTRACT(DAY FROM (t3.actual_delivery_date - t2.eta)) as delivery_tat,
		trip_track.master_trip_id as trip_id,

	vehicle_booking_details.vehicle_id as vehicle_id,

	t7.start_date,

	branch.branch_name as region,
	warehouse.warehouse_name as branch,
	customer.customer_company,

trip_consignment.customer_lr_number,
trip_consignment.material_quantity as packages,
shipment_details.time_stamp::date as lr_date,
		drops.name as consigneename,

		source.name as consignorname,

		source.address_name as from_location,

		drops.address_name as to_location,
	booking_commercial.logistic_booking_type as service,
	trip_consignment.weight as actual_weight,
	shipment_details.charged_shipment_weight as customer_charged_weight,

	shipment_details.invoice_no,
	shipment_details.invoice_value,
	shipment_details.ewaybillno,
	one.invoice_date,
	thc_details.vehicle_number as vehicle_no,
	thc_details.vehicle_type as model_of_truck,

	thc_details.driver_mobile_no as driver_number,
		booking_commercial.customer_tat as tat,
		t1.unloading_time,
		t1.unloading_date,	
		'' as halting_charges,
		trip.trip_status as trip_status

from trip_track 
inner join trip on trip.id = trip_track.trip_id
inner join vehicle_booking_details on vehicle_booking_details.id = trip.vehicle_booking_details
inner join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id

inner join vehicle on vehicle_booking_details.vehicle_id = vehicle.id		
inner join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
inner join booking on booking.id = vehicle_booking_details.booking_id
inner join branch on branch.id = booking.branch_id
join warehouse on booking.warehouse_id::int = warehouse.id 
inner join shipment_details on booking.final_drop_id = shipment_details.drop_id
inner join customer on booking_commercial.customer_id = customer.id
left join thc_masters on thc_masters.master_trip_id = trip_track.master_trip_id
left join thc_details on thc_masters.thc_masters_id = thc_details.thc_masters_id
left join (select trip_id,added_on_datetime::date as invoice_date from trip_documents where trip_documents.document_type = 'invoice' group by trip_id,added_on_datetime)one on one.trip_id= trip_track.trip_id
inner join source on booking.source_id = source.id
inner join drops on trip_track.drop_id = drops.id
inner join
	(
		SELECT 
			tr.id as trip_id,
			ROUND((EXTRACT(EPOCH FROM(t_b.event_time - t_a.event_time))/3600)::numeric,3) AS unloading_time,
			t_b.event_time::date as unloading_date
		FROM 
			trip_events t_a 
		CROSS JOIN trip_events t_b
		inner join trip tr on 
			tr.id = t_a.trip_id
		where t_b.event_id = 11 and t_a.event_id = 10 and t_a.trip_id = t_b.trip_id and t_a.trip_id = tr.id
	)as t1
on trip.id = t1.trip_id 
join
	(
		SELECT 
			booking_commercial.id as booking_commercial_id,
			(t_a.time_stamp::timestamp::date) AS eta
		from trip_consignment
		inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		inner join trip_events t_a on tr.id = t_a.trip_id
		where  t_a.event_id = 4
	)as t2 
on t2.booking_commercial_id = booking_commercial.id

left join 
	(SELECT booking_commercial.id as booking_commercial_id,
		t_a.event_time AS actual_delivery_date
		from trip_consignment
		inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		inner join trip_events t_a on tr.id = t_a.trip_id
	where t_a.event_id = 12
	)as t3
on t3.booking_commercial_id = booking_commercial.id

inner join 
	(SELECT trip_events.event_time::date as start_date,trip.id
		FROM 
			trip_events  
		join trip on trip.id = trip_events.trip_id
		where trip_events.event_id = 4
	)as t7
on t7.id = trip.id
where trip_track.status != 'Cancelled'
)mytable

WHERE lr_date BETWEEN '{0}' AND '{1}'

	
	'''.format(from_date,to_date)
		#print(query)
		cur1.execute(query)
		result = cur1.fetchall()
		result=pd.DataFrame(result,columns = ['with_driver_application','drop_id','expected','tot_kms','to_date','actual_delivery_time','delivery_tat','trip_id', 'vehicle_id', 'start_date', 'region', 'branch','customer', 'customer_lr_number','packages', 'lr_date', 'consigneename', 'consignorname', 'from_location', 'to_location', 'service', 'actual_weight','customer_charged_weight','invoice_no',  'invoice_value', 'ewaybillno','invoice_date',  'vehicle_no', 'model_of_truck', 'driver_name', 'tat', 'unloading_time', 'unloading_date', 'halting_charges','trip_status'])
		print("checking length \n ",len(result))
		filters = result

		

		#filt = 'region =="{0}"  & customer == "{1}" & branch == "{2}" | region =="{0}"  & customer == "{1}" '.format(region,customer,branch)
		#filters = result.query(filt)
		# print("checking \n ",filters)
	
		# filters['tat'] = filters['tat'].fillna(0)
		# max_columns = int(max(filters['tat'],default=0) + 1)
		# #print("max_columns:",max_columns)
		# #filters['start_date'] = pd.to_datetime(filters['start_date'], format='%Y-%m-%d')
		# ctr = 0
		# for i in range(1,max_columns): # this loop creates columns based on tat and dates are generated 
		# 	name = 'day {0}'.format(i)
		# 	ctr = ctr + 1 #ctr is day count
		# 	filters.insert(ctr, name, "")
		# print(filters.columns)
		# #iteration through eacch row:
		# for row in filters.index:
		# 	tat_val = int(filters.loc[row,'tat'] + 1)
			
		# 	start = filters.loc[row,'start_date']
		# 	dates = []
		# 	dates.append(start)
		# 	for i in range(1,tat_val):
		# 		start = start + datetime.timedelta(days=i)
		# 		print("dates-----------------------------------\n",start)
		# 		dates.append(start) #make it empty in the end
		# 		#print(dates)
		# 	#need to have vehicle_id
			
		# 	set_location_to_col = 1
		# 	try:
		# 		if filters.loc[row,'with_driver_application'] == "TRUE":
		# 			for all_date in dates:
		# 				day_column_num = 'day {0}'.format(set_location_to_col)
		# 				trip_no = filters.loc[row,'trip_id']
		# 				vehicle_id = filters.loc[row,'vehicle_id']
		# 				#print(day_column_num,trip_no,vehicle_id)
						
		# 				query = """ select lat_log from (select lattitude ||','|| longitude as lat_log,location_time::date as dat from waypoints_v_part_{0} where master_trip_id = {1} order by location_time::date desc limit 1)mytable where dat = '{2}' ; """.format(vehicle_id,trip_no,all_date)
		# 				cur1.execute(query)
		# 				wayp_res = cur1.fetchone()
		# 				locations = "{0}".format(wayp_res)
		# 				locations = locations[2:23]
		# 				#print(locations)
		# 				#latlog = '12.982811,77.6385579'
		# 				try:
		# 					#print('getting address')
		# 					address = getplace(locations)
							
		# 				except:
		# 					print('not getting address',vehicle_id,trip_no,locations)
		# 					address = ''
		# 				#pprint(address)
		# 				#print(locations)

		# 				filters.loc[row,day_column_num] = address
		# 				set_location_to_col = set_location_to_col + 1
		# 				if set_location_to_col > filters.loc[row,'tat']:
		# 					#print("entering")
		# 					set_location_to_col = 0 
		# 		else:
		# 			for all_date in dates:
		# 				print("*************************************************************")
		# 				day_column_num = 'day {0}'.format(set_location_to_col)
		# 				trip_no = filters.loc[row,'trip_id']
		# 				vehicle_id = filters.loc[row,'vehicle_id']
		# 				#print(day_column_num)
		# 				query = """ select scanned_location from ltl_shipment_tracking where drop_id = {} and scan_date::date = '{}' """.format(filters.loc[row,'drop_id'],all_date)
		# 				cur1.execute(query)
		# 				address = cur1.fetchone()

		# 				filters.loc[row,day_column_num] = address
		# 				set_location_to_col = set_location_to_col + 1
		# 				if set_location_to_col > filters.loc[row,'tat']:
		# 					#print("entering")
		# 					set_location_to_col = 0 
		# 	except Exception as e:
		# 		print(e)
		# 	dates = []
		
		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['invoice_date'] = pd.to_datetime(filters['invoice_date']).dt.strftime('%d/%m/%Y')
		filters['unloading_date'] = pd.to_datetime(filters['unloading_date']).dt.strftime('%d/%m/%Y')
		filters['to_date'] = pd.to_datetime(filters['to_date']).dt.strftime('%d/%m/%Y')
		filters['start_date'] = pd.to_datetime(filters['start_date']).dt.strftime('%d/%m/%Y')
		filters['expected'] = pd.to_datetime(filters['expected']).dt.strftime('%d/%m/%Y')
		
		filters['lr_date']=filters['lr_date'].astype(str)
		filters['to_date']=filters['to_date'].astype(str)
		filters['start_date']=filters['start_date'].astype(str)
		filters['invoice_date']=filters['invoice_date'].astype(str)
		filters['unloading_date']=filters['unloading_date'].astype(str)
		filters['expected']=filters['expected'].astype(str)


		
		return (filters)
	except Exception as e:
		print(e)
		
		return str(e)
	finally:
		cur1.close()
		conn1.close()


def kpi_report(from_date,to_date):
	try:

		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
	-- KPI Report
	select * from 
		(select 
			branch.branch_name as Region,
			warehouse.warehouse_name as Branch,

		   customer.customer_company as customer,
			trip.id as trip_id,
			trip_consignment.customer_lr_number,
			trip_consignment.material_quantity as packages,
			trip_consignment.weight as actual_weight,


			shipment_details.time_stamp::date as lr_date,
			
			t2.eta::date as expected_date_delivery,
			
			source.address_name as from_location,

			drops.address_name as to_location,

			t3.actual_delivery_date::date,

		shipment_details.charged_shipment_weight as charged_weight,
		booking_commercial.customer_tat as approx_transit_days,
		booking_commercial.logistic_booking_type as service,
		 (case when (booking_commercial.customer_tat - (EXTRACT(DAY FROM (t3.actual_delivery_date - t2.eta))) )::INTEGER < 0 OR (booking_commercial.customer_tat - (EXTRACT(DAY FROM (t3.actual_delivery_date - t2.eta))) )::INTEGER > 1 then 100 else ((booking_commercial.customer_tat - (EXTRACT(DAY FROM (t3.actual_delivery_date - t2.eta))))*100)::INTEGER end) as percentage,

			 

			 shipment_details.invoice_no as invoice_number,
			 shipment_details.invoice_value as invoice_value,
			one.invoice_date,
			--(case when trip_documents.added_on_datetime::date is not null then trip_documents.added_on_datetime::date else null end)as invoice_date,

			carrier_company.company_name as vendor_name,

			 vehicle.regno as vehicle_no,

			 vehicle_attr.model as model_of_truck,

			 EXTRACT(DAY FROM (t3.actual_delivery_date - t2.eta)) as delivery_tat,
			 trip.trip_status as trip_status
		
			
			
		from trip_track 
	inner join trip on trip.id = trip_track.trip_id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip.vehicle_booking_details
	inner join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
	inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id

	inner join vehicle on vehicle_booking_details.vehicle_id = vehicle.id		
	inner join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
	inner join booking on booking.id = vehicle_booking_details.booking_id
	inner join source on booking.source_id = source.id
	inner join drops on booking.final_drop_id = drops.id
	inner join branch on branch.id = booking.branch_id
	join warehouse on booking.warehouse_id::int = warehouse.id 
	inner join shipment_details on booking.final_drop_id = shipment_details.drop_id
	-- inner join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
	inner join customer on booking_commercial.customer_id = customer.id
	left join thc_details on trip_consignment.drop_id = thc_details.drop_id
	left join thc_masters on thc_details.thc_masters_id = thc_masters.thc_masters_id
	left join thc_payment_charges on thc_payment_charges.thc_masters_id = thc_masters.thc_masters_id

	left join (select trip_id,added_on_datetime::date as invoice_date from trip_documents where trip_documents.document_type = 'invoice' group by trip_id,added_on_datetime)one on one.trip_id= trip_track.trip_id

	join
		(
			SELECT 
				booking_commercial.id as booking_commercial_id,
				(t_a.time_stamp::timestamp::date) + make_interval(days => booking_commercial.customer_tat) AS eta
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
			where  t_a.event_id = 4
		)as t2 
	on t2.booking_commercial_id = booking_commercial.id

	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id
	where trip_track.status != 'Cancelled'
	--  
	)mytable
	WHERE
		lr_date BETWEEN '{0}' AND '{1}'
		'''.format(from_date,to_date)
			print(query)
			cur1.execute(query)
			result = cur1.fetchall()
			result=pd.DataFrame(result,columns = ['region','branch','customer', 'trip_id', 'customer_lr_number', 'packages', 'actual_weight', 'lr_date', 'expected_date_delivery', 'from_location', 'to_location', 'actual_delivery_date', 'charged_weight', 'approx_transit_days', 'service', 'percentage', 'invoice_number', 'invoice_value', 'invoice_date', 'vendor_name', 'vehicle_no', 'model_of_truck', 'delivery_tat','trip_status'])
			print("checking length \n ",len(result))
			filters = result

			#filt = 'region =="{0}"  & customer == "{1}" & branch == "{2}" | region =="{0}"  & customer == "{1}" '.format(region,customer,branch)
			#filters = result.query(filt)

			filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
			filters['actual_delivery_date'] = pd.to_datetime(filters['actual_delivery_date']).dt.strftime('%d/%m/%Y')
			filters['expected_date_delivery'] = pd.to_datetime(filters['expected_date_delivery']).dt.strftime('%d/%m/%Y')
			filters['invoice_date'] = pd.to_datetime(filters['invoice_date']).dt.strftime('%d/%m/%Y')

			filters['lr_date'] = filters['lr_date'].astype(str)
			filters['actual_delivery_date'] = filters['actual_delivery_date'].astype(str)
			filters['expected_date_delivery']=filters['expected_date_delivery'].astype(str)	
			filters['invoice_date']=filters['invoice_date'].astype(str)

			
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
		
		return (filters)
	except Exception as e:
		print(e)
		return str(e)


def dsr_report(from_date,to_date):
	try:
		
		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
	select * from 
	(select 
	warehouse.warehouse_name as branch,
	branch.branch_name as Region,
	trip_consignment.customer_lr_number,
	trip_consignment.material_quantity as packages,
	shipment_details.time_stamp::date as lr_date,
	t2.eta as expected_date_delivery,
	customer.customer_company as customer,
	s.from_location,
	t.to_location,
	shipment_details.invoice_no,
	shipment_details.vendor_lr_number,
	shipment_details.vendor_lr_date as vendor_lr_date,
	one.invoice_date,
	-- trip_documents.added_on_datetime::date as invoice_date,
	carrier_company.company_name as vendor_name,
	thc_details.thc_number,
	thc_details.thc_creation_date as thc_date,
	(case when booking_commercial.logistic_booking_type = 'LTL' then thc_details.vehicle_number else vehicle.regno end)as vehicle_number,
	(case when booking_commercial.logistic_booking_type = 'LTL' then thc_details.vehicle_type else vehicle_type.type end)as vehicle_type,
	trip_consignment.weight as actual_weight,
	booking_commercial.carrier_volumetric_weight as volumetric_weight,
	shipment_details.charged_shipment_weight as charged_weight,
	booking_commercial.logistic_booking_type as service,
	(case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end) as customer_basic_freight ,
	booking_commercial.customer_fsc,
	booking_commercial.customer_fov,
	booking_commercial.customer_docket_charge,
	booking_commercial.customer_handing_charge,
	booking_commercial.customer_oda,
	booking_commercial.customer_loading_charge,
	booking_commercial.customer_unloading_charge,
	booking_commercial.customer_other_charge,
	booking_commercial.customer_management_fee,
	(COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end),0)+COALESCE(booking_commercial.customer_fsc,0)+COALESCE(booking_commercial.customer_fov,0)+COALESCE(booking_commercial.customer_docket_charge,0)+COALESCE(booking_commercial.customer_handing_charge,0)+COALESCE(booking_commercial.customer_oda,0)+COALESCE(booking_commercial.customer_loading_charge,0)+COALESCE(booking_commercial.customer_unloading_charge,0)+COALESCE(booking_commercial.customer_other_charge,0)+COALESCE(booking_commercial.customer_management_fee,0)) as sub_total,
	(COALESCE(booking_commercial.customer_sgst,0) + COALESCE(booking_commercial.customer_cgst,0) + COALESCE(booking_commercial.customer_igst,0)) as gst,
	(COALESCE(booking_commercial.customer_management_fee,0)+COALESCE(booking_commercial.customer_other_charge,0)+COALESCE(booking_commercial.customer_unloading_charge,0)+COALESCE(booking_commercial.customer_loading_charge,0)+COALESCE(booking_commercial.customer_oda,0)+COALESCE(booking_commercial.customer_handing_charge,0)+COALESCE(booking_commercial.customer_docket_charge,0)+COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end),0) + COALESCE(booking_commercial.customer_fsc,0) + COALESCE(booking_commercial.customer_fov,0) + COALESCE(booking_commercial.customer_sgst,0) + COALESCE(booking_commercial.customer_cgst,0) + COALESCE(booking_commercial.customer_igst,0))as customer_total_freight,
	booking_commercial.carrier_fsc,
	booking_commercial.carrier_fov,
	booking_commercial.carrier_docket_charge,
	booking_commercial.carrier_oda,
	booking_commercial.carrier_loading_charge,
	booking_commercial.carrier_unloading_charge,
	booking_commercial.carrier_other_charge,
	(booking_commercial.carrier_sgst + booking_commercial.carrier_cgst + booking_commercial.carrier_igst) as carrier_gst,
	(case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.carrier_basic_freight else booking_commercial.carrier_price end)  as vendor_basic_cost,
	thc_payment_charges.final_amount,
	thc_payment_charges.advance_amount,
	thc_payment_charges.balance,
	thc_payment_charges.halting_charges,
	(COALESCE(thc_payment_charges.halting_charges,0)+COALESCE(booking_commercial.carrier_other_charge,0)+COALESCE(booking_commercial.carrier_unloading_charge,0)+COALESCE(booking_commercial.carrier_loading_charge,0)+COALESCE(booking_commercial.carrier_oda,0)+COALESCE(booking_commercial.carrier_docket_charge,0)+COALESCE(booking_commercial.carrier_fov,0)+COALESCE(booking_commercial.carrier_fsc,0)+COALESCE(thc_payment_charges.final_amount,0)+COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.carrier_basic_freight else booking_commercial.carrier_price end),0))as sub_total,
	(COALESCE(thc_payment_charges.halting_charges,0)+COALESCE(booking_commercial.carrier_sgst,0) + COALESCE(booking_commercial.carrier_cgst,0) + COALESCE(booking_commercial.carrier_igst,0) + COALESCE(booking_commercial.carrier_other_charge,0)+COALESCE(booking_commercial.carrier_unloading_charge,0)+COALESCE(booking_commercial.carrier_loading_charge,0)+COALESCE(booking_commercial.carrier_oda,0)+COALESCE(booking_commercial.carrier_docket_charge,0)+COALESCE(booking_commercial.carrier_fov,0)+COALESCE(booking_commercial.carrier_fsc,0)+COALESCE(thc_payment_charges.balance,0)+COALESCE(thc_payment_charges.advance_amount,0)+COALESCE(thc_payment_charges.final_amount,0)+COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.carrier_basic_freight else booking_commercial.carrier_price end),0)) as total_vendor_expense,
	(COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end),0)+COALESCE(booking_commercial.customer_fsc,0)+COALESCE(booking_commercial.customer_fov,0)+COALESCE(booking_commercial.customer_docket_charge,0)+COALESCE(booking_commercial.customer_handing_charge,0)+COALESCE(booking_commercial.customer_oda,0)+COALESCE(booking_commercial.customer_loading_charge,0)+COALESCE(booking_commercial.customer_unloading_charge,0)+COALESCE(booking_commercial.customer_other_charge,0)+COALESCE(booking_commercial.customer_management_fee,0))-(COALESCE(thc_payment_charges.halting_charges,0)+COALESCE(booking_commercial.carrier_other_charge,0)+COALESCE(booking_commercial.carrier_unloading_charge,0)+COALESCE(booking_commercial.carrier_loading_charge,0)+COALESCE(booking_commercial.carrier_oda,0)+COALESCE(booking_commercial.carrier_docket_charge,0)+COALESCE(booking_commercial.carrier_fov,0)+COALESCE(booking_commercial.carrier_fsc,0)+COALESCE(thc_payment_charges.final_amount,0)+COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.carrier_basic_freight else booking_commercial.carrier_price end),0)) as docket_profitability,
	t3.actual_delivery_date,
	trip.trip_status
from 
trip_track
join trip on trip.id = trip_track.trip_id
join shipment_details on shipment_details.drop_id = trip_track.drop_id
join drops on drops.id = trip_track.drop_id
join customeraddress on customeraddress.id = drops.customeraddress_id
join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
join vehicle on vehicle_booking_details.vehicle_id = vehicle.id
join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
join vehicle_type on vehicle_attr. vehicle_type_id = vehicle_type.id
join booking on booking.id = vehicle_booking_details.booking_id
join warehouse on booking.warehouse_id::int = warehouse.id
join branch on warehouse.branch_id = branch.id
join customer on customeraddress.customer_id = customer.id
join carrier_company on vehicle_booking_details.vehicle_company_id = carrier_company.id
inner join source on booking.source_id = source.id
join (select city as from_location,id from customeraddress)s on s.id = source.customeraddress_id
join (select city as to_location,id from customeraddress)t on t.id = drops.customeraddress_id
join
		(
			SELECT 
				booking_commercial.id as booking_commercial_id,
				(t_a.time_stamp::timestamp::date) + make_interval(days => booking_commercial.customer_tat) AS eta
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
			where  t_a.event_id = 4
		)as t2 
	on t2.booking_commercial_id = booking_commercial.id
left join (select trip_id,added_on_datetime::date as invoice_date from trip_documents where trip_documents.document_type = 'invoice' group by trip_id,added_on_datetime)one on one.trip_id= trip_track.trip_id

left join thc_masters on thc_masters.master_trip_id = trip_track.master_trip_id
	left join thc_details on thc_masters.thc_masters_id = thc_details.thc_masters_id
	left join thc_payments on thc_payments.thc_masters_id = thc_masters.thc_masters_id
	left join thc_payment_charges on thc_payment_charges.thc_masters_id = thc_masters.thc_masters_id

left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id


where trip_track.status != 'Cancelled'
	)mytable
WHERE
lr_date BETWEEN '{0}' AND '{1}'

		'''.format(from_date,to_date)
			print(from_date)
			cur1.execute(query)
			result = cur1.fetchall()
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			#cur1.close()
			conn1.close()
			
		result=pd.DataFrame(result,columns=['branch','region','customer_lr_number','packages','lr_date','expected_date_delivery','customer','from_location','to_location','invoice_no','vendor_lr_number','vendor_lr_date','invoice_date','vendor_name','thc_number','thc_date','vehicle_number','vehicle_type','actual_weight','volumetric_weight','charged_weight','service','customer_basic_freight','customer_fsc','customer_fov','customer_docket_charge','customer_handing_charge','customer_oda','customer_loading_charge','customer_unloading_charge','customer_other_charge','customer_management_fee','cust_sub_total','gst','customer_total_freight','carrier_fsc','carrier_fov','carrier_docket_charge','carrier_oda','carrier_loading_charge','carrier_unloading_charge','carrier_other_charge','carrier_gst','vendor_basic_cost','final_amount','advance_amount','balance','halting_charges','sub_total','total_vendor_expense','docket_profitability','actual_delivery_date','trip_status'])
		print("checking length \n ",len(result))
		filters = result

		#filt = 'region =="{0}"  & customer == "{1}" & branch == "{2}" | region =="{0}" & customer == "{1}" '.format(region,customer,branch)
		#filters = result.query(filt)
		print("after executing filter query:",len(filters))
		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['actual_delivery_date'] = pd.to_datetime(filters['actual_delivery_date']).dt.strftime('%d/%m/%Y')
		filters['expected_date_delivery'] = pd.to_datetime(filters['expected_date_delivery']).dt.strftime('%d/%m/%Y')
		filters['invoice_date'] = pd.to_datetime(filters['invoice_date']).dt.strftime('%d/%m/%Y')
		filters['vendor_lr_date'] = pd.to_datetime(filters['vendor_lr_date']).dt.strftime('%d/%m/%Y')
		filters['thc_date'] = pd.to_datetime(filters['thc_date']).dt.strftime('%d/%m/%Y')

		filters['lr_date']=filters['lr_date'].astype(str)
		filters['expected_date_delivery']=filters['expected_date_delivery'].astype(str)	
		filters['actual_delivery_date']=filters['actual_delivery_date'].astype(str)
		filters['invoice_date']=filters['invoice_date'].astype(str)
		filters['vendor_lr_date']=filters['vendor_lr_date'].astype(str)
		filters['thc_date']=filters['thc_date'].astype(str)
		filters = filters.replace('nan','')
		
		
		return (filters)
	except Exception as e:
		print(e)
		return str(e)


def freight_report(from_date,to_date):
	try:
		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
	select * from 
	(select 
	warehouse.warehouse_name as branch,
	branch.branch_name as Region,
	trip_consignment.customer_lr_number,
	trip_consignment.material_quantity as packages,
	customer_lr_numbers.final_status_datetime::date as lr_date,
	t2.eta as expected_date_delivery,
	customer.customer_company as customer,
	s.from_location,
	t.to_location,
	shipment_details.invoice_no,
	one.invoice_date,
	-- trip_documents.added_on_datetime::date as invoice_date,
	thc_details.thc_number,
	thc_details.thc_creation_date as thc_date,
	(case when booking_commercial.logistic_booking_type = 'LTL' then thc_details.vehicle_number else vehicle.regno end) as vehicle_number,
	(case when booking_commercial.logistic_booking_type = 'LTL' then thc_details.vehicle_type else vehicle_type.type end) as vehicle_type,
	trip_consignment.weight as actual_weight,
	booking_commercial.carrier_volumetric_weight as volumetric_weight,
	shipment_details.charged_shipment_weight as charged_weight,
	booking_commercial.logistic_booking_type as service,
	(case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end) as customer_basic_freight,
	booking_commercial.customer_fsc,
	booking_commercial.customer_fov,
	booking_commercial.customer_docket_charge,
	booking_commercial.customer_handing_charge,
	booking_commercial.customer_oda,
	booking_commercial.customer_loading_charge,
	booking_commercial.customer_unloading_charge,
	booking_commercial.customer_other_charge,
	booking_commercial.customer_management_fee,
	(COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end),0)+COALESCE(booking_commercial.customer_fsc,0)+COALESCE(booking_commercial.customer_fov,0)+COALESCE(booking_commercial.customer_docket_charge,0)+COALESCE(booking_commercial.customer_handing_charge,0)+COALESCE(booking_commercial.customer_oda,0)+COALESCE(booking_commercial.customer_loading_charge,0)+COALESCE(booking_commercial.customer_unloading_charge,0)+COALESCE(booking_commercial.customer_other_charge,0)+COALESCE(booking_commercial.customer_management_fee,0)) as sub_total,
	(COALESCE(booking_commercial.customer_sgst,0) + COALESCE(booking_commercial.customer_cgst,0) + COALESCE(booking_commercial.customer_igst,0)) as gst,
	(COALESCE(booking_commercial.customer_management_fee,0)+COALESCE(booking_commercial.customer_other_charge,0)+COALESCE(booking_commercial.customer_unloading_charge,0)+COALESCE(booking_commercial.customer_loading_charge,0)+COALESCE(booking_commercial.customer_oda,0)+COALESCE(booking_commercial.customer_handing_charge,0)+COALESCE(booking_commercial.customer_docket_charge,0)+COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end),0) + COALESCE(booking_commercial.customer_fsc,0) + COALESCE(booking_commercial.customer_fov,0) + COALESCE(booking_commercial.customer_sgst,0) + COALESCE(booking_commercial.customer_cgst,0) + COALESCE(booking_commercial.customer_igst,0))as customer_total_freight,
	thc_payment_charges.final_amount,
	thc_payment_charges.advance_amount,
	thc_payment_charges.balance,
	thc_payment_charges.halting_charges,
	(COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.customer_basic_freight else booking_commercial.customer_price end),0)+COALESCE(booking_commercial.customer_fsc,0)+COALESCE(booking_commercial.customer_fov,0)+COALESCE(booking_commercial.customer_docket_charge,0)+COALESCE(booking_commercial.customer_handing_charge,0)+COALESCE(booking_commercial.customer_oda,0)+COALESCE(booking_commercial.customer_loading_charge,0)+COALESCE(booking_commercial.customer_unloading_charge,0)+COALESCE(booking_commercial.customer_other_charge,0)+COALESCE(booking_commercial.customer_management_fee,0))-(COALESCE(thc_payment_charges.halting_charges,0)+COALESCE(booking_commercial.carrier_other_charge,0)+COALESCE(booking_commercial.carrier_unloading_charge,0)+COALESCE(booking_commercial.carrier_loading_charge,0)+COALESCE(booking_commercial.carrier_oda,0)+COALESCE(booking_commercial.carrier_docket_charge,0)+COALESCE(booking_commercial.carrier_fov,0)+COALESCE(booking_commercial.carrier_fsc,0)+COALESCE(thc_payment_charges.final_amount,0)+COALESCE((case when booking_commercial.logistic_booking_type = 'LTL' then booking_commercial.carrier_basic_freight else booking_commercial.carrier_price end),0)) as docket_profitability,
	t3.actual_delivery_date,
	trip.trip_status as trip_status
	from 
trip_track
join trip on trip.id = trip_track.trip_id
join shipment_details on shipment_details.drop_id = trip_track.drop_id
join drops on drops.id = trip_track.drop_id
join customeraddress on customeraddress.id = drops.customeraddress_id
join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
join vehicle on vehicle_booking_details.vehicle_id = vehicle.id
join vehicle_attr on vehicle_attr.vehicle_id = vehicle.id
join vehicle_type on vehicle_attr. vehicle_type_id = vehicle_type.id
join booking on booking.id = vehicle_booking_details.booking_id
join warehouse on booking.warehouse_id::int = warehouse.id
join branch on warehouse.branch_id = branch.id
join customer on customeraddress.customer_id = customer.id
join carrier_company on vehicle_booking_details.vehicle_company_id = carrier_company.id
inner join source on booking.source_id = source.id
join (select city as from_location,id from customeraddress)s on s.id = source.customeraddress_id
join (select city as to_location,id from customeraddress)t on t.id = drops.customeraddress_id
join
		(
			SELECT 
				booking_commercial.id as booking_commercial_id,
				(t_a.time_stamp::timestamp::date) + make_interval(days => booking_commercial.customer_tat) AS eta
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
			where  t_a.event_id = 4
		)as t2 
	on t2.booking_commercial_id = booking_commercial.id
left join (select trip_id,added_on_datetime::date as invoice_date from trip_documents where trip_documents.document_type = 'invoice' group by trip_id,added_on_datetime)one on one.trip_id= trip_track.trip_id

left join thc_masters on thc_masters.master_trip_id = trip_track.master_trip_id
	left join thc_details on thc_masters.thc_masters_id = thc_details.thc_masters_id
	left join thc_payments on thc_payments.thc_masters_id = thc_masters.thc_masters_id
	left join thc_payment_charges on thc_payment_charges.thc_masters_id = thc_masters.thc_masters_id

left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id

	where trip_track.status != 'Cancelled'
	)mytable
		WHERE	 
		lr_date BETWEEN '{0}' AND '{1}'
		'''.format(from_date,to_date)
			print(from_date)
			cur1.execute(query)
			result = cur1.fetchall()
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
			
		result=pd.DataFrame(result,columns=['branch','region','customer_lr_number','packages','lr_date','expected_date_delivery','customer','from_location','to_location','invoice_no','invoice_date','thc_number','thc_date','vehicle_number','vehicle_type','actual_weight','volumetric_weight','charged_weight','service','customer_basic_freight','customer_fsc','customer_fov','customer_docket_charge','customer_handing_charge','customer_oda','customer_loading_charge','customer_unloading_charge','customer_other_charge','customer_management_fee','cust_sub_total','gst','customer_total_freight','final_amount','advance_amount','balance','halting_charges','docket_profitability','actual_delivery_date','trip_status'])
		print("checking length \n ",len(result))
		filters = result

			
		#filt = 'region =="{0}"  & customer == "{1}" & branch == "{2}" | region =="{0}" & customer == "{1}" '.format(region,customer,branch)
		#filters = result.query(filt)
		print("after executing filter query:",len(filters))
		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['actual_delivery_date'] = pd.to_datetime(filters['actual_delivery_date']).dt.strftime('%d/%m/%Y')
		filters['expected_date_delivery'] = pd.to_datetime(filters['expected_date_delivery']).dt.strftime('%d/%m/%Y')
		filters['invoice_date'] = pd.to_datetime(filters['invoice_date']).dt.strftime('%d/%m/%Y')
		filters['thc_date'] = pd.to_datetime(filters['thc_date']).dt.strftime('%d/%m/%Y')

		filters['lr_date']=filters['lr_date'].astype(str)
		filters['expected_date_delivery']=filters['expected_date_delivery'].astype(str)	
		filters['actual_delivery_date']=filters['actual_delivery_date'].astype(str)
		filters['invoice_date']=filters['invoice_date'].astype(str)
		filters['thc_date']=filters['thc_date'].astype(str)
		filters = filters.replace('nan','')

		#if (len(df) == 0):
		#	s = {'cells':df,"success":"true","message":"No Data for the selected filter."}
		#result = list(result[0])
		
		
		return (filters)
	except Exception as e:
		print(e)
		return str(e)


def mis_report(from_date,to_date):
	try:

		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
	select * from 
	(select 
	customer.customer_company as customer,
	warehouse.warehouse_name as branch,
	branch.branch_name as Region,
	shipment_details.customer_lr_number,
	customer_lr_numbers.final_status_datetime::date as lr_date,
	customeraddress.city as consignee_city,
	customeraddress.contact_name as consignee_name,
	count(trip_consignment_package_details.trip_consignment_id) as articles,
	trip_consignment.weight as actual_weight,
	shipment_details.charged_shipment_weight,
	shipment_details.invoice_no,
	shipment_details.invoice_value,
	trip_consignment.material_type,
	booking_commercial.customer_tat as transit_days,
	t2.eta::date as expected_date_delivery,
	t3.actual_delivery_date::date,
	t2.eta::date - shipment_details.schedule_delivery_date::date as variance,
	trip.trip_status as trip_status

	from 
	trip_track
	join trip on trip.id = trip_track.trip_id
	join shipment_details on shipment_details.drop_id = trip_track.drop_id
	join drops on drops.id = trip_track.drop_id
	join customeraddress on customeraddress.id = drops.customeraddress_id
	join customer on customeraddress.customer_id = customer.id
	join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
	join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
	join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
	join booking on booking.id = vehicle_booking_details.booking_id
	join warehouse on booking.warehouse_id::int = warehouse.id
	join branch on warehouse.branch_id = branch.id
	join(
	SELECT 
	booking_commercial.id as booking_commercial_id,
	(t_a.time_stamp::timestamp::date) + make_interval(days => booking_commercial.customer_tat) + make_interval(days => 1) AS eta
	from trip_consignment
	inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
	inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
	inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
	inner join trip_events t_a on tr.id = t_a.trip_id
	where  t_a.event_id = 4)as t2 on t2.booking_commercial_id = booking_commercial.id
	join trip_consignment_package_details on trip_consignment.trip_consignment_id = trip_consignment_package_details.trip_consignment_id
	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id
	where trip_track.status != 'Cancelled'
	
	group by 
	customer.customer_company,
	warehouse.warehouse_name,
	branch.branch_name,
	shipment_details.customer_lr_number,
	customer_lr_numbers.final_status_datetime::date,
	customeraddress.city,
	customeraddress.contact_name,
	trip_consignment.weight,
	shipment_details.charged_shipment_weight,
	shipment_details.invoice_no,
	shipment_details.invoice_value,
	trip_consignment.material_type,
	booking_commercial.customer_tat,
	t2.eta::date,
	t3.actual_delivery_date::date,
	shipment_details.schedule_delivery_date,
	trip.trip_status

	
	)mytable
		WHERE	 
		lr_date BETWEEN '{0}' AND '{1}'
		'''.format(from_date,to_date)
			print(from_date)
			cur1.execute(query)
			result = cur1.fetchall()
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
			
		result=pd.DataFrame(result,columns=["customer","branch","region","customer_lr_number","lr_date","consignee_city","consignee_name","articles","actual_weight","charged_shipment_weight","invoice_no","invoice_value","material_type","transit_days","expected_date_delivery","actual_delivery_date","variance","trip_status"])
		print("checking length \n ",len(result))
		filters = result

			
		#filt = 'region =="{0}"  & customer == "{1}" & branch == "{2}" | region =="{0}" & customer == "{1}" '.format(region,customer,branch)
		#filters = result.query(filt)
		print("after executing filter query:",len(filters))
		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['actual_delivery_date'] = pd.to_datetime(filters['actual_delivery_date']).dt.strftime('%d/%m/%Y')
		filters['expected_date_delivery'] = pd.to_datetime(filters['expected_date_delivery']).dt.strftime('%d/%m/%Y')
		
		

		filters['lr_date']=filters['lr_date'].astype(str)
		filters['expected_date_delivery']=filters['expected_date_delivery'].astype(str)	
		filters['actual_delivery_date']=filters['actual_delivery_date'].astype(str)
		
		
		filters = filters.replace('nan','')
		return (filters)

	except Exception as e:
		print(e)
		return str(e)


def mis_report_tupperware(from_date,to_date):
	try:

		try:
			conn1 = psycopg2.connect(dbname="transo_nippon_production",user="ezyloads", host="127.0.0.1", password="ezy@1234")
			cur1 = conn1.cursor()
			query='''
	select * from 
	(select 
	customer.customer_company as customer,
	warehouse.warehouse_name as branch,
	branch.branch_name as Region,
	shipment_details.customer_lr_number,
	customer_lr_numbers.final_status_datetime::date as lr_date,
	customeraddress.city as consignee_city,
	customeraddress.contact_name as consignee_name,
	customeraddress.contact_code as consignee_code,
	count(trip_consignment_package_details.trip_consignment_id) as articles,
	round((trip_consignment.weight)::numeric,2) as actual_weight,
	round((shipment_details.charged_shipment_weight)::numeric,2) as charged_shipment_weight,
	shipment_details.invoice_no,
	one.invoice_date,
	round((shipment_details.invoice_value)::numeric,2) as invoice_value,
	trip_consignment.material_type,
	booking_commercial.customer_tat as transit_days,
	t2.eta::date as expected_date_delivery,
t3.actual_delivery_date::date,
	t2.eta::date - shipment_details.schedule_delivery_date::date as variance,
	booking.logistic_booking_type as booking_type,
	carrier_company.company_name as vendor_name,
	shipment_details.vendor_lr_number,
	trip.trip_status as trip_status

	from 
	trip_track
	join trip on trip.id = trip_track.trip_id
	join shipment_details on shipment_details.drop_id = trip_track.drop_id
	join drops on drops.id = trip_track.drop_id
	join customeraddress on customeraddress.id = drops.customeraddress_id
	join customer on customeraddress.customer_id = customer.id
	join trip_consignment on trip_track.drop_id = trip_consignment.drop_id
	join customer_lr_numbers on trip_consignment.customer_lr_numbers_id = customer_lr_numbers.id
	join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id
	inner join carrier_company on booking_commercial.carrier_company_id = carrier_company.id
	inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
	join booking on booking.id = vehicle_booking_details.booking_id
	join warehouse on booking.warehouse_id::int = warehouse.id
	join branch on warehouse.branch_id = branch.id
	join(
	SELECT 
	booking_commercial.id as booking_commercial_id,
	(t_a.time_stamp::timestamp::date) + make_interval(days => booking_commercial.customer_tat) + make_interval(days => 1) AS eta
	from trip_consignment
	inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
	inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
	inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
	inner join trip_events t_a on tr.id = t_a.trip_id
	where  t_a.event_id = 4)as t2 on t2.booking_commercial_id = booking_commercial.id
	join trip_consignment_package_details on trip_consignment.trip_consignment_id = trip_consignment_package_details.trip_consignment_id
	left join (select trip_id,added_on_datetime::date as invoice_date from trip_documents where trip_documents.document_type = 'invoice' group by trip_id,added_on_datetime)one on one.trip_id= trip_track.trip_id
	left join 
		(SELECT booking_commercial.id as booking_commercial_id,
			t_a.event_time AS actual_delivery_date
			from trip_consignment
		 inner join booking_commercial on booking_commercial.trip_consignment_id = trip_consignment.trip_consignment_id	
		 inner join vehicle_booking_details on vehicle_booking_details.id = trip_consignment.vehicle_booking_details_id
		 inner join trip tr on tr.vehicle_booking_details = vehicle_booking_details.id	
		 inner join trip_events t_a on tr.id = t_a.trip_id
		where t_a.event_id = 12
		)as t3
	on t3.booking_commercial_id = booking_commercial.id
	where trip_track.status != 'Cancelled'
	
	group by 
	customer.customer_company,
	warehouse.warehouse_name,
	branch.branch_name,
	shipment_details.customer_lr_number,
	customer_lr_numbers.final_status_datetime::date,
	customeraddress.city,
	customeraddress.contact_name,
	trip_consignment.weight,
	shipment_details.charged_shipment_weight,
	shipment_details.invoice_no,
	shipment_details.invoice_value,
	trip_consignment.material_type,
	booking_commercial.customer_tat,
	t2.eta::date,
	t3.actual_delivery_date::date,
	shipment_details.schedule_delivery_date,
	customeraddress.contact_code,
	one.invoice_date,
	booking.logistic_booking_type,
	carrier_company.company_name,
	shipment_details.vendor_lr_number,
	trip.trip_status

	
	)mytable
		WHERE	 
		lr_date BETWEEN '{0}' AND '{1}'
		'''.format(from_date,to_date)
			print(from_date)
			cur1.execute(query)
			result = cur1.fetchall()
		except Exception:
			conn1.rollback()
			logging.error("Database connection error")
			raise
		#for i in result:
		else:
			conn1.commit()
		finally:
			cur1.close()
			conn1.close()
			
		result=pd.DataFrame(result,columns=["customer","branch","region","customer_lr_number","lr_date","consignee_city","consignee_name","consignee_code","articles","actual_weight","charged_shipment_weight","invoice_no","invoice_date","invoice_value","material_type","transit_days","expected_date_delivery","actual_delivery_date","variance","booking_type","vendor_name","vendor_lr_number", "trip_status"
	])
		print("checking length \n ",len(result))
		filters = result

			
		#filt = 'region =="{0}"  & customer == "{1}" & branch == "{2}" | region =="{0}" & customer == "{1}" '.format(region,customer,branch)
		#filters = result.query(filt)
		print("after executing filter query:",len(filters))
		filters['lr_date'] = pd.to_datetime(filters['lr_date']).dt.strftime('%d/%m/%Y')
		filters['actual_delivery_date'] = pd.to_datetime(filters['actual_delivery_date']).dt.strftime('%d/%m/%Y')
		filters['expected_date_delivery'] = pd.to_datetime(filters['expected_date_delivery']).dt.strftime('%d/%m/%Y')
		filters['lr_date']=filters['lr_date'].astype(str)
		filters['expected_date_delivery']=filters['expected_date_delivery'].astype(str)	
		filters['actual_delivery_date']=filters['actual_delivery_date'].astype(str)
		filters = filters.replace('nan','')
	
		
		return (filters)
	except Exception as e:
		print(e)
		return str(e)


