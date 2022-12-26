from django.shortcuts import render,get_object_or_404
from .forms import PDFUploadForm
from .models import Text
import PyPDF2
import os
from django.shortcuts import redirect
from django.conf import settings
import tempfile

def extract_text_from_pdf(pdf_file):
    # create a temporary file
    temp = tempfile.NamedTemporaryFile(delete=False)

    # write the contents of the InMemoryUploadedFile object to the temporary file
    for chunk in pdf_file.chunks():
        temp.write(chunk)

    # get the file path of the temporary file
    file_path = temp.name

    # open the PDF file in read-binary mode
    with open(file_path, 'rb') as file:
        # create a PDF object
        pdf = PyPDF2.PdfReader(file)

        # initialize an empty string
        text = ''

        # iterate over every page in the PDF
        for page in range(len(pdf.pages)):
            # extract the text from the page
            page_text = pdf.pages[page].extract_text()
            # add the page text to the overall text
            text += page_text

    # close and delete the temporary file
    temp.close()
    os.unlink(file_path)

    return text

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # save the uploaded file
            pdf_file = request.FILES['pdf_file']
            file_name = pdf_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb') as file:
                file.write(pdf_file.read())
            # extract the text from the PDF file
            text = extract_text_from_pdf(pdf_file)
            # create a new Text object and save it to the database
            text_obj = Text.objects.create(text=text, pdf_file=file_name)
            return redirect('text_detail', pk=text_obj.pk)
    else:
        form = PDFUploadForm()
    return render(request, 'upload.html', {'form': form})

def text_list(request):
    texts = Text.objects.all()
    return render(request, 'text_list.html', {'texts': texts})

def text_detail(request, pk):
    text = Text.objects.get(pk=pk)
    return render(request, 'text_detail.html', {'text': text})