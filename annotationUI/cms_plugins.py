# -*- coding: utf-8 -*-

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from xml.etree import ElementTree as ET
import urlparse
import os
import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# def convert2XML(predict,text):
#     print "in"
#     with open(text) as textfile:
#         textstring=textfile.read().encode('utf8',errors='replace')
#
#     outstring = ""
#     begin=0
#     with open(predict,"r") as predictfile:
#         for line in predictfile:
#             data=line.split("\t")
#             strt=int(data[1])+1
#             end=int(data[2])+2
#
#             outstring = outstring + textstring[begin:strt].encode('utf8',errors='replace')+ '<term id="T0">' + textstring[strt:end].encode('utf8',errors='replace')+ '</term>'
#             begin=end
#             print outstring
#
#         outstring=outstring+textstring[end:].encode('utf8',errors='replace')
#
#     return outstring


def convert2XML(predict,text):
    with open(text) as textfile:
        textstring=textfile.read()

    outstring=""
    begin=0
    with open(predict,"r") as predictfile:
        for line in predictfile:
            data=line.split("\t")
            strt=int(data[1])+1
            end=int(data[2])+2

            #fixing distorted shift due to encoding
            if textstring[strt:end]==str(data[3]):
                outstring=outstring+textstring[begin:strt]+'<term id="T0">'+str(data[3])+'</term>'
                begin=end
            else:
                match=False
                i=1
                while (match==False):
                    if i==len(textstring):
                        break
                    else:
                        if textstring[strt+i:end+i]==str(data[3]):
                            match=True
                        else:
                            i+=1

                if match:
                    outstring=outstring+textstring[begin:strt+i]+'<term id="T0">'+textstring[strt+i:end+i]+'</term>'
                    begin=end+i
                else:
                    outstring=outstring+textstring[begin:strt]+textstring[strt:end]
                    begin=end


        outstring=outstring+textstring[end:]

    predictfile.close()
    return outstring


def stripdiv(div,outfile):
    out=open(outfile,"w")
    out.write('\n')
    s=re.sub('<[^>]*>', '', div)

    out.write(s)

    out.close()


def list_not_hidden(path):
    files=[]
    for f in os.listdir(path):
        if not f.startswith('.'):
            files.append(f)
    return files


class AnnoUIPlugin(CMSPluginBase):
    name=u'annoUI'
    render_template="annoUI.html"


    @csrf_exempt
    def render(self,context,instance,placeholder):

        request = context['request']

        if request.is_ajax():
            data = json.loads(request.body)
            div = data['div']
            url = data['url']
            action=data['action']
            if action=="save":
                query = urlparse.urlparse(url)
                file_name =urlparse.parse_qs(query.query)['file'][0]
                if div == "":
                    file = open('Kino/' + file_name).read()
                else:
                    with open('Kino/'+file_name, 'w') as f:
                            f.write(div.strip())

        else:
            cat = []
            tag = []
            color = []
            with open('config/configuration') as f:
                my_lines = f.readlines()

            for line in my_lines:
                data = line.split(';')
                cat.append(data[0])
                tag.append(data[1])
                color.append(data[2])

                categories = zip(cat, tag, color)

            context.update({'cat': categories})

            file_list = list_not_hidden('Kino')
            file_name = request.GET.get("file", "")
            sug=request.GET.get("sug", "")

            if file_name == "":
                file = ""
            else:
                with open('Kino/' + file_name) as f:
                    div=f.read()
                if sug=="":
                    file=div
                else:
                    stripdiv(div, "tmp.txt")
                    os.system('scp tmp.txt thaer@tsudalab1.tsudalab.org:chemspot-2.0')
                    os.system('ssh thaer@tsudalab1.tsudalab.org ./shell')
                    # os.system('ssh thaer@tsudalab1.tsudalab.org "cd chemspot-2.0 && java -Xmx16G -jar chemspot.jar -t tmp.txt -o tmp_predict.txt -i """')
                    os.system('scp thaer@tsudalab1.tsudalab.org:chemspot-2.0/tmp_predict.txt .')
                    file=convert2XML('tmp_predict.txt','tmp.txt')
                    context.update({'status':"ChemSpot annotation is done"})

            context.update({'file': file, 'file_list': file_list, 'file_name': file_name})


        return context



    cache = False


plugin_pool.register_plugin(AnnoUIPlugin)






























