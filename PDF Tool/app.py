
import os
from flask import Flask,render_template,send_file,request
import PyPDF2

app = Flask(__name__)
#pdf , angle , page number
@app.route('/',methods=["POST","GET"])
def pdf_rotate():
	if request.method == "POST":
		file=request.files['file']
		try :
			file.save(os.path.join('uploads',file.filename))
		except :
			return "Input file not provided !"
		pages=list( map(int,request.form['pages'].split(',')) )
		angle=list( map(int,request.form['angle'].split(',')) )
		
		if (len(pages)!=len(angle)):
			return "Pages and angles do not match ! \n each page can only be rotated once, please try again"

		if (min(pages)==0 or min(pages)<0):
			return "Pages cannot be 0 or negative"
		
		pdf_in = open(f"uploads/{file.filename}", 'rb')
		pdf_reader = PyPDF2.PdfFileReader(pdf_in)
		pdf_writer = PyPDF2.PdfFileWriter()
		if (max(pages)>pdf_reader.numPages):
			return "Page number cannot be greater than document itself , please try again"
		
		for an in angle:
			if an%90 != 0:
				return "Angles can only be multiple of 90 degree , please try again"

		ct=0
		pgdict=dict()
		for i in range(len(pages)):
			pgdict[pages[i]]=angle[i]

		for ct in range(1,pdf_reader.numPages+1):
			if ct in pages:
				page=pdf_reader.getPage(ct-1)
				page.rotateClockwise(pgdict[ct])
				pdf_writer.addPage(page)
			else :
				page=pdf_reader.getPage(ct-1)
				pdf_writer.addPage(page)
	
		pdf_out = open(f'outputs/{file.filename}', 'wb')
		pdf_writer.write(pdf_out)
		pdf_out.close()
		pdf_in.close()
		
		return f"Sucessful operation ! Output can be seen at outputs/{file.filename}"
	return render_template("index.html")
if __name__ == '__main__':
	app.run(debug=True)
