import json

from decouple import config
from django.http import HttpResponse
from django.shortcuts import render, redirect
from console_main.views import login_required
from django.contrib import messages
from django.urls import reverse

from adenine.common import Common
from adenine.console import Console

from .forms import UploadFileForm, VerifyAndShowForm
from .models import UploadFile


@login_required
def generate_key(request):
    if request.method == 'POST':
        common = Common()
        did = request.session['did']
        response = common.generate_api_request(config('SHARED_SECRET_ADENINE'), did)
        if response.status:
            api_key = response.api_key
            sent_json = json.dumps({'API_KEY': api_key})
            return HttpResponse(sent_json, content_type='application/JSON')
        else:
            messages.success(request, "Could not generate an API key. Please try again")
            return redirect(reverse('login:generateKey'))
    else:
        return render(request, "service/generateKey.html")


@login_required
def upload_and_sign(request):
    did = request.session['did']
    if request.method == 'POST':
        # Purge old requests for housekeeping.
        UploadFile.objects.filter(did=did).delete()

        private_key = request.POST['private_key']
        api_key = request.POST['api_key']
        form = UploadFileForm(request.POST, request.FILES, initial={'did': did})
        if form.is_valid():
            form.save()
            temp_file = UploadFile.objects.get(did=did)
            file_path = temp_file.uploaded_file.path
            console = Console()
            response = console.upload_and_sign(api_key, private_key, file_path)
            data = json.loads(response.output)
            if response.status:
                temp_file.delete()
                message_hash = data['result']['msg']
                public_key = data['result']['pub']
                signature = data['result']['sig']
                file_hash = data['result']['hash']
                return render(request, "service/uploadAndSign.html",
                              {"message_hash": message_hash, "public_key": public_key, "signature": signature,
                               "file_hash": file_hash, 'output': True})
            else:
                messages.success(request, "File could not be uploaded. Please try again")
                return redirect(reverse('login:uploadAndSign'))

    else:
        form = UploadFileForm(initial={'did': did})
        return render(request, "service/uploadAndSign.html", {'form': form, 'output': False})


@login_required
def verify_and_show(request):
    if request.method == 'POST':
        output = True
        msg = request.POST['message_hash']
        private_key = request.POST['private_key']
        public_key = request.POST['public_key']
        file_hash = request.POST['file_hash']
        signature = request.POST['signature']
        api_key = request.POST['api_key']
        request_input = {
            "msg": msg,
            "pub": public_key,
            "sig": signature,
            "hash": file_hash,
            "private_key": private_key
        }
        console = Console()
        response = console.verify_and_show(api_key, request_input)
        if response.status:
            content = response.output
            return render(request, 'service/verifyAndShow.html', {'output': output, 'content': content})
        else:
            messages.success(request, "File could not be verified nor shown. Please try again")
            return redirect(reverse('login:verifyAndShow'))
    else:
        output = False
        form = VerifyAndShowForm()
        return render(request, 'service/verifyAndShow.html', {'output': output, 'form': form})


@login_required
def request_ela(request):
    return render(request, "service/requestELA.html")


@login_required
def vote_supernodes(request):
    return render(request, "service/voteSupernodes.html")


@login_required
def run_contract(request):
    return render(request, "service/runContract.html")


@login_required
def save_did_data(request):
    return render(request, "service/saveData.html")


@login_required
def retrieve_did_data(request):
    return render(request, "service/retrieveData.html")