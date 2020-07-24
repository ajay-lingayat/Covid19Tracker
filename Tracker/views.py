from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
import re
import requests
from bs4 import BeautifulSoup
from .track import grab_data, get_data
from .check import check_country
import os

def index( request ):

    List = grab_data()
    cases = List[1]
    deaths = List[2]
    recovered = List[3]
    actives = List[4]
    closed = List[5]
    List = List[0]

    if List:
        First_Row = list()

        count = 0
        List[0].pop(0)
        for i in List[0]:
            First_Row.append(i)
            if count == 12:
                break
            count+=1

        List.pop(0)

        for i in List:
            i.pop(1)
            i.pop(2)
            i.pop(7)
            i.pop(13)
            for j in range(5):
                i.pop(-1)
        
        for k in range(7):
            List.pop(-2)
            
        try:
            Context = {
                'List': List,
                'First_Row': First_Row,
                'cases': cases,
                'deaths': deaths,
                'recovered': recovered,
                'actives': actives,
                'closed': closed,
            }
            t = loader.get_template('Tracker/index.html')
            return HttpResponse(t.render(Context, request))
        except Exception as e:
            print(e)
            return render(request, 'Tracker/index.html')
    else:
        raise Http404("Check Internet Connection!")

def country( request ):
    if request.method == "POST":
        country = request.POST['country']
        return redirect(f'country/{country}')
    else:
        return redirect('/')

def country_name( request, name ):
    if name:
       URL = check_country( name )
       print(URL)
       if URL:
           data = get_data( URL )
           print(data)
           if data:
               cases_int = data[0]
               deaths_int = data[1]
               recovered_int = data[2]
               cases_str = data[3]
               deaths_str = data[4]
               recovered_str = data[5]
               Country_Name = data[6]
               Context = {
                   'cases_int': cases_int,
                   'deaths_int': deaths_int,
                   'recovered_int': recovered_int,
                   'cases_str': cases_str,
                   'deaths_str': deaths_str,
                   'recovered_str': recovered_str,
                   'Country_Name': Country_Name,
               }
               t = loader.get_template('Tracker/country.html')
               print('Found!')
               return HttpResponse(t.render(Context, request))
           else:
               print('Not Found!')
               raise Http404('')
       else:
           print('Not Found!')
           raise Http404('')
    else:
        return redirect('/')

def contact( request ):
    if request.method == 'POST':
       
       fullname = request.POST['fullname']
       email = request.POST['email']
       message = request.POST['message']
       subject = request.POST['subject']

       try:
          From = 'resumebuilder2810@gmail.com'
          To = 'lingayatajay2810@gmail.com'
          text_content = f"Hey Ajay,\n{fullname} has sent you a message!\n\nFullname : {fullname}\nEmail Address : {email}\nMessage : {message}"
          html_content = f"""\
              <html>
                  <body>
                       <h1>
                           Hey Ajay,
                       </h1>
                       <h2>
                           {fullname} has sent you a message!
                       </h2>
                       <h4>
                           Fullname : {fullname}<br>
                           Email Address : {email}<br>
                           Message : {message}
                       </h4>
                  </body>
              </html>
              """
          msg = EmailMultiAlternatives(subject, text_content, From, [To])
          msg.attach_alternative(html_content, 'text/html')
          msg.send()
          messages.success(request, 'Mail Sent Successfully!')
          return redirect('/')
       except Exception as e:
          print(e)
          messages.warning(request, 'Please Check Your Internet Connection!')
          return redirect('contact')
    else:
       return render(request, 'Tracker/contact.html')

def about( request ):
    return render(request, 'Tracker/about.html')