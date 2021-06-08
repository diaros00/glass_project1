from django.shortcuts import render,redirect
from .models import Defect , modelGlass , modelGlassWithDefect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import UserProfile
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Case, When, IntegerField
import datetime
from datetime import timedelta
from datetime import datetime
from django.db.models import Q
from decimal import Decimal
from collections import Counter


counter = 0
counter = 1
datepick_for_check = 0

status_defect_for_check = 0   # 0 คือ ไม่มี defect  /  1  คือ พบ defect
status_defect_to_nodefect = 0   # 0 คือ ไม่มี defect  /  1  คือ พบ defect
status_check_before_have_noDefect = 'no'




def hello(request):
    #Query
    data_defect = Defect.objects.all()
    data_glass = modelGlass.objects.all()
    return render(request,'index.html',{'defects':data_defect,'modelGlasss':data_glass})


def report(request):
    
    labels = []
    data = []

    if modelGlassWithDefect:
        
        queryset = modelGlassWithDefect.objects.filter(status_glass="NG")
        data_defect = Defect.objects.all()
        # print('data_defect >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' ,data_defect[0].defect_name)
        count_defect_name1 = 0
        count_defect_name2 = 0
        count_defect_name3 = 0
        count_defect_name4 = 0
        count_defect_name5 = 0

        for i in range(Defect.objects.all().count()):

            count_defect_name1_temp = modelGlassWithDefect.objects.filter(defect_name1=data_defect[i].defect_name).count()
            count_defect_name2_temp = modelGlassWithDefect.objects.filter(defect_name2=data_defect[i].defect_name).count()
            count_defect_name3_temp = modelGlassWithDefect.objects.filter(defect_name3=data_defect[i].defect_name).count()
            count_defect_name4_temp = modelGlassWithDefect.objects.filter(defect_name4=data_defect[i].defect_name).count()
            count_defect_name5_temp = modelGlassWithDefect.objects.filter(defect_name5=data_defect[i].defect_name).count()

            count_defect_name1 = count_defect_name1 + count_defect_name1_temp
            count_defect_name2 = count_defect_name2 + count_defect_name2_temp
            count_defect_name3 = count_defect_name3 + count_defect_name3_temp
            count_defect_name4 = count_defect_name4 + count_defect_name4_temp
            count_defect_name5 = count_defect_name5 + count_defect_name5_temp

            count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5

            print(data_defect[i].defect_name, ' = ' ,count_defect_all)

            labels.append(data_defect[i].defect_name)
            data.append(count_defect_all)


        return  render(request, 'report.html', {
            'labels': labels,
            'data': data,
            'defects':data_defect,
            'data_defects':queryset
        })
def filtering(request): 
    labels = []
    data = []
    inputDefect = request.POST['inputDefect']
    shift = request.POST['shift']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']




    print("shift : ",shift)
    print("start_date : ",start_date)
    print("end_date : ",end_date)
    data_defect = Defect.objects.all()
    count_defect_name1 = 0
    count_defect_name2 = 0
    count_defect_name3 = 0
    count_defect_name4 = 0
    count_defect_name5 = 0

   
        
    #-------------------->>>>> inputDefect  ALL
    if inputDefect == 'ALL' :
        
        if shift == 'ALL' :
            #-------------------->>>>> defect ALL + shift ALL  +  Date  
            if start_date:
                print("#-------------------->>>>> defect ALL + shift ALL  +  Date   1")
                queryset = modelGlassWithDefect.objects.filter(date_create__range=(start_date, end_date)).filter(status_glass="NG")
                count_row_mix = modelGlassWithDefect.objects.filter(date_create__range=(start_date, end_date)).filter(status_glass="NG").count()

                
                list_of_label = []
                

                for i in range(count_row_mix):
                    for k in range(data_defect.count()):
                        if data_defect[k].defect_name == queryset[i].defect_name1:
                            count_defect_name1_temp = 1
                            count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name2:
                            count_defect_name2_temp = 1
                            count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name3:
                            count_defect_name3_temp = 1
                            count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name4:
                            count_defect_name4_temp = 1
                            count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name5:
                            count_defect_name5_temp = 1
                            count_defect_name5 = count_defect_name5 + count_defect_name5_temp
                            list_of_label.append(data_defect[k].defect_name)
                        
                        
                        # count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5
        
                print(list_of_label)

                Counter(list_of_label).keys() # equals to list(set(words))
                Counter(list_of_label).values() # counts the elements' frequency
                label_list = list(Counter(list_of_label).keys())
                data_list = list(Counter(list_of_label).values())
                print(len(label_list))
                for i in range(len(label_list)):  # จัดเก็บลง label กับ data
                    labels.append(label_list[i])   
                    data.append(data_list[i])

                print(labels)
                print(data)


                # for i in range(Defect.objects.all().count()):
                #     count_defect_name1_temp = modelGlassWithDefect.objects.filter(defect_name1=data_defect[i].defect_name).count()
                #     count_defect_name2_temp = modelGlassWithDefect.objects.filter(defect_name2=data_defect[i].defect_name).count()
                #     count_defect_name3_temp = modelGlassWithDefect.objects.filter(defect_name3=data_defect[i].defect_name).count()
                #     count_defect_name4_temp = modelGlassWithDefect.objects.filter(defect_name4=data_defect[i].defect_name).count()
                #     count_defect_name5_temp = modelGlassWithDefect.objects.filter(defect_name5=data_defect[i].defect_name).count()

                #     count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                #     count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                #     count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                #     count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                #     count_defect_name5 = count_defect_name5 + count_defect_name5_temp
                #     count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5
                #     print(data_defect[i].defect_name, ' = ' ,count_defect_all)

                #         # labels.append(data_defect[i].defect_name)
                #     labels.append(data_defect[i].defect_name)
                # data.append(count_defect_all)
                
                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':inputDefect,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                        
                    })
            #-------------------->>>>> defect ALL + shift ALL    
            else:
                print("#-------------------->>>>> defect ALL + shift ALL + NO Date   2")
            
                queryset = modelGlassWithDefect.objects.filter(status_glass="NG")
                for i in range(Defect.objects.all().count()):

                    count_defect_name1_temp = modelGlassWithDefect.objects.filter(defect_name1=data_defect[i].defect_name).count()
                    count_defect_name2_temp = modelGlassWithDefect.objects.filter(defect_name2=data_defect[i].defect_name).count()
                    count_defect_name3_temp = modelGlassWithDefect.objects.filter(defect_name3=data_defect[i].defect_name).count()
                    count_defect_name4_temp = modelGlassWithDefect.objects.filter(defect_name4=data_defect[i].defect_name).count()
                    count_defect_name5_temp = modelGlassWithDefect.objects.filter(defect_name5=data_defect[i].defect_name).count()

                    count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                    count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                    count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                    count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                    count_defect_name5 = count_defect_name5 + count_defect_name5_temp

                    count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5

                    print(data_defect[i].defect_name, ' = ' ,count_defect_all)

                    labels.append(data_defect[i].defect_name)
                    data.append(count_defect_all)

                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':inputDefect,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                    
                })    
        #-------------------->>>>> defect ALL + shift NO All         
        else:

            if start_date:
                print("#-------------------->>>>> defect ALL + shift NO All   + Date   3")
                # filter สองอันพร้อมกัน filter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกัน

                queryset = modelGlassWithDefect.objects.filter(shift=shift).filter(status_glass="NG").filter(date_create__range=(start_date, end_date))
                count_row_mix = modelGlassWithDefect.objects.filter(shift=shift).filter(status_glass="NG").filter(date_create__range=(start_date, end_date)).count()
                print('count_row_mix =', count_row_mix )

                # filter สองอันพร้อมกัน filter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกัน
                
                list_of_label = []
                

                for i in range(count_row_mix):
                    for k in range(data_defect.count()):
                        if data_defect[k].defect_name == queryset[i].defect_name1:
                            count_defect_name1_temp = 1
                            count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name2:
                            count_defect_name2_temp = 1
                            count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name3:
                            count_defect_name3_temp = 1
                            count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name4:
                            count_defect_name4_temp = 1
                            count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name5:
                            count_defect_name5_temp = 1
                            count_defect_name5 = count_defect_name5 + count_defect_name5_temp
                            list_of_label.append(data_defect[k].defect_name)
                        
                        
                        # count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5
        
                print(list_of_label)

                Counter(list_of_label).keys() # equals to list(set(words))
                Counter(list_of_label).values() # counts the elements' frequency
                label_list = list(Counter(list_of_label).keys())
                data_list = list(Counter(list_of_label).values())
                print(len(label_list))
                for i in range(len(label_list)):  # จัดเก็บลง label กับ data
                    labels.append(label_list[i])   
                    data.append(data_list[i])

                print(labels)
                print(data)
            
            
                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':inputDefect,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                    
                })
            else:
                print("#-------------------->>>>> defect ALL + shift NO All   + NO Date   4")
                # filter สองอันพร้อมกัน filter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกัน

                queryset = modelGlassWithDefect.objects.filter(shift=shift).filter(status_glass="NG")
                count_row_mix = modelGlassWithDefect.objects.filter(shift=shift).filter(status_glass="NG").count()
                print('count_row_mix =', count_row_mix )

                # filter สองอันพร้อมกัน filter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกัน
                
                list_of_label = []
                

                for i in range(count_row_mix):
                    for k in range(data_defect.count()):
                        if data_defect[k].defect_name == queryset[i].defect_name1:
                            count_defect_name1_temp = 1
                            count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name2:
                            count_defect_name2_temp = 1
                            count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name3:
                            count_defect_name3_temp = 1
                            count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name4:
                            count_defect_name4_temp = 1
                            count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name5:
                            count_defect_name5_temp = 1
                            count_defect_name5 = count_defect_name5 + count_defect_name5_temp
                            list_of_label.append(data_defect[k].defect_name)
                        
                        
                        # count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5
        
                print(list_of_label)

                Counter(list_of_label).keys() # equals to list(set(words))
                Counter(list_of_label).values() # counts the elements' frequency
                label_list = list(Counter(list_of_label).keys())
                data_list = list(Counter(list_of_label).values())
                print(len(label_list))
                for i in range(len(label_list)):  # จัดเก็บลง label กับ data
                    labels.append(label_list[i])   
                    data.append(data_list[i])

                print(labels)
                print(data)
            
            
                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':inputDefect,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                    
                })
    #-------------------->>>>> inputDefect NO ALL
    else:

        
        if shift == 'ALL' :

            #-------------------->>>>> inputDefect NO ALL  + shift ALL + Date
            if start_date:
                print("#-------------------->>>>> inputDefect NO ALL  + shift ALL + Date   5")
                objModeldefect = Defect.objects.get(id=inputDefect)
                # queryset = modelGlassWithDefect.objects.filter(defect_name1=objModeldefect.defect_name) | modelGlassWithDefect.objects.filter(defect_name2=objModeldefect.defect_name) | modelGlassWithDefect.objects.filter(defect_name3=objModeldefect.defect_name) | modelGlassWithDefect.objects.filter(defect_name4=objModeldefect.defect_name) | modelGlassWithDefect.objects.filter(defect_name5=objModeldefect.defect_name)| modelGlassWithDefect.objects.filter(shift=shift) 
     
                queryset = modelGlassWithDefect.objects.filter(date_select__range=(start_date, end_date)).filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name))
                
                print('count_row_mix  = ' ,modelGlassWithDefect.objects.filter(date_select__range=(start_date, end_date)).filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name)).count() )
                count_row_mix = modelGlassWithDefect.objects.filter(date_select__range=(start_date, end_date)).filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name)).count()
                
                
                labels.append(objModeldefect.defect_name)
                data.append(count_row_mix)
                
                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':objModeldefect.defect_name,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                        
                    })
 
                    
            #-------------------->>>>> inputDefect NO ALL  + shift ALL + NO date  
            else:
                print("#-------------------->>>>> inputDefect NO ALL  + shift ALL + NO Date   6")
        
                objModeldefect = Defect.objects.get(id=inputDefect)
                queryset = modelGlassWithDefect.objects.filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name))

                count_row_mix = modelGlassWithDefect.objects.filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name)).count()

                list_of_label = []
                

                for i in range(count_row_mix):
                    for k in range(data_defect.count()):
                        if data_defect[k].defect_name == queryset[i].defect_name1:
                            count_defect_name1_temp = 1
                            count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name2:
                            count_defect_name2_temp = 1
                            count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name3:
                            count_defect_name3_temp = 1
                            count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name4:
                            count_defect_name4_temp = 1
                            count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name5:
                            count_defect_name5_temp = 1
                            count_defect_name5 = count_defect_name5 + count_defect_name5_temp
                            list_of_label.append(data_defect[k].defect_name)
                        
                        
                        # count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5
        
                print(list_of_label)

                Counter(list_of_label).keys() # equals to list(set(words))
                Counter(list_of_label).values() # counts the elements' frequency
                label_list = list(Counter(list_of_label).keys())
                data_list = list(Counter(list_of_label).values())
                print(len(label_list))
                for i in range(len(label_list)):  # จัดเก็บลง label กับ data
                    labels.append(label_list[i])   
                    data.append(data_list[i])

                print(labels)
                print(data)


                # labels.append(objModeldefect.defect_name)
                # data.append(count_row_mix)

                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':objModeldefect.defect_name,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                    
                })    
        #-------------------->>>>> inputDefect NO ALL  + shift NO ALL    
        else:
            #-------------------->>>>> inputDefect NO ALL  + shift NO ALL  + Date
            if start_date:
                print("#-------------------->>>>> inputDefect NO ALL  + shift NO ALL  + Date  7")

                objModeldefect = Defect.objects.get(id=inputDefect)
                queryset = modelGlassWithDefect.objects.filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name)).filter(shift=shift).filter(date_select__range=(start_date, end_date))

                count_row_mix = modelGlassWithDefect.objects.filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name)).filter(shift=shift).filter(date_select__range=(start_date, end_date)).count()

             
                print('count_row_mix =', count_row_mix )

                # filter สองอันพร้อมกัน filter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกัน
                
                list_of_label = []
                

                for i in range(count_row_mix):
                    for k in range(data_defect.count()):
                        if data_defect[k].defect_name == queryset[i].defect_name1:
                            count_defect_name1_temp = 1
                            count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name2:
                            count_defect_name2_temp = 1
                            count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name3:
                            count_defect_name3_temp = 1
                            count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name4:
                            count_defect_name4_temp = 1
                            count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name5:
                            count_defect_name5_temp = 1
                            count_defect_name5 = count_defect_name5 + count_defect_name5_temp
                            list_of_label.append(data_defect[k].defect_name)
                        
                        
                        # count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5
        
                print(list_of_label)

                Counter(list_of_label).keys() # equals to list(set(words))
                Counter(list_of_label).values() # counts the elements' frequency
                label_list = list(Counter(list_of_label).keys())
                data_list = list(Counter(list_of_label).values())
                print(len(label_list))
                for i in range(len(label_list)):  # จัดเก็บลง label กับ data
                    labels.append(label_list[i])   
                    data.append(data_list[i])

                print(labels)
                print(data)

                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':objModeldefect.defect_name,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                    
                })    

            #-------------------->>>>> inputDefect NO ALL  + shift NO ALL  + NO Date        
            else:        
            # filter สองอันพร้อมกัน filter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกัน
                print("#-------------------->>>>> inputDefect NO ALL  + shift NO ALL  + NO Date  8")
                objModeldefect = Defect.objects.get(id=inputDefect)
                queryset = modelGlassWithDefect.objects.filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name)).filter(shift=shift)

                count_row_mix = modelGlassWithDefect.objects.filter(Q(defect_name1=objModeldefect.defect_name) 
                | Q(defect_name2=objModeldefect.defect_name) 
                | Q(defect_name3=objModeldefect.defect_name) 
                | Q(defect_name4=objModeldefect.defect_name) 
                | Q(defect_name5=objModeldefect.defect_name)).filter(shift=shift).count()

             
                print('count_row_mix =', count_row_mix )

                # filter สองอันพร้อมกัน filter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกันfilter สองอันพร้อมกัน
                
                list_of_label = []
                

                for i in range(count_row_mix):
                    for k in range(data_defect.count()):
                        if data_defect[k].defect_name == queryset[i].defect_name1:
                            count_defect_name1_temp = 1
                            count_defect_name1 = count_defect_name1 + count_defect_name1_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name2:
                            count_defect_name2_temp = 1
                            count_defect_name2 = count_defect_name2 + count_defect_name2_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name3:
                            count_defect_name3_temp = 1
                            count_defect_name3 = count_defect_name3 + count_defect_name3_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name4:
                            count_defect_name4_temp = 1
                            count_defect_name4 = count_defect_name4 + count_defect_name4_temp
                            list_of_label.append(data_defect[k].defect_name)
                            
                        if data_defect[k].defect_name == queryset[i].defect_name5:
                            count_defect_name5_temp = 1
                            count_defect_name5 = count_defect_name5 + count_defect_name5_temp
                            list_of_label.append(data_defect[k].defect_name)
                        
                        
                        # count_defect_all = count_defect_name1 + count_defect_name2 + count_defect_name3 + count_defect_name4 + count_defect_name5
        
                print(list_of_label)

                Counter(list_of_label).keys() # equals to list(set(words))
                Counter(list_of_label).values() # counts the elements' frequency
                label_list = list(Counter(list_of_label).keys())
                data_list = list(Counter(list_of_label).values())
                print(len(label_list))
                for i in range(len(label_list)):  # จัดเก็บลง label กับ data
                    labels.append(label_list[i])   
                    data.append(data_list[i])

                print(labels)
                print(data)
            
                return  render(request, 'report_filter.html', {
                    'labels': labels,
                    'data': data,
                    'defects':data_defect,
                    'inputDefect':objModeldefect.defect_name,
                    'data_defects':queryset,
                    'inputDefect_id':inputDefect,
                    'shift':shift,
                    'start_date':start_date,
                    'end_date':end_date
                    
                })   






def createForm(request):
    return render(request,'form.html')


def loginForm(request):
    return render(request,'login.html')

def addUser(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    department = request.POST['department']
    shift = request.POST['shift']
    username = request.POST['username']
    password = request.POST['password']
    rePassword = request.POST['rePassword']


    if password == rePassword :
        if User.objects.filter(username=username).exists():
            messages.error(request,'UserName นี้มีคนใช้แล้ว')
          
            return redirect('/createForm')
        else:  
            user = User.objects.create_user(
            username = username,
            password = password,
            first_name = firstname,
            last_name = lastname


            )
            user.save()

            profile = UserProfile.objects.create(
            user_id=user.id,
            department = department,
            shift =  shift

            )
            profile.save()
          

            messages.success(request,'ลงทะเบียนเรียบร้อย')
            return redirect('/')
            
    else:
        messages.error(request,'password ไม่ตรงกัน')
        return redirect('/createForm')




def login(request):
    username = request.POST['username']
    password = request.POST['password']
 
    
    #check username password
    user = auth.authenticate(username=username,password=password)

    if user is not None :
        auth.login(request,user)
        return redirect('/home')
    else :
        messages.error(request, 'username หรือ password ไม่ถูกต้อง')
        return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')



def addDefect(request):
    defect_name = request.POST['defect_name']

    defect_add = Defect.objects.create(
            defect_name = defect_name

            )
    defect_add.save()

    messages.success(request,'Add defect successfully.')

    return redirect('/home')


def addModel(request):
    
    model_code = request.POST['model_code']
    model_name = request.POST['model_name']
    model_desc = request.POST['model_desc']
   

    model_add = modelGlass.objects.create(
    model_code = model_code,
    model_name = model_name,
    model_desc = model_desc

    )
    


    file_img = request.FILES['img']
    file_img_name = request.FILES['img'].name
    fs = FileSystemStorage()
    filename = fs.save(file_img_name,file_img)
    upload_file_url = fs.url(filename)


    model_add.model_image = upload_file_url
    model_add.save()

    messages.success(request,'Add Model successfully.')

    return redirect('/home')

def collector(request):
    data_defect = Defect.objects.all()
    data_glass = modelGlass.objects.all()
    
    return render(request,'collector.html',{'defects':data_defect,'modelGlasss':data_glass})


def choose_defect_on_glass(request):
    global counter
    global datepick_for_check
   

    
    data_defect = Defect.objects.all()
    datepick = request.POST['datepicker']

    if datepick != datepick_for_check :
        counter = 1
       

    # datepick_for_check = datepick

    
    
    shift = request.POST['shift']
    inputModelDesc = request.POST['inputModelDesc']
    # filter โดย ID ของ modelGlass แล้วมาเก็บใน objModelDesc โดยดึง ทั้งแถวมาเลย
    objModelDesc = modelGlass.objects.get(id=inputModelDesc)

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()
    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .

   

    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':objModelDesc.model_desc,
    'inputModelName':objModelDesc.model_name,
    'inputModelCode':objModelDesc.model_code,
    'inputModelImage':objModelDesc.model_image,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter}
    )


def add_have_defect(request):




    global counter
    global datepick_for_check
    global status_defect_for_check
    global status_defect_to_nodefect

    data_defect = Defect.objects.all()
    department = request.POST['department']
    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    status_defect_to_nodefect = 1


    

    if status_defect_for_check == 1 :  # 0 คือ ไม่มี defect  /  1  คือ พบ defect

        
        if datepick == datepick_for_check :
            counter = counter + 1
        else:
            counter = counter

            
            

        status_defect_for_check = 0  # 0 คือ ไม่มี defect  /  1  คือ พบ defect
        messages.success(request,'Add defect in model > ' + inputModelCode + ' < successfully.')
        return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
        'inputModelDesc':inputModelDesc,
        'inputModelName':inputModelName,
        'inputModelCode':inputModelCode,
        'inputModelImage':inputModelImage,
        'defects':data_defect,
        'datepick_for_check' : datepick_for_check,
        'counter':counter})

    else:
        messages.error(request, 'Please, choose defect before save.')
        return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
        'inputModelDesc':inputModelDesc,
        'inputModelName':inputModelName,
        'inputModelCode':inputModelCode,
        'inputModelImage':inputModelImage,
        'defects':data_defect,
        'datepick_for_check' : datepick_for_check,
        'counter':counter})


def add_no_defect(request):
    global status_check_before_have_noDefect
    global counter
    global datepick_for_check
    global status_defect_for_check
    global status_defect_to_nodefect
    
    data_defect = Defect.objects.all()
    department = request.POST['department']
    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']


    if status_defect_for_check == 0 :   # 0 คือ ไม่มี defect  /  1  คือ พบ defect
        id_glass_temp = modelGlassWithDefect.objects.values_list('id_glass', flat=True).last() + 1
        status_check_before_have_noDefect = 'yes'
        

        if status_defect_to_nodefect == 1 :   # 0 คือ ไม่มี defect  /  1  คือ พบ defect
            print('if 5')
            counter = request.POST['counter']
            counter = int(counter)
            datepick_for_check = datepick

    
            

            modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                                date_select = datepick,
                                                shift = shift,
                                                model_desc = inputModelDesc,
                                                model_name = inputModelName,
                                                model_code = inputModelCode,
                                                department = department,
                                                number_glass = counter,
                                                status_glass = status_glass,
                                                id_glass = id_glass_temp
                                                                                        
                                        )
            modelGlassWithDefect_add.save()

            
            status_defect_to_nodefect = 0
            
            
        # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
            messages.success(request,'Add No defect in model > ' + inputModelCode + ' < successfully.')
            return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
            'inputModelDesc':inputModelDesc,
            'inputModelName':inputModelName,
            'inputModelCode':inputModelCode,
            'inputModelImage':inputModelImage,
            'defects':data_defect,
            'datepick_for_check' : datepick_for_check,
            'counter':counter + 1})

            

        else:    

            print('if 6')

            if datepick == datepick_for_check :
                counter = counter + 1
            else:
                counter = counter
                

            datepick_for_check = datepick


            modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                                date_select = datepick,
                                                shift = shift,
                                                model_desc = inputModelDesc,
                                                model_name = inputModelName,
                                                model_code = inputModelCode,
                                                department = department,
                                                number_glass = counter,
                                                status_glass = status_glass,
                                                id_glass = id_glass_temp
                                                                                        
                                        )
            modelGlassWithDefect_add.save()
            
        
            
        # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
            messages.success(request,'Add No defect in model > ' + inputModelCode + ' < successfully.')
            return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
            'inputModelDesc':inputModelDesc,
            'inputModelName':inputModelName,
            'inputModelCode':inputModelCode,
            'inputModelImage':inputModelImage,
            'defects':data_defect,
            'datepick_for_check' : datepick_for_check,
            'counter':counter + 1})

    else:
        messages.error(request, 'Please, Save and go to next Glass first.')
        return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
        'inputModelDesc':inputModelDesc,
        'inputModelName':inputModelName,
        'inputModelCode':inputModelCode,
        'inputModelImage':inputModelImage,
        'defects':data_defect,
        'datepick_for_check' : datepick_for_check,
        'counter':counter})


def add_defect1(request):
    global status_check_before_have_noDefect
    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    data_defect = Defect.objects.all()
    department = request.POST['department']
    datepick = request.POST['datepick']

    
    point_defect = 1
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP1_box1_defect1 = request.POST['inputDefectP1_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP1_box1_defect1)

    
    
    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        shift = shift,
                                        point_defect = point_defect,
                                        model_desc = inputModelDesc, 
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name,
                                      
                                         
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + '@ glass ' + str(counter) + ' < successfully.'  )
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect2(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    
    point_defect = 1
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP1_box2_defect1 = request.POST['inputDefectP1_box2_defect1']
    inputDefectP1_box2_defect2 = request.POST['inputDefectP1_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP1_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP1_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(

                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect3(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 1
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP1_box3_defect1 = request.POST['inputDefectP1_box3_defect1']
    inputDefectP1_box3_defect2 = request.POST['inputDefectP1_box3_defect2']
    inputDefectP1_box3_defect3 = request.POST['inputDefectP1_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP1_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP1_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP1_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect4(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 1
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP1_box4_defect1 = request.POST['inputDefectP1_box4_defect1']
    inputDefectP1_box4_defect2 = request.POST['inputDefectP1_box4_defect2']
    inputDefectP1_box4_defect3 = request.POST['inputDefectP1_box4_defect3']
    inputDefectP1_box4_defect4 = request.POST['inputDefectP1_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP1_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP1_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP1_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP1_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect5(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 1
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP1_box5_defect1 = request.POST['inputDefectP1_box5_defect1']
    inputDefectP1_box5_defect2 = request.POST['inputDefectP1_box5_defect2']
    inputDefectP1_box5_defect3 = request.POST['inputDefectP1_box5_defect3']
    inputDefectP1_box5_defect4 = request.POST['inputDefectP1_box5_defect4']
    inputDefectP1_box5_defect5 = request.POST['inputDefectP1_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP1_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP1_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP1_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP1_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP1_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})


def add_defect6(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 2
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP2_box1_defect1 = request.POST['inputDefectP2_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP2_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect7(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 2
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP2_box2_defect1 = request.POST['inputDefectP2_box2_defect1']
    inputDefectP2_box2_defect2 = request.POST['inputDefectP2_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP2_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP2_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect8(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 2
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP2_box3_defect1 = request.POST['inputDefectP2_box3_defect1']
    inputDefectP2_box3_defect2 = request.POST['inputDefectP2_box3_defect2']
    inputDefectP2_box3_defect3 = request.POST['inputDefectP2_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP2_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP2_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP2_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect9(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 2
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP2_box4_defect1 = request.POST['inputDefectP2_box4_defect1']
    inputDefectP2_box4_defect2 = request.POST['inputDefectP2_box4_defect2']
    inputDefectP2_box4_defect3 = request.POST['inputDefectP2_box4_defect3']
    inputDefectP2_box4_defect4 = request.POST['inputDefectP2_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP2_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP2_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP2_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP2_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect10(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 2
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP2_box5_defect1 = request.POST['inputDefectP2_box5_defect1']
    inputDefectP2_box5_defect2 = request.POST['inputDefectP2_box5_defect2']
    inputDefectP2_box5_defect3 = request.POST['inputDefectP2_box5_defect3']
    inputDefectP2_box5_defect4 = request.POST['inputDefectP2_box5_defect4']
    inputDefectP2_box5_defect5 = request.POST['inputDefectP2_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP2_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP2_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP2_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP2_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP2_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})










def add_defect11(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 3
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP3_box1_defect1 = request.POST['inputDefectP3_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP3_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect12(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 3
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP3_box2_defect1 = request.POST['inputDefectP3_box2_defect1']
    inputDefectP3_box2_defect2 = request.POST['inputDefectP3_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP3_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP3_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect13(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 3
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP3_box3_defect1 = request.POST['inputDefectP3_box3_defect1']
    inputDefectP3_box3_defect2 = request.POST['inputDefectP3_box3_defect2']
    inputDefectP3_box3_defect3 = request.POST['inputDefectP3_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP3_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP3_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP3_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect14(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 3
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP3_box4_defect1 = request.POST['inputDefectP3_box4_defect1']
    inputDefectP3_box4_defect2 = request.POST['inputDefectP3_box4_defect2']
    inputDefectP3_box4_defect3 = request.POST['inputDefectP3_box4_defect3']
    inputDefectP3_box4_defect4 = request.POST['inputDefectP3_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP3_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP3_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP3_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP3_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect15(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 3
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP3_box5_defect1 = request.POST['inputDefectP3_box5_defect1']
    inputDefectP3_box5_defect2 = request.POST['inputDefectP3_box5_defect2']
    inputDefectP3_box5_defect3 = request.POST['inputDefectP3_box5_defect3']
    inputDefectP3_box5_defect4 = request.POST['inputDefectP3_box5_defect4']
    inputDefectP3_box5_defect5 = request.POST['inputDefectP3_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP3_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP3_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP3_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP3_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP3_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})






def add_defect16(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 4
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP4_box1_defect1 = request.POST['inputDefectP4_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP4_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect17(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 4
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP4_box2_defect1 = request.POST['inputDefectP4_box2_defect1']
    inputDefectP4_box2_defect2 = request.POST['inputDefectP4_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP4_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP4_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect18(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 4
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP4_box3_defect1 = request.POST['inputDefectP4_box3_defect1']
    inputDefectP4_box3_defect2 = request.POST['inputDefectP4_box3_defect2']
    inputDefectP4_box3_defect3 = request.POST['inputDefectP4_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP4_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP4_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP4_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect19(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 4
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP4_box4_defect1 = request.POST['inputDefectP4_box4_defect1']
    inputDefectP4_box4_defect2 = request.POST['inputDefectP4_box4_defect2']
    inputDefectP4_box4_defect3 = request.POST['inputDefectP4_box4_defect3']
    inputDefectP4_box4_defect4 = request.POST['inputDefectP4_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP4_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP4_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP4_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP4_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect20(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 4
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP4_box5_defect1 = request.POST['inputDefectP4_box5_defect1']
    inputDefectP4_box5_defect2 = request.POST['inputDefectP4_box5_defect2']
    inputDefectP4_box5_defect3 = request.POST['inputDefectP4_box5_defect3']
    inputDefectP4_box5_defect4 = request.POST['inputDefectP4_box5_defect4']
    inputDefectP4_box5_defect5 = request.POST['inputDefectP4_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP4_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP4_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP4_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP4_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP4_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})




def add_defect21(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 5
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP5_box1_defect1 = request.POST['inputDefectP5_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP5_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect22(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 5
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP5_box2_defect1 = request.POST['inputDefectP5_box2_defect1']
    inputDefectP5_box2_defect2 = request.POST['inputDefectP5_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP5_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP5_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect23(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 5
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP5_box3_defect1 = request.POST['inputDefectP5_box3_defect1']
    inputDefectP5_box3_defect2 = request.POST['inputDefectP5_box3_defect2']
    inputDefectP5_box3_defect3 = request.POST['inputDefectP5_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP5_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP5_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP5_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect24(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 5
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP5_box4_defect1 = request.POST['inputDefectP5_box4_defect1']
    inputDefectP5_box4_defect2 = request.POST['inputDefectP5_box4_defect2']
    inputDefectP5_box4_defect3 = request.POST['inputDefectP5_box4_defect3']
    inputDefectP5_box4_defect4 = request.POST['inputDefectP5_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP5_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP5_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP5_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP5_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect25(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 5
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP5_box5_defect1 = request.POST['inputDefectP5_box5_defect1']
    inputDefectP5_box5_defect2 = request.POST['inputDefectP5_box5_defect2']
    inputDefectP5_box5_defect3 = request.POST['inputDefectP5_box5_defect3']
    inputDefectP5_box5_defect4 = request.POST['inputDefectP5_box5_defect4']
    inputDefectP5_box5_defect5 = request.POST['inputDefectP5_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP5_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP5_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP5_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP5_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP5_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})





def add_defect26(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 6
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP6_box1_defect1 = request.POST['inputDefectP6_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP6_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect27(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 6
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP6_box2_defect1 = request.POST['inputDefectP6_box2_defect1']
    inputDefectP6_box2_defect2 = request.POST['inputDefectP6_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP6_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP6_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect28(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 6
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP6_box3_defect1 = request.POST['inputDefectP6_box3_defect1']
    inputDefectP6_box3_defect2 = request.POST['inputDefectP6_box3_defect2']
    inputDefectP6_box3_defect3 = request.POST['inputDefectP6_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP6_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP6_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP6_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect29(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 6
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP6_box4_defect1 = request.POST['inputDefectP6_box4_defect1']
    inputDefectP6_box4_defect2 = request.POST['inputDefectP6_box4_defect2']
    inputDefectP6_box4_defect3 = request.POST['inputDefectP6_box4_defect3']
    inputDefectP6_box4_defect4 = request.POST['inputDefectP6_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP6_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP6_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP6_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP6_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect30(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
 
    point_defect = 6
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP6_box5_defect1 = request.POST['inputDefectP6_box5_defect1']
    inputDefectP6_box5_defect2 = request.POST['inputDefectP6_box5_defect2']
    inputDefectP6_box5_defect3 = request.POST['inputDefectP6_box5_defect3']
    inputDefectP6_box5_defect4 = request.POST['inputDefectP6_box5_defect4']
    inputDefectP6_box5_defect5 = request.POST['inputDefectP6_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP6_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP6_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP6_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP6_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP6_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})





def add_defect31(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 7
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP7_box1_defect1 = request.POST['inputDefectP7_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP7_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect32(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 7
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP7_box2_defect1 = request.POST['inputDefectP7_box2_defect1']
    inputDefectP7_box2_defect2 = request.POST['inputDefectP7_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP7_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP7_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect33(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 7
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP7_box3_defect1 = request.POST['inputDefectP7_box3_defect1']
    inputDefectP7_box3_defect2 = request.POST['inputDefectP7_box3_defect2']
    inputDefectP7_box3_defect3 = request.POST['inputDefectP7_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP7_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP7_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP7_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect34(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 7
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP7_box4_defect1 = request.POST['inputDefectP7_box4_defect1']
    inputDefectP7_box4_defect2 = request.POST['inputDefectP7_box4_defect2']
    inputDefectP7_box4_defect3 = request.POST['inputDefectP7_box4_defect3']
    inputDefectP7_box4_defect4 = request.POST['inputDefectP7_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP7_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP7_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP7_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP7_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect35(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 7
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP7_box5_defect1 = request.POST['inputDefectP7_box5_defect1']
    inputDefectP7_box5_defect2 = request.POST['inputDefectP7_box5_defect2']
    inputDefectP7_box5_defect3 = request.POST['inputDefectP7_box5_defect3']
    inputDefectP7_box5_defect4 = request.POST['inputDefectP7_box5_defect4']
    inputDefectP7_box5_defect5 = request.POST['inputDefectP7_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP7_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP7_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP7_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP7_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP7_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})




def add_defect36(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 8
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP8_box1_defect1 = request.POST['inputDefectP8_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP8_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect37(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 8
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP8_box2_defect1 = request.POST['inputDefectP8_box2_defect1']
    inputDefectP8_box2_defect2 = request.POST['inputDefectP8_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP8_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP8_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect38(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 8
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP8_box3_defect1 = request.POST['inputDefectP8_box3_defect1']
    inputDefectP8_box3_defect2 = request.POST['inputDefectP8_box3_defect2']
    inputDefectP8_box3_defect3 = request.POST['inputDefectP8_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP8_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP8_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP8_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect39(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 8
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP8_box4_defect1 = request.POST['inputDefectP8_box4_defect1']
    inputDefectP8_box4_defect2 = request.POST['inputDefectP8_box4_defect2']
    inputDefectP8_box4_defect3 = request.POST['inputDefectP8_box4_defect3']
    inputDefectP8_box4_defect4 = request.POST['inputDefectP8_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP8_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP8_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP8_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP8_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect40(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 8
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP8_box5_defect1 = request.POST['inputDefectP8_box5_defect1']
    inputDefectP8_box5_defect2 = request.POST['inputDefectP8_box5_defect2']
    inputDefectP8_box5_defect3 = request.POST['inputDefectP8_box5_defect3']
    inputDefectP8_box5_defect4 = request.POST['inputDefectP8_box5_defect4']
    inputDefectP8_box5_defect5 = request.POST['inputDefectP8_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP8_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP8_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP8_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP8_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP8_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})




def add_defect41(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 9
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP9_box1_defect1 = request.POST['inputDefectP9_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP9_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect42(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 9
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP9_box2_defect1 = request.POST['inputDefectP9_box2_defect1']
    inputDefectP9_box2_defect2 = request.POST['inputDefectP9_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP9_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP9_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect43(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 9
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP9_box3_defect1 = request.POST['inputDefectP9_box3_defect1']
    inputDefectP9_box3_defect2 = request.POST['inputDefectP9_box3_defect2']
    inputDefectP9_box3_defect3 = request.POST['inputDefectP9_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP9_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP9_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP9_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect44(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 9
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP9_box4_defect1 = request.POST['inputDefectP9_box4_defect1']
    inputDefectP9_box4_defect2 = request.POST['inputDefectP9_box4_defect2']
    inputDefectP9_box4_defect3 = request.POST['inputDefectP9_box4_defect3']
    inputDefectP9_box4_defect4 = request.POST['inputDefectP9_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP9_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP9_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP9_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP9_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect45(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 9
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP9_box5_defect1 = request.POST['inputDefectP9_box5_defect1']
    inputDefectP9_box5_defect2 = request.POST['inputDefectP9_box5_defect2']
    inputDefectP9_box5_defect3 = request.POST['inputDefectP9_box5_defect3']
    inputDefectP9_box5_defect4 = request.POST['inputDefectP9_box5_defect4']
    inputDefectP9_box5_defect5 = request.POST['inputDefectP9_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP9_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP9_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP9_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP9_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP9_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})




def add_defect46(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 10
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP10_box1_defect1 = request.POST['inputDefectP10_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP10_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect47(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 10
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP10_box2_defect1 = request.POST['inputDefectP10_box2_defect1']
    inputDefectP10_box2_defect2 = request.POST['inputDefectP10_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP10_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP10_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect48(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 10
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP10_box3_defect1 = request.POST['inputDefectP10_box3_defect1']
    inputDefectP10_box3_defect2 = request.POST['inputDefectP10_box3_defect2']
    inputDefectP10_box3_defect3 = request.POST['inputDefectP10_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP10_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP10_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP10_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect49(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 10
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP10_box4_defect1 = request.POST['inputDefectP10_box4_defect1']
    inputDefectP10_box4_defect2 = request.POST['inputDefectP10_box4_defect2']
    inputDefectP10_box4_defect3 = request.POST['inputDefectP10_box4_defect3']
    inputDefectP10_box4_defect4 = request.POST['inputDefectP10_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP10_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP10_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP10_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP10_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect50(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 10
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP10_box5_defect1 = request.POST['inputDefectP10_box5_defect1']
    inputDefectP10_box5_defect2 = request.POST['inputDefectP10_box5_defect2']
    inputDefectP10_box5_defect3 = request.POST['inputDefectP10_box5_defect3']
    inputDefectP10_box5_defect4 = request.POST['inputDefectP10_box5_defect4']
    inputDefectP10_box5_defect5 = request.POST['inputDefectP10_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP10_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP10_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP10_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP10_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP10_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})




def add_defect51(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 11
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP11_box1_defect1 = request.POST['inputDefectP11_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP11_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect52(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 11
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP11_box2_defect1 = request.POST['inputDefectP11_box2_defect1']
    inputDefectP11_box2_defect2 = request.POST['inputDefectP11_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP11_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP11_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect53(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 11
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP11_box3_defect1 = request.POST['inputDefectP11_box3_defect1']
    inputDefectP11_box3_defect2 = request.POST['inputDefectP11_box3_defect2']
    inputDefectP11_box3_defect3 = request.POST['inputDefectP11_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP11_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP11_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP11_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect54(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 11
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP11_box4_defect1 = request.POST['inputDefectP11_box4_defect1']
    inputDefectP11_box4_defect2 = request.POST['inputDefectP11_box4_defect2']
    inputDefectP11_box4_defect3 = request.POST['inputDefectP11_box4_defect3']
    inputDefectP11_box4_defect4 = request.POST['inputDefectP11_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP11_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP11_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP11_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP11_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect55(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 11
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP11_box5_defect1 = request.POST['inputDefectP11_box5_defect1']
    inputDefectP11_box5_defect2 = request.POST['inputDefectP11_box5_defect2']
    inputDefectP11_box5_defect3 = request.POST['inputDefectP11_box5_defect3']
    inputDefectP11_box5_defect4 = request.POST['inputDefectP11_box5_defect4']
    inputDefectP11_box5_defect5 = request.POST['inputDefectP11_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP11_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP11_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP11_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP11_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP11_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})





def add_defect56(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 12
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP12_box1_defect1 = request.POST['inputDefectP12_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP12_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect57(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 12
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP12_box2_defect1 = request.POST['inputDefectP12_box2_defect1']
    inputDefectP12_box2_defect2 = request.POST['inputDefectP12_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP12_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP12_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect58(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 12
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP12_box3_defect1 = request.POST['inputDefectP12_box3_defect1']
    inputDefectP12_box3_defect2 = request.POST['inputDefectP12_box3_defect2']
    inputDefectP12_box3_defect3 = request.POST['inputDefectP12_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP12_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP12_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP12_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect59(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 12
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP12_box4_defect1 = request.POST['inputDefectP12_box4_defect1']
    inputDefectP12_box4_defect2 = request.POST['inputDefectP12_box4_defect2']
    inputDefectP12_box4_defect3 = request.POST['inputDefectP12_box4_defect3']
    inputDefectP12_box4_defect4 = request.POST['inputDefectP12_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP12_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP12_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP12_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP12_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect60(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 12
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP12_box5_defect1 = request.POST['inputDefectP12_box5_defect1']
    inputDefectP12_box5_defect2 = request.POST['inputDefectP12_box5_defect2']
    inputDefectP12_box5_defect3 = request.POST['inputDefectP12_box5_defect3']
    inputDefectP12_box5_defect4 = request.POST['inputDefectP12_box5_defect4']
    inputDefectP12_box5_defect5 = request.POST['inputDefectP12_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP12_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP12_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP12_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP12_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP12_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})







def add_defect61(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 13
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP13_box1_defect1 = request.POST['inputDefectP13_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP13_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect62(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 13
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP13_box2_defect1 = request.POST['inputDefectP13_box2_defect1']
    inputDefectP13_box2_defect2 = request.POST['inputDefectP13_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP13_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP13_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect63(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 13
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP13_box3_defect1 = request.POST['inputDefectP13_box3_defect1']
    inputDefectP13_box3_defect2 = request.POST['inputDefectP13_box3_defect2']
    inputDefectP13_box3_defect3 = request.POST['inputDefectP13_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP13_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP13_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP13_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect64(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 13
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP13_box4_defect1 = request.POST['inputDefectP13_box4_defect1']
    inputDefectP13_box4_defect2 = request.POST['inputDefectP13_box4_defect2']
    inputDefectP13_box4_defect3 = request.POST['inputDefectP13_box4_defect3']
    inputDefectP13_box4_defect4 = request.POST['inputDefectP13_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP13_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP13_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP13_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP13_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect65(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 13
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP13_box5_defect1 = request.POST['inputDefectP13_box5_defect1']
    inputDefectP13_box5_defect2 = request.POST['inputDefectP13_box5_defect2']
    inputDefectP13_box5_defect3 = request.POST['inputDefectP13_box5_defect3']
    inputDefectP13_box5_defect4 = request.POST['inputDefectP13_box5_defect4']
    inputDefectP13_box5_defect5 = request.POST['inputDefectP13_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP13_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP13_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP13_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP13_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP13_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})




def add_defect66(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 14
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP14_box1_defect1 = request.POST['inputDefectP14_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP14_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect67(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 14
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP14_box2_defect1 = request.POST['inputDefectP14_box2_defect1']
    inputDefectP14_box2_defect2 = request.POST['inputDefectP14_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP14_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP14_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect68(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 14
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP14_box3_defect1 = request.POST['inputDefectP14_box3_defect1']
    inputDefectP14_box3_defect2 = request.POST['inputDefectP14_box3_defect2']
    inputDefectP14_box3_defect3 = request.POST['inputDefectP14_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP14_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP14_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP14_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect69(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 14
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP14_box4_defect1 = request.POST['inputDefectP14_box4_defect1']
    inputDefectP14_box4_defect2 = request.POST['inputDefectP14_box4_defect2']
    inputDefectP14_box4_defect3 = request.POST['inputDefectP14_box4_defect3']
    inputDefectP14_box4_defect4 = request.POST['inputDefectP14_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP14_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP14_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP14_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP14_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect70(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 14
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP14_box5_defect1 = request.POST['inputDefectP14_box5_defect1']
    inputDefectP14_box5_defect2 = request.POST['inputDefectP14_box5_defect2']
    inputDefectP14_box5_defect3 = request.POST['inputDefectP14_box5_defect3']
    inputDefectP14_box5_defect4 = request.POST['inputDefectP14_box5_defect4']
    inputDefectP14_box5_defect5 = request.POST['inputDefectP14_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP14_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP14_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP14_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP14_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP14_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect71(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 15
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP15_box1_defect1 = request.POST['inputDefectP15_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP15_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect72(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 15
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP15_box2_defect1 = request.POST['inputDefectP15_box2_defect1']
    inputDefectP15_box2_defect2 = request.POST['inputDefectP15_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP15_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP15_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect73(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 15
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP15_box3_defect1 = request.POST['inputDefectP15_box3_defect1']
    inputDefectP15_box3_defect2 = request.POST['inputDefectP15_box3_defect2']
    inputDefectP15_box3_defect3 = request.POST['inputDefectP15_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP15_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP15_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP15_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect74(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 15
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP15_box4_defect1 = request.POST['inputDefectP15_box4_defect1']
    inputDefectP15_box4_defect2 = request.POST['inputDefectP15_box4_defect2']
    inputDefectP15_box4_defect3 = request.POST['inputDefectP15_box4_defect3']
    inputDefectP15_box4_defect4 = request.POST['inputDefectP15_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP15_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP15_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP15_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP15_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect75(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 15
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP15_box5_defect1 = request.POST['inputDefectP15_box5_defect1']
    inputDefectP15_box5_defect2 = request.POST['inputDefectP15_box5_defect2']
    inputDefectP15_box5_defect3 = request.POST['inputDefectP15_box5_defect3']
    inputDefectP15_box5_defect4 = request.POST['inputDefectP15_box5_defect4']
    inputDefectP15_box5_defect5 = request.POST['inputDefectP15_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP15_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP15_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP15_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP15_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP15_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect76(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 16
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP16_box1_defect1 = request.POST['inputDefectP16_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP16_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect77(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 16
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP16_box2_defect1 = request.POST['inputDefectP16_box2_defect1']
    inputDefectP16_box2_defect2 = request.POST['inputDefectP16_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP16_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP16_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect78(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 16
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP16_box3_defect1 = request.POST['inputDefectP16_box3_defect1']
    inputDefectP16_box3_defect2 = request.POST['inputDefectP16_box3_defect2']
    inputDefectP16_box3_defect3 = request.POST['inputDefectP16_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP16_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP16_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP16_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect79(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 16
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP16_box4_defect1 = request.POST['inputDefectP16_box4_defect1']
    inputDefectP16_box4_defect2 = request.POST['inputDefectP16_box4_defect2']
    inputDefectP16_box4_defect3 = request.POST['inputDefectP16_box4_defect3']
    inputDefectP16_box4_defect4 = request.POST['inputDefectP16_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP16_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP16_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP16_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP16_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect80(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 16
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP16_box5_defect1 = request.POST['inputDefectP16_box5_defect1']
    inputDefectP16_box5_defect2 = request.POST['inputDefectP16_box5_defect2']
    inputDefectP16_box5_defect3 = request.POST['inputDefectP16_box5_defect3']
    inputDefectP16_box5_defect4 = request.POST['inputDefectP16_box5_defect4']
    inputDefectP16_box5_defect5 = request.POST['inputDefectP16_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP16_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP16_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP16_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP16_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP16_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect81(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 17
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP17_box1_defect1 = request.POST['inputDefectP17_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP17_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect82(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 17
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP17_box2_defect1 = request.POST['inputDefectP17_box2_defect1']
    inputDefectP17_box2_defect2 = request.POST['inputDefectP17_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP17_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP17_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect83(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 17
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP17_box3_defect1 = request.POST['inputDefectP17_box3_defect1']
    inputDefectP17_box3_defect2 = request.POST['inputDefectP17_box3_defect2']
    inputDefectP17_box3_defect3 = request.POST['inputDefectP17_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP17_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP17_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP17_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect84(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 17
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP17_box4_defect1 = request.POST['inputDefectP17_box4_defect1']
    inputDefectP17_box4_defect2 = request.POST['inputDefectP17_box4_defect2']
    inputDefectP17_box4_defect3 = request.POST['inputDefectP17_box4_defect3']
    inputDefectP17_box4_defect4 = request.POST['inputDefectP17_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP17_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP17_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP17_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP17_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect85(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 17
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP17_box5_defect1 = request.POST['inputDefectP17_box5_defect1']
    inputDefectP17_box5_defect2 = request.POST['inputDefectP17_box5_defect2']
    inputDefectP17_box5_defect3 = request.POST['inputDefectP17_box5_defect3']
    inputDefectP17_box5_defect4 = request.POST['inputDefectP17_box5_defect4']
    inputDefectP17_box5_defect5 = request.POST['inputDefectP17_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP17_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP17_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP17_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP17_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP17_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect86(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 18
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP18_box1_defect1 = request.POST['inputDefectP18_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP18_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect87(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 18
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP18_box2_defect1 = request.POST['inputDefectP18_box2_defect1']
    inputDefectP18_box2_defect2 = request.POST['inputDefectP18_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP18_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP18_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect88(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 18
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP18_box3_defect1 = request.POST['inputDefectP18_box3_defect1']
    inputDefectP18_box3_defect2 = request.POST['inputDefectP18_box3_defect2']
    inputDefectP18_box3_defect3 = request.POST['inputDefectP18_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP18_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP18_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP18_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect89(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 18
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP18_box4_defect1 = request.POST['inputDefectP18_box4_defect1']
    inputDefectP18_box4_defect2 = request.POST['inputDefectP18_box4_defect2']
    inputDefectP18_box4_defect3 = request.POST['inputDefectP18_box4_defect3']
    inputDefectP18_box4_defect4 = request.POST['inputDefectP18_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP18_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP18_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP18_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP18_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect90(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 18
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP18_box5_defect1 = request.POST['inputDefectP18_box5_defect1']
    inputDefectP18_box5_defect2 = request.POST['inputDefectP18_box5_defect2']
    inputDefectP18_box5_defect3 = request.POST['inputDefectP18_box5_defect3']
    inputDefectP18_box5_defect4 = request.POST['inputDefectP18_box5_defect4']
    inputDefectP18_box5_defect5 = request.POST['inputDefectP18_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP18_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP18_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP18_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP18_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP18_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect91(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 19
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP19_box1_defect1 = request.POST['inputDefectP19_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP19_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect92(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 19
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP19_box2_defect1 = request.POST['inputDefectP19_box2_defect1']
    inputDefectP19_box2_defect2 = request.POST['inputDefectP19_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP19_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP19_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect93(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 19
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP19_box3_defect1 = request.POST['inputDefectP19_box3_defect1']
    inputDefectP19_box3_defect2 = request.POST['inputDefectP19_box3_defect2']
    inputDefectP19_box3_defect3 = request.POST['inputDefectP19_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP19_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP19_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP19_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect94(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 19
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP19_box4_defect1 = request.POST['inputDefectP19_box4_defect1']
    inputDefectP19_box4_defect2 = request.POST['inputDefectP19_box4_defect2']
    inputDefectP19_box4_defect3 = request.POST['inputDefectP19_box4_defect3']
    inputDefectP19_box4_defect4 = request.POST['inputDefectP19_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP19_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP19_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP19_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP19_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect95(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 19
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP19_box5_defect1 = request.POST['inputDefectP19_box5_defect1']
    inputDefectP19_box5_defect2 = request.POST['inputDefectP19_box5_defect2']
    inputDefectP19_box5_defect3 = request.POST['inputDefectP19_box5_defect3']
    inputDefectP19_box5_defect4 = request.POST['inputDefectP19_box5_defect4']
    inputDefectP19_box5_defect5 = request.POST['inputDefectP19_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP19_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP19_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP19_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP19_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP19_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect96(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 20
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP20_box1_defect1 = request.POST['inputDefectP20_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP20_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect97(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 20
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP20_box2_defect1 = request.POST['inputDefectP20_box2_defect1']
    inputDefectP20_box2_defect2 = request.POST['inputDefectP20_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP20_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP20_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect98(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 20
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP20_box3_defect1 = request.POST['inputDefectP20_box3_defect1']
    inputDefectP20_box3_defect2 = request.POST['inputDefectP20_box3_defect2']
    inputDefectP20_box3_defect3 = request.POST['inputDefectP20_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP20_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP20_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP20_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect99(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 20
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP20_box4_defect1 = request.POST['inputDefectP20_box4_defect1']
    inputDefectP20_box4_defect2 = request.POST['inputDefectP20_box4_defect2']
    inputDefectP20_box4_defect3 = request.POST['inputDefectP20_box4_defect3']
    inputDefectP20_box4_defect4 = request.POST['inputDefectP20_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP20_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP20_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP20_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP20_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect100(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 20
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP20_box5_defect1 = request.POST['inputDefectP20_box5_defect1']
    inputDefectP20_box5_defect2 = request.POST['inputDefectP20_box5_defect2']
    inputDefectP20_box5_defect3 = request.POST['inputDefectP20_box5_defect3']
    inputDefectP20_box5_defect4 = request.POST['inputDefectP20_box5_defect4']
    inputDefectP20_box5_defect5 = request.POST['inputDefectP20_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP20_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP20_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP20_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP20_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP20_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect101(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 21
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP21_box1_defect1 = request.POST['inputDefectP21_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP21_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect102(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 21
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP21_box2_defect1 = request.POST['inputDefectP21_box2_defect1']
    inputDefectP21_box2_defect2 = request.POST['inputDefectP21_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP21_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP21_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect103(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 21
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP21_box3_defect1 = request.POST['inputDefectP21_box3_defect1']
    inputDefectP21_box3_defect2 = request.POST['inputDefectP21_box3_defect2']
    inputDefectP21_box3_defect3 = request.POST['inputDefectP21_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP21_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP21_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP21_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect104(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 21
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP21_box4_defect1 = request.POST['inputDefectP21_box4_defect1']
    inputDefectP21_box4_defect2 = request.POST['inputDefectP21_box4_defect2']
    inputDefectP21_box4_defect3 = request.POST['inputDefectP21_box4_defect3']
    inputDefectP21_box4_defect4 = request.POST['inputDefectP21_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP21_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP21_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP21_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP21_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect105(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 21
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP21_box5_defect1 = request.POST['inputDefectP21_box5_defect1']
    inputDefectP21_box5_defect2 = request.POST['inputDefectP21_box5_defect2']
    inputDefectP21_box5_defect3 = request.POST['inputDefectP21_box5_defect3']
    inputDefectP21_box5_defect4 = request.POST['inputDefectP21_box5_defect4']
    inputDefectP21_box5_defect5 = request.POST['inputDefectP21_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP21_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP21_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP21_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP21_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP21_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect106(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 22
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP22_box1_defect1 = request.POST['inputDefectP22_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP22_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect107(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 22
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP22_box2_defect1 = request.POST['inputDefectP22_box2_defect1']
    inputDefectP22_box2_defect2 = request.POST['inputDefectP22_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP22_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP22_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect108(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 22
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP22_box3_defect1 = request.POST['inputDefectP22_box3_defect1']
    inputDefectP22_box3_defect2 = request.POST['inputDefectP22_box3_defect2']
    inputDefectP22_box3_defect3 = request.POST['inputDefectP22_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP22_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP22_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP22_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect109(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 22
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP22_box4_defect1 = request.POST['inputDefectP22_box4_defect1']
    inputDefectP22_box4_defect2 = request.POST['inputDefectP22_box4_defect2']
    inputDefectP22_box4_defect3 = request.POST['inputDefectP22_box4_defect3']
    inputDefectP22_box4_defect4 = request.POST['inputDefectP22_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP22_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP22_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP22_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP22_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect110(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 22
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP22_box5_defect1 = request.POST['inputDefectP22_box5_defect1']
    inputDefectP22_box5_defect2 = request.POST['inputDefectP22_box5_defect2']
    inputDefectP22_box5_defect3 = request.POST['inputDefectP22_box5_defect3']
    inputDefectP22_box5_defect4 = request.POST['inputDefectP22_box5_defect4']
    inputDefectP22_box5_defect5 = request.POST['inputDefectP22_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP22_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP22_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP22_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP22_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP22_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect111(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 23
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP23_box1_defect1 = request.POST['inputDefectP23_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP23_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect112(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 23
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP23_box2_defect1 = request.POST['inputDefectP23_box2_defect1']
    inputDefectP23_box2_defect2 = request.POST['inputDefectP23_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP23_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP23_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect113(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 23
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP23_box3_defect1 = request.POST['inputDefectP23_box3_defect1']
    inputDefectP23_box3_defect2 = request.POST['inputDefectP23_box3_defect2']
    inputDefectP23_box3_defect3 = request.POST['inputDefectP23_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP23_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP23_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP23_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect114(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 23
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP23_box4_defect1 = request.POST['inputDefectP23_box4_defect1']
    inputDefectP23_box4_defect2 = request.POST['inputDefectP23_box4_defect2']
    inputDefectP23_box4_defect3 = request.POST['inputDefectP23_box4_defect3']
    inputDefectP23_box4_defect4 = request.POST['inputDefectP23_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP23_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP23_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP23_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP23_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect115(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 23
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP23_box5_defect1 = request.POST['inputDefectP23_box5_defect1']
    inputDefectP23_box5_defect2 = request.POST['inputDefectP23_box5_defect2']
    inputDefectP23_box5_defect3 = request.POST['inputDefectP23_box5_defect3']
    inputDefectP23_box5_defect4 = request.POST['inputDefectP23_box5_defect4']
    inputDefectP23_box5_defect5 = request.POST['inputDefectP23_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP23_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP23_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP23_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP23_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP23_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect116(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 24
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP24_box1_defect1 = request.POST['inputDefectP24_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP24_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect117(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 24
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP24_box2_defect1 = request.POST['inputDefectP24_box2_defect1']
    inputDefectP24_box2_defect2 = request.POST['inputDefectP24_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP24_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP24_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect118(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 24
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP24_box3_defect1 = request.POST['inputDefectP24_box3_defect1']
    inputDefectP24_box3_defect2 = request.POST['inputDefectP24_box3_defect2']
    inputDefectP24_box3_defect3 = request.POST['inputDefectP24_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP24_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP24_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP24_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect119(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 24
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP24_box4_defect1 = request.POST['inputDefectP24_box4_defect1']
    inputDefectP24_box4_defect2 = request.POST['inputDefectP24_box4_defect2']
    inputDefectP24_box4_defect3 = request.POST['inputDefectP24_box4_defect3']
    inputDefectP24_box4_defect4 = request.POST['inputDefectP24_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP24_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP24_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP24_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP24_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect120(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 24
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP24_box5_defect1 = request.POST['inputDefectP24_box5_defect1']
    inputDefectP24_box5_defect2 = request.POST['inputDefectP24_box5_defect2']
    inputDefectP24_box5_defect3 = request.POST['inputDefectP24_box5_defect3']
    inputDefectP24_box5_defect4 = request.POST['inputDefectP24_box5_defect4']
    inputDefectP24_box5_defect5 = request.POST['inputDefectP24_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP24_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP24_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP24_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP24_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP24_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect121(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 25
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP25_box1_defect1 = request.POST['inputDefectP25_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP25_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect122(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 25
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP25_box2_defect1 = request.POST['inputDefectP25_box2_defect1']
    inputDefectP25_box2_defect2 = request.POST['inputDefectP25_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP25_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP25_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect123(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 25
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP25_box3_defect1 = request.POST['inputDefectP25_box3_defect1']
    inputDefectP25_box3_defect2 = request.POST['inputDefectP25_box3_defect2']
    inputDefectP25_box3_defect3 = request.POST['inputDefectP25_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP25_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP25_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP25_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect124(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 25
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP25_box4_defect1 = request.POST['inputDefectP25_box4_defect1']
    inputDefectP25_box4_defect2 = request.POST['inputDefectP25_box4_defect2']
    inputDefectP25_box4_defect3 = request.POST['inputDefectP25_box4_defect3']
    inputDefectP25_box4_defect4 = request.POST['inputDefectP25_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP25_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP25_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP25_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP25_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect125(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 25
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP25_box5_defect1 = request.POST['inputDefectP25_box5_defect1']
    inputDefectP25_box5_defect2 = request.POST['inputDefectP25_box5_defect2']
    inputDefectP25_box5_defect3 = request.POST['inputDefectP25_box5_defect3']
    inputDefectP25_box5_defect4 = request.POST['inputDefectP25_box5_defect4']
    inputDefectP25_box5_defect5 = request.POST['inputDefectP25_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP25_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP25_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP25_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP25_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP25_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect126(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 26
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP26_box1_defect1 = request.POST['inputDefectP26_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP26_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect127(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 26
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP26_box2_defect1 = request.POST['inputDefectP26_box2_defect1']
    inputDefectP26_box2_defect2 = request.POST['inputDefectP26_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP26_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP26_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect128(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 26
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP26_box3_defect1 = request.POST['inputDefectP26_box3_defect1']
    inputDefectP26_box3_defect2 = request.POST['inputDefectP26_box3_defect2']
    inputDefectP26_box3_defect3 = request.POST['inputDefectP26_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP26_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP26_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP26_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect129(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 26
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP26_box4_defect1 = request.POST['inputDefectP26_box4_defect1']
    inputDefectP26_box4_defect2 = request.POST['inputDefectP26_box4_defect2']
    inputDefectP26_box4_defect3 = request.POST['inputDefectP26_box4_defect3']
    inputDefectP26_box4_defect4 = request.POST['inputDefectP26_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP26_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP26_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP26_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP26_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect130(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 26
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP26_box5_defect1 = request.POST['inputDefectP26_box5_defect1']
    inputDefectP26_box5_defect2 = request.POST['inputDefectP26_box5_defect2']
    inputDefectP26_box5_defect3 = request.POST['inputDefectP26_box5_defect3']
    inputDefectP26_box5_defect4 = request.POST['inputDefectP26_box5_defect4']
    inputDefectP26_box5_defect5 = request.POST['inputDefectP26_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP26_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP26_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP26_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP26_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP26_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect131(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 27
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP27_box1_defect1 = request.POST['inputDefectP27_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP27_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect132(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 27
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP27_box2_defect1 = request.POST['inputDefectP27_box2_defect1']
    inputDefectP27_box2_defect2 = request.POST['inputDefectP27_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP27_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP27_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect133(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 27
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP27_box3_defect1 = request.POST['inputDefectP27_box3_defect1']
    inputDefectP27_box3_defect2 = request.POST['inputDefectP27_box3_defect2']
    inputDefectP27_box3_defect3 = request.POST['inputDefectP27_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP27_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP27_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP27_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect134(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 27
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP27_box4_defect1 = request.POST['inputDefectP27_box4_defect1']
    inputDefectP27_box4_defect2 = request.POST['inputDefectP27_box4_defect2']
    inputDefectP27_box4_defect3 = request.POST['inputDefectP27_box4_defect3']
    inputDefectP27_box4_defect4 = request.POST['inputDefectP27_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP27_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP27_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP27_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP27_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect135(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 27
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP27_box5_defect1 = request.POST['inputDefectP27_box5_defect1']
    inputDefectP27_box5_defect2 = request.POST['inputDefectP27_box5_defect2']
    inputDefectP27_box5_defect3 = request.POST['inputDefectP27_box5_defect3']
    inputDefectP27_box5_defect4 = request.POST['inputDefectP27_box5_defect4']
    inputDefectP27_box5_defect5 = request.POST['inputDefectP27_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP27_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP27_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP27_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP27_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP27_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect136(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 28
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP28_box1_defect1 = request.POST['inputDefectP28_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP28_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect137(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 28
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP28_box2_defect1 = request.POST['inputDefectP28_box2_defect1']
    inputDefectP28_box2_defect2 = request.POST['inputDefectP28_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP28_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP28_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect138(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 28
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP28_box3_defect1 = request.POST['inputDefectP28_box3_defect1']
    inputDefectP28_box3_defect2 = request.POST['inputDefectP28_box3_defect2']
    inputDefectP28_box3_defect3 = request.POST['inputDefectP28_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP28_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP28_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP28_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect139(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 28
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP28_box4_defect1 = request.POST['inputDefectP28_box4_defect1']
    inputDefectP28_box4_defect2 = request.POST['inputDefectP28_box4_defect2']
    inputDefectP28_box4_defect3 = request.POST['inputDefectP28_box4_defect3']
    inputDefectP28_box4_defect4 = request.POST['inputDefectP28_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP28_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP28_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP28_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP28_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect140(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 28
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP28_box5_defect1 = request.POST['inputDefectP28_box5_defect1']
    inputDefectP28_box5_defect2 = request.POST['inputDefectP28_box5_defect2']
    inputDefectP28_box5_defect3 = request.POST['inputDefectP28_box5_defect3']
    inputDefectP28_box5_defect4 = request.POST['inputDefectP28_box5_defect4']
    inputDefectP28_box5_defect5 = request.POST['inputDefectP28_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP28_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP28_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP28_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP28_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP28_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect141(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 29
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP29_box1_defect1 = request.POST['inputDefectP29_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP29_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect142(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 29
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP29_box2_defect1 = request.POST['inputDefectP29_box2_defect1']
    inputDefectP29_box2_defect2 = request.POST['inputDefectP29_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP29_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP29_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect143(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 29
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP29_box3_defect1 = request.POST['inputDefectP29_box3_defect1']
    inputDefectP29_box3_defect2 = request.POST['inputDefectP29_box3_defect2']
    inputDefectP29_box3_defect3 = request.POST['inputDefectP29_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP29_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP29_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP29_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect144(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 29
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP29_box4_defect1 = request.POST['inputDefectP29_box4_defect1']
    inputDefectP29_box4_defect2 = request.POST['inputDefectP29_box4_defect2']
    inputDefectP29_box4_defect3 = request.POST['inputDefectP29_box4_defect3']
    inputDefectP29_box4_defect4 = request.POST['inputDefectP29_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP29_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP29_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP29_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP29_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect145(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 29
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP29_box5_defect1 = request.POST['inputDefectP29_box5_defect1']
    inputDefectP29_box5_defect2 = request.POST['inputDefectP29_box5_defect2']
    inputDefectP29_box5_defect3 = request.POST['inputDefectP29_box5_defect3']
    inputDefectP29_box5_defect4 = request.POST['inputDefectP29_box5_defect4']
    inputDefectP29_box5_defect5 = request.POST['inputDefectP29_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP29_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP29_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP29_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP29_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP29_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect146(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 30
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP30_box1_defect1 = request.POST['inputDefectP30_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP30_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect147(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 30
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP30_box2_defect1 = request.POST['inputDefectP30_box2_defect1']
    inputDefectP30_box2_defect2 = request.POST['inputDefectP30_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP30_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP30_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect148(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 30
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP30_box3_defect1 = request.POST['inputDefectP30_box3_defect1']
    inputDefectP30_box3_defect2 = request.POST['inputDefectP30_box3_defect2']
    inputDefectP30_box3_defect3 = request.POST['inputDefectP30_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP30_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP30_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP30_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect149(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 30
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP30_box4_defect1 = request.POST['inputDefectP30_box4_defect1']
    inputDefectP30_box4_defect2 = request.POST['inputDefectP30_box4_defect2']
    inputDefectP30_box4_defect3 = request.POST['inputDefectP30_box4_defect3']
    inputDefectP30_box4_defect4 = request.POST['inputDefectP30_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP30_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP30_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP30_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP30_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect150(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 30
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP30_box5_defect1 = request.POST['inputDefectP30_box5_defect1']
    inputDefectP30_box5_defect2 = request.POST['inputDefectP30_box5_defect2']
    inputDefectP30_box5_defect3 = request.POST['inputDefectP30_box5_defect3']
    inputDefectP30_box5_defect4 = request.POST['inputDefectP30_box5_defect4']
    inputDefectP30_box5_defect5 = request.POST['inputDefectP30_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP30_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP30_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP30_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP30_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP30_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect151(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 31
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP31_box1_defect1 = request.POST['inputDefectP31_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP31_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect152(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 31
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP31_box2_defect1 = request.POST['inputDefectP31_box2_defect1']
    inputDefectP31_box2_defect2 = request.POST['inputDefectP31_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP31_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP31_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect153(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 31
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP31_box3_defect1 = request.POST['inputDefectP31_box3_defect1']
    inputDefectP31_box3_defect2 = request.POST['inputDefectP31_box3_defect2']
    inputDefectP31_box3_defect3 = request.POST['inputDefectP31_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP31_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP31_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP31_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect154(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 31
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP31_box4_defect1 = request.POST['inputDefectP31_box4_defect1']
    inputDefectP31_box4_defect2 = request.POST['inputDefectP31_box4_defect2']
    inputDefectP31_box4_defect3 = request.POST['inputDefectP31_box4_defect3']
    inputDefectP31_box4_defect4 = request.POST['inputDefectP31_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP31_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP31_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP31_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP31_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect155(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 31
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP31_box5_defect1 = request.POST['inputDefectP31_box5_defect1']
    inputDefectP31_box5_defect2 = request.POST['inputDefectP31_box5_defect2']
    inputDefectP31_box5_defect3 = request.POST['inputDefectP31_box5_defect3']
    inputDefectP31_box5_defect4 = request.POST['inputDefectP31_box5_defect4']
    inputDefectP31_box5_defect5 = request.POST['inputDefectP31_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP31_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP31_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP31_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP31_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP31_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect156(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 32
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP32_box1_defect1 = request.POST['inputDefectP32_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP32_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect157(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 32
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP32_box2_defect1 = request.POST['inputDefectP32_box2_defect1']
    inputDefectP32_box2_defect2 = request.POST['inputDefectP32_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP32_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP32_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect158(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 32
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP32_box3_defect1 = request.POST['inputDefectP32_box3_defect1']
    inputDefectP32_box3_defect2 = request.POST['inputDefectP32_box3_defect2']
    inputDefectP32_box3_defect3 = request.POST['inputDefectP32_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP32_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP32_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP32_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect159(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 32
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP32_box4_defect1 = request.POST['inputDefectP32_box4_defect1']
    inputDefectP32_box4_defect2 = request.POST['inputDefectP32_box4_defect2']
    inputDefectP32_box4_defect3 = request.POST['inputDefectP32_box4_defect3']
    inputDefectP32_box4_defect4 = request.POST['inputDefectP32_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP32_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP32_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP32_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP32_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect160(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 32
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP32_box5_defect1 = request.POST['inputDefectP32_box5_defect1']
    inputDefectP32_box5_defect2 = request.POST['inputDefectP32_box5_defect2']
    inputDefectP32_box5_defect3 = request.POST['inputDefectP32_box5_defect3']
    inputDefectP32_box5_defect4 = request.POST['inputDefectP32_box5_defect4']
    inputDefectP32_box5_defect5 = request.POST['inputDefectP32_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP32_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP32_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP32_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP32_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP32_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect161(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 33
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP33_box1_defect1 = request.POST['inputDefectP33_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP33_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect162(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 33
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP33_box2_defect1 = request.POST['inputDefectP33_box2_defect1']
    inputDefectP33_box2_defect2 = request.POST['inputDefectP33_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP33_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP33_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect163(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 33
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP33_box3_defect1 = request.POST['inputDefectP33_box3_defect1']
    inputDefectP33_box3_defect2 = request.POST['inputDefectP33_box3_defect2']
    inputDefectP33_box3_defect3 = request.POST['inputDefectP33_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP33_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP33_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP33_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect164(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 33
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP33_box4_defect1 = request.POST['inputDefectP33_box4_defect1']
    inputDefectP33_box4_defect2 = request.POST['inputDefectP33_box4_defect2']
    inputDefectP33_box4_defect3 = request.POST['inputDefectP33_box4_defect3']
    inputDefectP33_box4_defect4 = request.POST['inputDefectP33_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP33_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP33_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP33_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP33_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect165(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 33
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP33_box5_defect1 = request.POST['inputDefectP33_box5_defect1']
    inputDefectP33_box5_defect2 = request.POST['inputDefectP33_box5_defect2']
    inputDefectP33_box5_defect3 = request.POST['inputDefectP33_box5_defect3']
    inputDefectP33_box5_defect4 = request.POST['inputDefectP33_box5_defect4']
    inputDefectP33_box5_defect5 = request.POST['inputDefectP33_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP33_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP33_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP33_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP33_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP33_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect166(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 34
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP34_box1_defect1 = request.POST['inputDefectP34_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP34_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect167(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 34
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP34_box2_defect1 = request.POST['inputDefectP34_box2_defect1']
    inputDefectP34_box2_defect2 = request.POST['inputDefectP34_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP34_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP34_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect168(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 34
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP34_box3_defect1 = request.POST['inputDefectP34_box3_defect1']
    inputDefectP34_box3_defect2 = request.POST['inputDefectP34_box3_defect2']
    inputDefectP34_box3_defect3 = request.POST['inputDefectP34_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP34_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP34_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP34_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect169(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 34
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP34_box4_defect1 = request.POST['inputDefectP34_box4_defect1']
    inputDefectP34_box4_defect2 = request.POST['inputDefectP34_box4_defect2']
    inputDefectP34_box4_defect3 = request.POST['inputDefectP34_box4_defect3']
    inputDefectP34_box4_defect4 = request.POST['inputDefectP34_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP34_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP34_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP34_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP34_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect170(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 34
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP34_box5_defect1 = request.POST['inputDefectP34_box5_defect1']
    inputDefectP34_box5_defect2 = request.POST['inputDefectP34_box5_defect2']
    inputDefectP34_box5_defect3 = request.POST['inputDefectP34_box5_defect3']
    inputDefectP34_box5_defect4 = request.POST['inputDefectP34_box5_defect4']
    inputDefectP34_box5_defect5 = request.POST['inputDefectP34_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP34_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP34_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP34_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP34_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP34_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})



def add_defect171(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
   
    point_defect = 35
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP35_box1_defect1 = request.POST['inputDefectP35_box1_defect1']
    
    objModeldefect = Defect.objects.get(id=inputDefectP35_box1_defect1)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect172(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 35
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP35_box2_defect1 = request.POST['inputDefectP35_box2_defect1']
    inputDefectP35_box2_defect2 = request.POST['inputDefectP35_box2_defect2']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP35_box2_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP35_box2_defect2)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect173(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 35
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP35_box3_defect1 = request.POST['inputDefectP35_box3_defect1']
    inputDefectP35_box3_defect2 = request.POST['inputDefectP35_box3_defect2']
    inputDefectP35_box3_defect3 = request.POST['inputDefectP35_box3_defect3']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP35_box3_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP35_box3_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP35_box3_defect3)

    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect174(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 35
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP35_box4_defect1 = request.POST['inputDefectP35_box4_defect1']
    inputDefectP35_box4_defect2 = request.POST['inputDefectP35_box4_defect2']
    inputDefectP35_box4_defect3 = request.POST['inputDefectP35_box4_defect3']
    inputDefectP35_box4_defect4 = request.POST['inputDefectP35_box4_defect4']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP35_box4_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP35_box4_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP35_box4_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP35_box4_defect4)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})

def add_defect175(request):

    global status_check_before_have_noDefect
    global status_defect_for_check
    global counter
    global datepick_for_check

    status_defect_for_check = 1
    
    counter = counter
    
    point_defect = 35
    data_defect = Defect.objects.all()
    department = request.POST['department']

    datepick = request.POST['datepick']
    shift = request.POST['shift']
    status_glass = request.POST['status_glass']
    
    

    datepick_for_check = datepick
    inputModelDesc = request.POST['inputModelDesc']
    inputModelName = request.POST['inputModelName']
    inputModelCode = request.POST['inputModelCode']
    inputModelImage = request.POST['inputModelImage']
    inputDefectP35_box5_defect1 = request.POST['inputDefectP35_box5_defect1']
    inputDefectP35_box5_defect2 = request.POST['inputDefectP35_box5_defect2']
    inputDefectP35_box5_defect3 = request.POST['inputDefectP35_box5_defect3']
    inputDefectP35_box5_defect4 = request.POST['inputDefectP35_box5_defect4']
    inputDefectP35_box5_defect5 = request.POST['inputDefectP35_box5_defect5']
    
    
    objModeldefect1 = Defect.objects.get(id=inputDefectP35_box5_defect1)
    objModeldefect2 = Defect.objects.get(id=inputDefectP35_box5_defect2)
    objModeldefect3 = Defect.objects.get(id=inputDefectP35_box5_defect3)
    objModeldefect4 = Defect.objects.get(id=inputDefectP35_box5_defect4)
    objModeldefect5 = Defect.objects.get(id=inputDefectP35_box5_defect5)


    if modelGlassWithDefect:

        if status_check_before_have_noDefect == 'no':

            if shift == modelGlassWithDefect.objects.values_list('shift', flat=True).last():

                if counter == int(modelGlassWithDefect.objects.values_list('number_glass', flat=True).last()):  # ถ้า counter เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last())
                    print('if 1')

                else :  # ถ้า counter ไม่ !! เท่ากับ num_glass ตัวก่อนหน้า
                    id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1
                    print('if 2')
            
            

        else : # >> status_check_before_have_noDefect == 'yes'
            print('if 3')
            id_glass_temp = int(modelGlassWithDefect.objects.values_list('id_glass', flat=True).last()) + 1 
            status_check_before_have_noDefect = 'no'
            

    else:
        id_glass_temp = 1
        print('if 4')
    

    modelGlassWithDefect_add = modelGlassWithDefect.objects.create(
                                        id_glass = id_glass_temp,
                                        date_select = datepick,
                                        point_defect = point_defect,
                                        shift = shift,
                                        model_desc = inputModelDesc,
                                        model_name = inputModelName,
                                        model_code = inputModelCode,
                                        department = department,
                                        status_glass = status_glass,
                                        number_glass = counter,
                                        defect_name1 = objModeldefect1.defect_name,
                                        defect_name2 = objModeldefect2.defect_name,
                                        defect_name3 = objModeldefect3.defect_name,
                                        defect_name4 = objModeldefect4.defect_name,
                                        defect_name5 = objModeldefect5.defect_name
                                )
    modelGlassWithDefect_add.save()
    

    # data_defect = Defect.objects.all()
    # data_glass = modelGlass.objects.all()

    # objModelDesc.model_desc    objModelDesc.model_name    objModelDesc.model_code     เรียกชื่อ attribute (หัว column) โดย ใส่ .
    messages.success(request,'Add defect > ' + objModeldefect1.defect_name + ',' + objModeldefect2.defect_name + ',' + objModeldefect3.defect_name + ',' + objModeldefect4.defect_name + ',' + objModeldefect5.defect_name + ' < in model > ' + inputModelCode + ' < successfully.')
    return render(request,'choose_defect_on_glass.html',{'shift':shift,'datepick':datepick,
    'inputModelDesc':inputModelDesc,
    'inputModelName':inputModelName,
    'inputModelCode':inputModelCode,
    'inputModelImage':inputModelImage,
    'defects':data_defect,
    'datepick_for_check' : datepick_for_check,
    'counter':counter})












    
    

    





