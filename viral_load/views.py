from django.shortcuts import render
from viral_load.models import ViralLoad
# from encounters.views import RemoteEncounters
from viral_load.serializer import ViralLoadSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from service import ApplicationService
from datetime import datetime
from django.http import JsonResponse
from rest_framework import authentication, permissions
# Create your views here.
class ViralLoadList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        service = ApplicationService()
        query ='''SELECT * FROM encounters e INNER JOIN facilities f on f.id = e.facility_id 
        WHERE encounter_date = '{}' AND f.viral_load = '1'; '''.format(datetime.today().strftime('%Y-%m-%d'))
        results = service.query_processor(query)
        return JsonResponse({
            'facilities':results
        })
           
class RemoteViralLoad(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            data = request.data  
        except AttributeError:
            data = request
        serializer = ViralLoadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        
    def get_lab_orders(self,data,client,remote,start_date,end_date):
        lab_order_query ='''"SELECT od.accession_number,MAX(pi.identifier),MAX(o.date_created) as ordered_date, 
            MAX(reason_test.name) as reason_test,MAX(statuses.value_text) AS order_status FROM obs o                    
            INNER JOIN orders od ON o.order_id = od.order_id    
            INNER JOIN patient_identifier pi ON pi.patient_id = o.person_id
            LEFT JOIN obs reason ON reason.order_id = od.order_id AND reason.voided = 0  AND reason.concept_id = 2429 -- 'Reason for test'
			LEFT JOIN concept_name reason_test ON reason_test.concept_id = reason.value_coded AND reason_test.voided = 0 
            LEFT JOIN obs statuses ON statuses.order_id = od.order_id AND statuses.voided = 0 AND statuses.concept_id = 10682 -- 'lab order status'
            WHERE o.value_coded =856 AND o.voided =0 AND pi.identifier_type = 4 AND DATE(o.date_created) BETWEEN '{}' AND '{}'                     
            group by od.accession_number;"'''.format(start_date,end_date)
        return remote.execute_query(data, client, lab_order_query)
        
    def get_lab_order_results(self,data,client,remote):
        lab_order_results_query = '''"SELECT od.accession_number,o.date_created as released_date,
                    CONCAT(o.value_modifier,' ', COALESCE(o.value_numeric,''),COALESCE(o.value_text,'')) as results FROM obs o
                    INNER JOIN orders od ON o.order_id = od.order_id
                    WHERE o.concept_id=856 AND DATE(o.date_created) = '{}'
                    order by o.obs_id desc;"'''.format(datetime.today().strftime('%Y-%m-%d'))
        return remote.execute_query(data, client, lab_order_results_query)
    
    def get_acknowledgement(self,data,client,remote):
        acknowledgement_query = '''"SELECT o.accession_number,las.acknowledgement_type,las.date_received as acknowledgement_date  
                                FROM lims_acknowledgement_statuses las
                                INNER JOIN orders o on las.order_id = o.order_id;"'''
        return remote.execute_query(data, client, acknowledgement_query)
        
    def create_lab_orders(self,results,facility_id):
        if results:
            del results[0]
            for result in results:
                result = result.rstrip('\n').split('\t')
                update=self.update_vl_status(result)
                if(update):
                    try:
                        lab_order= { 
                            'facility':facility_id,
                            'accession_number':result[0],
                            'person_id':result[1],
                            'ordered_date':result[2],
                            'test_reason':result[3],
                            'order_status':result[4]
                        }
                        self.post(lab_order)
                    except ViralLoad.DoesNotExist:
                        print("Fail to insert a viral load")
        
    def update_vl_status(self,result):
        try:
            update_vl_status = ViralLoad.objects.get(accession_number=result[0])
            update_vl_status.order_status = result[4] 
            update_vl_status.save()
            return False
        except ViralLoad.DoesNotExist:
            return True    

    def create_lab_order_results(self,results):
        if results:
            del results[0]
            for result in results:
                result = result.rstrip('\n').split('\t')
                try:
                    update_viral_load_results = ViralLoad.objects.get(accession_number=result[0])
                    update_viral_load_results.released_date = result[1] 
                    update_viral_load_results.results =  result[2]   
                    update_viral_load_results.save()
                except ViralLoad.DoesNotExist:
                    print("Viral load results not available")
                    
    def create_acknowledgement_results(self,results):
        if results:
            del results[0]
            for result in results:
                result = result.rstrip('\n').split('\t')
                try:
                    update_viral_load_acknowledgement = ViralLoad.objects.get(accession_number=result[0])
                    update_viral_load_acknowledgement.acknowledgement_type = result[1] 
                    update_viral_load_acknowledgement.acknowledgement_date =  result[2]   
                    update_viral_load_acknowledgement.save()
                except ViralLoad.DoesNotExist:
                    pass
                
    def process_lab_orders(self,db_data,client,facility_id,remote):
        date =datetime.today().strftime('%Y-%m-%d')
        results =self.get_lab_orders(db_data,client,remote,'2023-06-26',date)
        self.create_lab_orders(results,facility_id)
        results = self.get_lab_order_results(db_data,client,remote)
        self.create_lab_order_results(results)
        results = self.get_acknowledgement(db_data,client,remote)
        self.create_acknowledgement_results(results)
        
                    
        
        
    