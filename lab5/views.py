from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from lab5_app.models import *
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

def home(request):
    return render(request,'home.html')

def studentlist(request):
    s=student.objects.all()
    return render(request,'studentlist.html',{'student_list':s})

def courselist(request):
    c=course.objects.all()
    return render(request,'courselist.html',{'course_list':c})
    
def add_project(request):
    if request.method=="POST":
        form=projectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>Project data successfully saved.</h1><br><hr>Designed and Developed by Sandra Santhosh, USN: 1BI21CS127, Dept. of CSE, BIT")
        else:
            return HttpResponse("<h1>Project details not saved.</h1><br><hr>Designed and Developed by Sandra Santhosh, USN: 1BI21CS127, Dept. of CSE, BIT")
    else:
        form=projectForm()
        return render(request, "projectReg.html",{'form':form})
    

class StudentListView(generic.ListView):
    model=student
    template_name="studentlist2.html"

class StudentDetailView(generic.DetailView):
    model=student
    template_name="studentview.html"

def generateCSV(request):
    courses=course.objects.all()
    resp=HttpResponse(content_type="text/csv")
    resp['Content-Disposition']='attachment; filename=course_data.csv'
    writer=csv.writer(resp)
    writer.writerow(['Course Code','Course Name','Course Credits'])
    for c in courses:
        writer.writerow([c.courseCode,c.courseName,c.courseCredits])
    return resp

def generatePDF(request):
    courses=course.objects.all()
    resp=HttpResponse(content_type="text/pdf")
    resp['Content-Disposition']='attachment; filename=course_data.pdf'
    pdf=SimpleDocTemplate(resp,pagesize=letter)
    table_data=[['Course Code','Course Name','Course Credits']]
    for c in courses:
        table_data.append([c.courseCode,c.courseName,str(c.courseCredits)])
    table=Table(table_data)
    pdf.build([table])
    return resp

def registerAjax(request): 
    if request.method == "POST": 
        sid=request.POST.get("susn") 
        cid=request.POST.get("ccode") 
        studentobj=student.objects.get(id=sid) 
        courseobj=course.objects.get(id=cid) 
        res=studentobj.courses.filter(id=cid) 
        if res: 
            return HttpResponse("<h1>Student already enrolled.</h1>") 
        studentobj.courses.add(courseobj) 
        return HttpResponse("<h1>Student enrolled successfully.</h1>") 
        
    else: 
        studentsobj=student.objects.all() 
        coursesobj=course.objects.all() 
         
        return render(request,"courseRegUsingAjax.html",{"students":studentsobj,"courses":coursesobj})

def enrolledStudentsUsingAjax(request):
    if request.method=="POST":
        cid=request.POST.get("cname")
        
        courseobj=course.objects.get(id=cid)
        studentlistobj=courseobj.student_set.all()
        return render(request,'enrolledStudentsAjax.html',{'course':courseobj,'student_list':studentlistobj})                                                                                   
    else:
        courselist=course.objects.all()
        return render(request,'courseSearchAjax.html',{'Course_List':courselist})

