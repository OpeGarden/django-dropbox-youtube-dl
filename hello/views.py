#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from models import Tempmedia
from django.core import serializers
from subprocess import call

import youtube_dl

import threading
import urllib2

import os.path
import dropbox
import json

class MyLogger(object):

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print msg


def my_hook(d):
    if d['status'] == 'finished':
        print 'Done downloading, now converting ...'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def downloadfile(yb,free):
    #url = "http://download.thinkbroadband.com/10MB.zip"
		
    url = youtube_dl.main([yb, '-v', '--socket-timeout', '10000'])
	
    free.status = 33
    free.save()

    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    u = urllib2.urlopen(req)
	
    f = open('/app/10.zip', 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            print "break %s" % (file_size_dl)
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    print "is file name %s" % os.path.isfile('/app/10.zip') 
	
	
    free.status = 66
    free.save()
	
	
    client = dropbox.client.DropboxClient('enter here a valid token')
    print 'linked account: ', client.account_info()
    f = open('/app/10.zip', 'r+')
    response = client.put_file(free.file_name, f, overwrite=True)
    print 'uploaded: ', response
	
    free.status = 99
    free.save()

    #folder_metadata = client.metadata('/')
    #print 'metadata: ', folder_metadata
	
    sh = client.share(free.file_name, short_url=False)
    f, metadata = client.get_file_and_metadata(free.file_name)
    
	
    free.status = 100
	
    free.url = sh['url']
    free.working = False
    free.save()
	
    return [sh, metadata]

	

def youtube(id):
    youtube_dl.main([id, '-v', '--socket-timeout', '10000'])

def youtubeA(id):
    youtube_dl.main([id, '-v', '--socket-timeout', '10000'])
# Create your views here.

def index(request):	
   # downloadfile(request.GET.get('yb', ''))
    free = getFreeSlot()
    free.working = True
    free.url = ''
    free.status = 0
    free.save()
	
    t = threading.Thread(target=downloadfile, args=(request.GET.get('yb', ''),free,))
    t.start()
	
    #return HttpResponse(json.dumps(share()))
    data = serializers.serialize("json", [free,])
    return HttpResponse(data)


def getFreeSlot():
    queryset = Tempmedia.objects.filter(working=False).order_by('-when').reverse()
    ans = queryset[0]
    print ans
    return ans
	
def latestUsed(request):
    data = serializers.serialize("json", [getFreeSlot(),])
    return HttpResponse(data) 
	
def status(request):
    tempmedia = Tempmedia.objects.get(pk=request.GET.get('pk', ''))
    data = serializers.serialize("json", [tempmedia,])
    return HttpResponse(data)


def slots(request):
    queryset = Tempmedia.objects.filter(working=False).order_by('-when').reverse()
    data = serializers.serialize("json", queryset)
    return HttpResponse(data)

	
def db(request):
    Tempmedia.objects.all().delete()
    for x in range(0, 19):
        print "We're on time %d" % (x)
        tempmedia = Tempmedia(file_name="/magnum-opus%d.mp4" % x)
        tempmedia.save()

    data = serializers.serialize("json", Tempmedia.objects.all())
    return HttpResponse(data)