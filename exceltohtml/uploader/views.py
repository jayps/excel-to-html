import os

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import pandas as pd
from django.template import Template, Context
import uuid
import shutil
from pathlib import Path


def uploader_view(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, template_name="uploader/index.html", context=None)

    if request.method == 'POST':
        Path('/code/downloads').mkdir(parents=True, exist_ok=True)
        Path('/code/downloads/tmp').mkdir(parents=True, exist_ok=True)
        excel_file = request.FILES['excel_file']
        uploaded_html_template = request.FILES['html_template']

        excel_sheet = pd.read_excel(excel_file)
        data = excel_sheet.to_dict(orient='records')

        template = Template(uploaded_html_template.file.read().decode())
        folder_name = uuid.uuid4()
        folder_path = f'/code/downloads/{folder_name}'
        os.mkdir(folder_path)
        for i in range(len(data)):
            context = Context(data[i])
            output = template.render(context)
            values = '_'.join(data[i].values())
            file_name = "".join(c for c in values if c.isalpha() or c.isdigit() or c == '-').rstrip()
            full_file_path = f'/{folder_path}/{file_name}.html'
            f = open(full_file_path, 'w')
            f.write(output)
            f.close()
        shutil.make_archive(str(folder_path), 'zip', folder_path)

        response = FileResponse(open(f'{folder_path}.zip', 'rb'), filename=f'{folder_name}.zip', as_attachment=True,
                                content_type='application/zip', status=200)

        shutil.rmtree(folder_path, ignore_errors=True, onerror=None)

        return response

    return render(request, template_name="uploader/index.html", context=None)
