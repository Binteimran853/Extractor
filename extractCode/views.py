from django.shortcuts import render
from google_api import authenticate_gmail, get_latest_code 



def netflix_otp_extractor(request):
    otp_result = None

    if request.method == "POST":
        email = request.POST.get("email")
        service = authenticate_gmail()
        otp_result = get_latest_code(service, email)  # call Gmail API

    return render(request, "extractCode/Netflix_Otp.html", {"otp_result": otp_result})