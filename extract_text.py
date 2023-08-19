import pdfplumber

def extract_text_from_pdf(input_path, output_path):
    with pdfplumber.open(input_path) as pdf, open(output_path+'.csv', 'w') as output_file:
        text = ''
        req_lines = []
        for page in pdf.pages:
            lines = page.extract_text_lines()
            detail_flag = False
            for line in lines:
                if "Detail" in line['text']:
                    detail_flag = True
                # print(line['text'])
                if "$" in line['text'] and detail_flag:
                    # print(line['text'])
                    req_lines.append(line['text'])
        input_string = "\n".join(req_lines)
        # example_input_string = """
        # Amazon Simple Storage Service $3.81
        # Charges $3.23
        # GST $0.58
        # AWS Data Transfer $0.00
        # Charges $0.00
        # GST $0.00
        # Amazon S3 Glacier Deep Archive $0.01
        # Charges $0.01
        # GST $0.00
        # AmazonCloudWatch $0.00
        # Charges $0.00
        # GST $0.00
        # """

        lines = input_string.strip().split('\n')
        data = []
        for i in range(0, len(lines), 3):
            service = lines[i].split(' $')[0]
            charges = lines[i+1].split(' $')[1]
            gst = lines[i+2].split(' $')[1]
            total = float(charges) + float(gst)
            data.append([service, f"{charges}", f"{gst}", f"{total:.2f}"])
        text += 'Service|charges($)|gst($)|total($)' + '\n'
        for row in data:
            text += '|'.join(row) + '\n'
        output_file.write(text)
        return output_path+'.csv'
