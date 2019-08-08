from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



class Config_inputPlugin(CMSPluginBase):
    name=u'config_input'
    render_template="config_input.html"

    @csrf_exempt
    def render(self,context,instance,placeholder):
        request = context['request']
        if request.method== 'POST':
            config_file=open('config/configuration','w')
            visual_file=open('damasapp/static/css/visual.css','w')
            visual_file.write('term:after {content: attr(id); font-size: 8pt; color: white; background-color: black}\n')
            visual_file.write('term	 {background-color: #F5DEB3 }\n')
            visual_file.write('term[sem="Other"]	{background-color: #8c8c8c;}\n')
            for i in range(1,10):
                category=request.POST.get('category'+str(i))
                if category!="":
                    tag=request.POST.get('tag'+str(i))
                    color=request.POST.get('color'+str(i))
                    visual_file.write('term[sem="'+str(tag)+'"] {background-color:'+str(color)+';}\n')

                    config_file.write(category+';'+tag+';'+color+'\n')

            visual_file.write('term[type="nest"] {font-size:80%}\n')

            config_file.close()
            visual_file.close()




        return context

    cache = False


plugin_pool.register_plugin(Config_inputPlugin)

































