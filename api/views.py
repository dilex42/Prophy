from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count

from .utils import extract_keyphrases
from .models import TextDoc, Keyphrases


# Create your views here.
def main(request):
    obj = TextDoc.objects.all().order_by('-id')
    return render(request,'main.html',context={'obj':obj})

def uploader(request, uploader_id):
    obj = TextDoc.objects.filter(uploader=uploader_id).order_by('-id')
    return render(request,'main.html',context={'obj':obj})


def detail(request, doc_id):
    obj = TextDoc.objects.get(pk=doc_id)
    return render(request,'detail.html',context={'doc':obj})

def top_kp(request):
    top_phrases = Keyphrases.objects.annotate(q_count=Count('textdoc')) \
                                 .order_by('-q_count')[:18]
    return render(request,'top.html',context={'phrases':top_phrases})

def form(request):
    if request.method == 'GET':
        return render(request,'form.html',context={})
    if request.method == 'POST':
        text = request.POST['text']
        desc = request.POST['desc']
        if not desc:
            desc = text[:140]
        uploader = request.POST['uploader']
        ans = extract_keyphrases(text,20)
        doc = TextDoc.objects.create(text=text, description=desc, uploader=uploader)
        if not len(ans):
            return redirect('detail', doc_id=doc.pk)
        for kp in ans:
            if Keyphrases.objects.filter(phrase=kp['phrase']).exists():
                doc.keyphrases.add(Keyphrases.objects.get(phrase=kp['phrase']))
            else :
                k = Keyphrases.objects.create(phrase=kp['phrase'],wiki_title=kp.get('title',''), wiki_url=kp.get('url',None), wiki_dis=kp.get('dis',None))
                doc.keyphrases.add(k)
        return redirect('detail', doc_id=doc.pk)
