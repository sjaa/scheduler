import pdb

from django.shortcuts         import render, redirect
#from django.http              import HttpResponseRedirect
#from django.core.urlresolvers import reverse



def top_page(request):
    return render(request, 'top_page/top_page.html', {})


'''
def announce_search(request, foo):
#   return render(request, 'top_page/top_page.html', {})
#   return HttpResponseRedirect(reverse('announce_search'))
    return HttpResponseRedirect(reverse('search'))
'''
