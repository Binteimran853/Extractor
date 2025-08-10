from django.shortcuts import render
from google_api import authenticate_gmail, get_latest_code 

def netflix_otp_extractor(request):
    otp_result = None
    email_html = ''

    if request.method == "POST":
        email = request.POST.get("email")
        service = authenticate_gmail()
        otp_result, email_html = get_latest_code(service, email)  # get OTP and email html
        print(email_html)
    return render(request, "extractCode/Netflix_Otp.html", {
        "otp_result": otp_result,
        "email_html": email_html,
    })
