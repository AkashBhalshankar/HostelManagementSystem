from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
import mysql.connector
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import FeeReceiptForm
from .models import FeeReceipt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def index(request):
    return render(request, "index.html")


def registration_form(request):
    if request.method == "POST":
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hostel"
        )

        # Retrieve form data
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        house_number = request.POST.get('house_number', '')
        village = request.POST.get('village', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        postal_code = request.POST.get('postal_code', '')
        joining_date = request.POST['joining_date']
        sharing_type = request.POST.get('sharing_type', 'single')
        monthly_fees = request.POST.get('monthly_fees', 0)
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'registration_form.html', {"error": "Passwords do not match"})

        # Prepare SQL query using string concatenation as per your logic
        sql = f"""
            INSERT INTO students (
                firstname, lastname, email, phone, house_number, village, city, state, postal_code,
                joining_date, sharing_type, monthly_fees, password
            ) VALUES (
                '{firstname}', '{lastname}', '{email}', '{phone}', '{house_number}', '{village}', '{city}',
                '{state}', '{postal_code}', '{joining_date}', '{sharing_type}', '{monthly_fees}', '{password}'
            )
        """

        # Insert data into the database
        try:
            mycursor = conn.cursor()
            mycursor.execute(sql)
            conn.commit()
            conn.close()
        except Exception as e:
            return render(request, 'registration_form.html', {"error": f"An error occurred: {str(e)}"})

        # Redirect to login or home page with success message
        return redirect('/login_form', {"status": "Registration successful! You can now log in."})

    else:
        return render(request, 'registration_form.html')



def login_form(request):
    print("Request Method:", request.method)  # Debugging request method
    
    if request.method == "POST":
        phone = request.POST.get('un')  # Retrieve phone number from the form
        password = request.POST.get('pwd')  # Retrieve password from the form
        
        print("Phone:", phone)  # Debugging form input
        print("Password:", password)  # Debugging form input

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hostel"
        )
        mycursor = conn.cursor()

        # Query to check credentials using the phone and password fields
        query = "SELECT * FROM students WHERE phone=%s AND password=%s"
        mycursor.execute(query, (phone, password))
        result = mycursor.fetchone()

        print("Query result:", result)  # Debugging result

        if result:
            # Set session variable
            request.session['phone'] = phone
            print("Above redirect")
            return redirect("student_home_page")  # Redirect to the home page (URL pattern name 'index')
        else:
            # Add error message
            messages.error(request, 'Invalid phone number or password.')
            return render(request, "login_form.html", {"status": "invalid credentials"})
    else:
        print("I am at else part")  # This will show if the request is a GET request
        # Render login form for GET request
        return render(request, "login_form.html")
    
def complaint_form(request):
     if request.method == 'POST':
        complaint_type = request.POST.get('complaint_type')
        complaint_description = request.POST.get('complaint_description')
        facing_from_date = request.POST.get('facing_from_date')
        
        # Save the data to the database
        Complaint.objects.create(
            complaint_type=complaint_type,
            complaint_description=complaint_description,
            facing_from_date=facing_from_date
        )
        return redirect('complaint_success')  # Redirect to a success page after submission

     return render(request, 'complaint_form.html')

def complaint_success(request):
    return render(request, 'complaint_success.html')

def complaint_form(request):
    if request.method == "POST":
        print("I'm in post request", request.POST)
        
        # Database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hostel"  # Update with your actual database name
        )
        
        # Retrieve form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        complaint_type = request.POST['complaint_type']
        complaint_description = request.POST['complaint_description']
        facing_from_date = request.POST['facing_from_date']
        
        # Prepare cursor and insert data into the database
        mycursor = conn.cursor()
        query = """
            INSERT INTO complaints (first_name, last_name, phone_number, complaint_type, complaint_description, facing_from_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, phone_number, complaint_type, complaint_description, facing_from_date)
        mycursor.execute(query, values)
        conn.commit()
        
        # Close the connection
        conn.close()
        
        # Redirect to the success page
        return redirect('/complaint/success')  # Update with the correct success page URL
        
    else:
        return render(request, 'complaint_form.html')
    




# View to generate and download the receipt as a PDF
def generate_receipt_pdf(request, receipt_id):
    receipt = FeeReceipt.objects.get(id=receipt_id)
    
    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Receipt details
    p.drawString(100, 750, f"Full Name: {receipt.full_name}")
    p.drawString(100, 730, f"UTR Number: {receipt.utr_number}")
    p.drawString(100, 710, f"Date: {receipt.date}")
    p.drawString(100, 690, f"Hostel Name: {receipt.hostel_name}")
    
    # Signature area
    p.drawString(100, 650, f"Owner's Signature: {receipt.owner_signature if receipt.owner_signature else 'Not Signed'}")
    
    # Save the PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    
    # Return the PDF as a response
    return HttpResponse(buffer, content_type='application/pdf')


# Success view after submitting the form
def receipt_success(request, receipt_id):
    receipt = FeeReceipt.objects.get(id=receipt_id)
    return render(request, 'receipt_success.html', {'receipt': receipt})    



from datetime import datetime

def fee_receipt_form(request):
    if request.method == "POST":
        # Collect form data
        fullname = request.POST.get('fullname')
        utr_number = request.POST.get('utr_number')
        date = request.POST.get('date')
        hostel_name = request.POST.get('hostel_name')
        owner_signature = request.POST.get('owner_signature')
        
        # Format the date into a more readable format
        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Update with your MySQL username
            password="",  # Update with your MySQL password
            database="hostel"  # Update with your database name
        )
        
        cursor = conn.cursor()

        # Insert form data into the fee_receipt table
        insert_query = """
            INSERT INTO fee_receipt (fullname, utr_number, date, hostel_name, owner_signature)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (fullname, utr_number, date, hostel_name, owner_signature))
        
        # Commit the transaction
        conn.commit()
        
        # Close the database connection
        cursor.close()
        conn.close()

        # Generate the receipt content
        receipt_content = f"""
        <html>
            <head>
                <title>Fees Receipt</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        padding: 20px;
                        width: 60%;
                        margin: 0 auto;
                        border: 1px solid #ddd;
                    }}
                    h2 {{
                        text-align: center;
                    }}
                    .details {{
                        margin: 20px 0;
                    }}
                    .footer {{
                        margin-top: 30px;
                        text-align: center;
                        font-style: italic;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Fees Receipt</h2>
                    <div class="details">
                        <p><strong>Full Name:</strong> {fullname}</p>
                        <p><strong>UTR Number:</strong> {utr_number}</p>
                        <p><strong>Date:</strong> {formatted_date}</p>
                        <p><strong>Hostel Name:</strong> {hostel_name}</p>
                    </div>
                    <div class="footer">
                        <p><strong>Owner's Signature:</strong> {owner_signature}</p>
                    </div>
                    <button onclick="window.print()">Print Receipt</button>
                </div>
            </body>
        </html>
        """

        return HttpResponse(receipt_content)

    return render(request, 'fee_receipt_form.html')



def student_home_page(request):
    # Render the student dashboard template
    return render(request, 'student_home_page.html')

def logout_view(request):
    # Clear the session, removing any stored session data (including user info)
    if 'phone' in request.session:
        del request.session['phone']
        messages.success(request, 'You have been logged out successfully.')
    
    # Redirect to the index page (home page)
    return redirect('index')  # Change 'index' to your actual home page URL pattern name



def admin_login_form(request):
    print("Request Method:", request.method)  # Debugging request method

    if request.method == "POST":
        username = request.POST.get('un')  # Retrieve username from the form
        password = request.POST.get('pwd')  # Retrieve password from the form
        
        print("Username:", username)  # Debugging form input
        print("Password:", password)  # Debugging form input

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hostel"
        )
        mycursor = conn.cursor()

        # Query to check admin credentials using the username and password fields
        query = "SELECT * FROM admin WHERE username=%s AND password=%s"
        mycursor.execute(query, (username, password))
        result = mycursor.fetchone()

        print("Query result:", result)  # Debugging result

        if result:
            # Set session variable for admin
            request.session['admin'] = username
            print("Above redirect")
            return redirect("dashheader")  # Redirect to the admin dashboard
        else:
            # Add error message for invalid credentials
            messages.error(request, 'Invalid username or password.')
            return render(request, "admin_login.html", {"status": "invalid credentials"})
    else:
        print("I am at else part")  # This will show if the request is a GET request
        # Render admin login form for GET request
        return render(request, "admin_login.html")
    
def admin_dashboard(request):
    # Check if the user is logged in as admin
    if 'admin' not in request.session:
        return redirect('admin_login')  # Redirect to login if not logged in
    
    return render(request, "admin_dashboard.html")  # Render the dashboard page

def view_students(request):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hostel"
    )
    cursor = conn.cursor()

    # Query to retrieve all student data
    query = "SELECT * FROM students"
    cursor.execute(query)
    students = cursor.fetchall()  # Fetch all student data

    # Close the connection
    conn.close()

    # Pass the student data to the template
    return render(request, "view_students.html", {"students": students})


def view_complaints(request):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hostel"
    )
    cursor = conn.cursor()

    # Query to retrieve all complaints
    query = "SELECT * FROM complaints"
    cursor.execute(query)
    complaints = cursor.fetchall()  # Fetch all complaints

    # Close the connection
    conn.close()

    # Pass the complaints data to the template
    return render(request, "view_complaints.html", {"complaints": complaints})

def view_fee_receipts(request):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hostel"
    )
    cursor = conn.cursor()

    # Query to retrieve all fee receipts
    query = "SELECT * FROM fee_receipt"
    cursor.execute(query)
    fee_receipts = cursor.fetchall()  # Fetch all fee receipts

    # Close the connection
    conn.close()

    # Pass the fee receipt data to the template
    return render(request, "view_fee_receipt.html", {"fee_receipts": fee_receipts})

def dashboard(request):
    # This view renders the dashboard page.
    return render(request, 'dashheader.html')




