from django.shortcuts import render
from google_api import authenticate_gmail, get_latest_code 
import subprocess
import os

def netflix_otp_extractor(request):
    
    email_html = ''
    links = []
    if request.method == "POST":
        email = request.POST.get("email")
        service = authenticate_gmail()
        email_html, verify_link = get_latest_code(service, email)
        if verify_link:
            script_path = os.path.abspath('selenium_test.py')
            # Run subprocess and capture output/errors for debugging
            proc = subprocess.Popen(
                ['python3', script_path, verify_link],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                out, err = proc.communicate(timeout=30)
                print(out,err)
            except subprocess.TimeoutExpired:
                proc.kill()
                out, err = proc.communicate()


            selenium_output = out.strip() if out else "No output from Selenium script"

        
     
        print("Email Links:", links)

    return render(request, "extractCode/Netflix_Otp.html", {
        
        "email_html": email_html,
        "links": links,
        "selenium_output": selenium_output,

    })
