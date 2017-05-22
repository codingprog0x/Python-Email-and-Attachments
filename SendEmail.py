'''
######
#	File containing SMTP and MIME for sending emails and attachments
#	Hashes, where applicable, are used in lieu of verbiage to protect confidentiality
######
'''

import smtplib
import resourceshash

######
#	below imports are related to attachment functionality
######
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class SendEmail:
	######
	#	Create SMTP object when class object is initialized
	######
	def __init__(self):
		self.smtp_obj = smtplib.SMTP("smtp.gmail.com", 587, None, 30)
		self.smtp_obj.ehlo()
		self.smtp_obj.starttls()
		
	def log_in(self, email=None, pw=None):
		if email is None:
			print("Please provide your email for SMTP login.")
			return False
		
		if pw is None:
			print("Please provide your password for SMTP login.")
			return False
		
		self.smtp_obj.login(email, pw)
		
	def log_out(self):
		self.smtp_obj.close()
	
	######
	#	Below method is for editing subject line in case
	#	submitter filled out incorrectly
	######
	def subject_header(self, pmc_name):
		default_subject = resourceshash.converted("74fdfc0f6701a197ba83d977cd32ad163c1b7ecc06c31d313a274c76a6559102") + pmc_name
		print("\nDefault Email Subject: " + default_subject)
		
		user_input = raw_input("\n/_\/_\ Does PMC name of subject header need to be edited? ")
		if user_input.lower().startswith("y"):
			user_input = raw_input(("Type in new subject header:"
										"\n"
										">	"))
			new_subject = resourceshash.converted("74fdfc0f6701a197ba83d977cd32ad163c1b7ecc06c31d313a274c76a6559102") + user_input
			print("\nNew subject header is: " + new_subject)
			
			user_input = raw_input("/_\/_\ Is this okay? ")
			if user_input.lower().startswith("n"):
				return self.subject_header(pmc_name)
			return new_subject
		return default_subject
		
	def send_to_submitter(self, to_header=None, from_header=None, is_property=None):
		if to_header is None:
			print("\nTo header not supplied in send_to_submitter() method.")
			return False
		if isinstance(to_header, bool):
			print("\nTo header value specified as a boolean in send_to_submitter() method.")
			return False
	
		if from_header is None:
			print("\nFrom header not supplied in send_to_submitter() method.")
			return False
		if isinstance(from_header, bool):
			print("\nFrom header specified as a boolean in send_to_submitter() method.")
			return False
		
		if is_property is None:
			print("\nWhether submission is a property not specified in send_to_submitter() method.")
			return False
		if not isinstance(is_property, bool):
			print("\nInvalid value for is_property argument in send_to_submitter() method.")
			return False
		
		print()
		print("Send to: " + to_header)
		user_input = raw_input("/_\/_\ Send email to SUBMITTER? ")
		
		if user_input.lower().startswith("y"):
			######
			#	Instantiate MIMEMultipart object
			#	Construct email body and subject
			#	Contents are contingent on type of submission
			######
			
			email_body = None
			an_email = MIMEMultipart()
		
			if is_property:
				an_email["Subject"] = resourceshash.converted("b2ec47d3a2d4817bbe9cef7a3a44586c42a44191db89a7493ec5f50419a2b0ba")
				email_body = resourceshash.converted("52a691ad384247078de771aed57f17d3d95b86609902f3b2ee64fc1caec38353")
			else:
				an_email["Subject"] = resourceshash.converted("0c204d40fe5fc470999fa58379182ebe1922692aa9529cbe95b5d6a74f52e714")
				email_body = resourceshash.converted("bf852f4764e75747667de3bcc20942fc5af05cf19ad9523cd54b21ffdddb91c8")
			
			######
			#	Add to and from headers to MIMEMultipart object
			#	as well as email message
			######
			an_email["To"] = to_header
			an_email["From"] = from_header
			an_email.attach(MIMEText(email_body))
			
			######
			#	sendmail() returns empty dictionary if successful
			#	An empty dictionary evaluates to false
			#	Run dictionary through bool and if false, then successful
			#	If anything else, then unsuccessful
			######
			is_successful = self.smtp_obj.sendmail(from_header, to_header, an_email.as_string())
			if not bool(is_successful):
				print("<---- Email to SUBMITTER sent successfully!")
			else:
				print("***EMAIL TO SUBMITTER FAILED***")
				print("**EMAIL TO SUBMITTER FAILED**")
				print("*EMAIL TO SUBMITTER FAILED*")
		else:
			print("X----X Did not send email to SUBMITTER.")

	######
	#	*args should be name of file only; exclude path, as it is specified in file_path argument
	#	**kwargs needs to contain to and from headers, as well as CC and BCC
	#	**kwargs' key-value names need be to_header, from_header, to_cc, and to_bcc, and their values
	#	need to be a list
	######
	def send_to_processor(self, pmc_name, file_path, *file_names, **headers):
		######
		#	Check method's parameters to see whether they meet criteria
		#	If they don't, print why and return False, which is to be
		#	handled by client
		######
		send_to_addresses = []
		
		if headers.get("to_header") is None:
			print("\nTo header not supplied in send_to_processor() method.")
			return False
		elif isinstance(headers.get("to_header"), list):
			pass
		elif isinstance(headers.get("to_header"), bool):
			print("\nInvalid input for to header in send_to_processor() method.")
			return False
		else:
			send_to_addresses += headers.get("to_header")
			
		if headers.get("from_header") is None:
			print("\nFrom header not supplied in send_to_processor() method.")
			return False
		elif isinstance(headers.get("from_header"), list):
			pass
		elif isinstance(headers.get("from_header"), bool):
			print("\nInvalid input for from header in send_to_processor() method.")
			return False
		else:
			print("\nFrom header needs to be a list.")
			return False
		
		if headers.get("to_cc") is None:
			pass
		elif isinstance(headers.get("to_cc"), list):
			send_to_addresses += headers.get("to_cc")
		elif isinstance(headers.get("to_cc"), bool):
			print("\nInvalid input for BCC in send_to_processor() method.")
			return False
		else:
			print("\nTo CC needs to be a list.")
			return False
		
		if headers.get("to_bcc") is None:
			pass
		elif isinstance(headers.get("to_bcc"), list):
			send_to_addresses += headers.get("to_bcc")
		elif isinstance(headers.get("to_bcc"), bool):
			print("\nInvalid input for BCC in send_to_processor() method.")
			return False
		else:
			print("\nTo BCC needs to be a list.")
			return False
		
		######
		#	An empty list returns a boolean of false
		######
		if not file_names:
			print("\nNo file provided as attachment in send_to_processor() method.")
			return False
		
		print("")
		print("PMC: " + pmc_name)
		print("Path: " + file_path)
		print("File(s): ", file_names)
		print("Recipients:", send_to_addresses)
		
		print("")
		user_input = raw_input("/_\/_\ Send email to PROCESSOR? ")
		if user_input.lower().startswith("y"):
			######
			#	Create MIMEMultipart and specify from, to, bcc, and subject
			#	MIMEMultipart needs to be assigned strings; lists throw an error
			######
			from_header_string = headers.get("from_header")
			from_header_string = ",".join(from_header_string)
			to_cc_string = headers.get("to_cc")
			to_cc_string = ",".join(to_cc_string)
			to_header_string = headers.get("to_header")
			to_header_string = ",".join(to_header_string)
			
			an_email = MIMEMultipart()
			an_email["From"] = from_header_string
			an_email["To"] = to_header_string
			an_email["CC"] = to_cc_string
			
			######
			#	Subject and email message are static for this use case
			#	However, due to possible submitter error, subject is editable
			######
			an_email["Subject"] = self.subject_header(pmc_name)
			
			if headers.get("bcc_header") is not None:
				an_email["BCC"] = headers.get("to_bcc")
			
			an_email.attach(MIMEText(resourceshash.converted("f11b436f7edc38bbbb08a43a4b46eabf745688080470adf4fd610cf1f317ec79")))
			
			######
			#	Put file names into a list to be attached shortly
			######
			files_to_attach = []
			for a_file in file_names:
				files_to_attach.append(a_file)
			
			######
			#	Put file path and files into a list, add a header,
			#	and then attach to MIMEMultipart() object
			######
			attachments = []
			for file_to_attach in files_to_attach:
				a_file = open("./" + file_path + "/" + file_to_attach, "rb")
				an_attachment = MIMEApplication(a_file.read(), "rb")
				a_file.close()
				
				an_attachment.add_header("Content-Disposition", "attachment", filename=file_to_attach)
				attachments.append(an_attachment)
				an_email.attach(an_attachment)
				
			is_successful = self.smtp_obj.sendmail(headers.get("from_header"), send_to_addresses, an_email.as_string())
			
			if not bool(is_successful):
				print("<---- Email to PROCESSOR sent successfully!")
			else:
				print("***EMAIL TO PROCESSOR FAILED***")
				print("**EMAIL TO PROCESSOR FAILED**")
				print("*EMAIL TO PROCESSOR FAILED*")
				print(is_successful)
		else:
			print("X----X Email to PROCESSOR not sent.")
