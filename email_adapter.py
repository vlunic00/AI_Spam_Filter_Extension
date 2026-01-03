import email
import re
import html
import os
import sys
from pathlib import Path

##################################################
## @brief Parse an email string and extract the text body
## @in string   raw_email_string
## @out string  body_content
##################################################
def extract_body_from_email(raw_email_string):
    msg = email.message_from_string(raw_email_string)
    body_content = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                continue

            # Prioritize text/plain over text/html
            if content_type == "text/plain":
                try:
                    body_content += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                except Exception:
                    pass
            elif content_type == "text/html" and not body_content:
                try:
                    body_content += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                except Exception:
                    pass
    else:
        try:
            body_content = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
        except Exception:
            pass
            
    return body_content

##################################################
## @brief Remove HTML tags & headers, normalize whitespace & turn text to lowercase
## @in string   text
## @out string  clean_text
##################################################
def cleanup_text(text):
    if not text:
        return ""

    temp_text = text
    patterns_to_remove = [
        r'(^\s*date:\s+.*?$)|(^\s*from:\s+.*?$)|(^\s*message-id:\s+.*?$)|(^\s*to:\s+.*?$)|(^\s*cc:\s+.*?$)',
        r'^\s*<[^>]+@[\w\.-]+>',
    ]

    for pattern in patterns_to_remove:
        temp_text = re.sub(pattern, '', temp_text, flags=re.IGNORECASE | re.MULTILINE)

    footer_pattern = r'_{15,}.*?(mailing list|list-unsubscribe|list-subscribe|list-id|@redhat\.com).*'
    temp_text = re.sub(footer_pattern, '', temp_text, flags=re.IGNORECASE | re.DOTALL)

    clean_text = re.sub(r'<.*?>', ' ', temp_text)
    clean_text = html.unescape(clean_text)
    clean_text = clean_text.lower()

    clean_text = re.sub(r'^\s*[\W_]+\s*$', '', clean_text, flags=re.MULTILINE)
    clean_text = " ".join(clean_text.split())

    return clean_text

##################################################
## @brief Handler for processing the email string 
## @in string   raw_data
## @out string  clean_data
##################################################
def process_email_data(raw_data):
    raw_body = extract_body_from_email(raw_data)
    clean_data = cleanup_text(raw_body)
    return clean_data

##################################################
## @brief   Iterate through all files in a dir, process them and save the output to the output dir 
## @in string, string     input_dir, output_dir
## @out void
##################################################
def batch_process_emails(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory created/verified at: {output_path}")
    print("-" * 30)

    processed_count = 0
    
    for file_path in input_path.iterdir():
        if file_path.is_file():
            print(f"Processing: {file_path.name}...", end="")
            try:
                raw_content = file_path.read_bytes().decode('latin-1', errors='ignore')

                cleaned_text = process_email_data(raw_content)

                output_file_path = output_path / file_path.name
                
                with open(output_file_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(cleaned_text)
                    
                processed_count += 1
                print(" DONE.")

            except Exception as e:
                print(f" ERROR! Could not process {file_path.name}. Reason: {e}")
        else:
            print(f"ERROR: {file_path.name} - Is not a supported file!")
    
    print("-" * 30)
    print(f"✅ Batch Processing Complete. Total files processed: {processed_count}")


if __name__ == "__main__":

    INPUT_DIR = sys.argv[1]
    OUTPUT_DIR = sys.argv[2]    
    batch_process_emails(INPUT_DIR, OUTPUT_DIR)