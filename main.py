import base64
import os

from google_apis import create_service
from extract_text import extract_text_from_pdf

if __name__ == '__main__':
	CLIENT_FILE = 'client-secret.json'
	API_NAME = 'gmail'
	API_VERSION = 'v1'
	SCOPES = ['https://mail.google.com/']
	QUERY_FETCH_ATTACHMENT_FROM = 'from:aws-in-receivables-support@amazon.com'


	gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

	results = gmail_service.users().messages().list(userId='me', q=QUERY_FETCH_ATTACHMENT_FROM).execute()
	messages = results.get('messages', [])
	print("Fetched all messages from aws-in-receivables-support@amazon.com")

	for message in messages:
		msg = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
		for part in msg['payload']['parts']:
			if part['filename'] and part['filename'].endswith('.pdf'):
				attachment_id = part['body']['attachmentId']
				attachment = gmail_service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachment_id).execute()
				
				# Decode and save attachment
				file_data = base64.urlsafe_b64decode(attachment['data'])
				file_name = part['filename']
				
				# Check if output dir exists first, if not, create the folder
				OUTPUT_DIR = 'output'
				cur_wrk_dir = os.getcwd()
				if not os.path.exists(os.path.join(cur_wrk_dir, OUTPUT_DIR)):
					os.mkdir(os.path.join(cur_wrk_dir, OUTPUT_DIR))
				output_path = os.path.join(cur_wrk_dir,OUTPUT_DIR)
				file_path = os.path.join(output_path,file_name)
				with open(file_path, 'wb') as f:
					f.write(file_data)
				print(f'Saved attachment: {file_name}')
				
				# extract required text and save as csv in output directory
				text_output_path = extract_text_from_pdf(
					input_path=os.path.join(output_path,file_name),
					output_path=os.path.join(output_path,f"csv_{file_name.split('.')[0]}"),
				)
