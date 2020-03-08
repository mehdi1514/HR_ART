import smtplib 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("wimpycat714@gmail.com", "temppassword123") 
  
# message to be sent 
message = 'Subject: {}\n\n{}'.format("SUBJECT", "TEXT")
  
# sending the mail 
s.sendmail("wimpycat714@gmail.com", "mehdi.patel@gmail.com", message) 
  
# terminating the session 
s.quit()