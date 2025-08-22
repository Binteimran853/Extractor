from django.shortcuts import render
from google_api import authenticate_gmail, get_latest_code, get_household_link
import subprocess
import os

def netflix_otp_extractor(request):
    selenium_output = ''
    email_html = ''
    houseHold_output = ''
    houseHold_link = ''

    if request.method == "POST":
        email = request.POST.get("email")
        service = authenticate_gmail()

        # Get OTP link
        email_html, verify_link = get_latest_code(service, email)

        if verify_link:
            script_path = os.path.abspath('selenium_test.py')
            proc = subprocess.Popen(
                ['python3', script_path, verify_link],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                out, err = proc.communicate(timeout=25)
                selenium_output = out.strip() if out else err.strip()
            except subprocess.TimeoutExpired:
                proc.kill()
                selenium_output = "Timed out while fetching OTP"
        else:
            selenium_output = "No verification link found in the email."

        # Get household link
        houseHold_link = get_household_link(service, email)

        if houseHold_link:
            print("Household link found:", houseHold_link)
            script_path = os.path.abspath('selenium_test1.py')
            proc = subprocess.Popen(
                ['python3', script_path, houseHold_link],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                out, err = proc.communicate(timeout=25)
                houseHold_output = out.strip() if out else err.strip()
                print(houseHold_output)
            except subprocess.TimeoutExpired:
                proc.kill()
                houseHold_output = "Timed out while fetching household"
        else:
            houseHold_output = "No household link found in the email."
            print(houseHold_output)

    return render(request, "extractCode/Netflix_Otp.html", {
        "email_html": email_html,
        "selenium_output": selenium_output,
        "houseHold_output": houseHold_output
    })
