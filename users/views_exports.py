# users/views_exports.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from .models import Resume
from .export_resume import build_pdf_bytes, build_docx_bytes

class ResumeExportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id: int):
        try:
            r = Resume.objects.get(pk=resume_id, user=request.user)
        except Resume.DoesNotExist:
            return Response({"detail": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

        schema = r.data.get("__schema") or (r.template.schema if r.template else {})
        pdf_bytes = build_pdf_bytes(r.data, schema)

        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="resume-{resume_id}.pdf"'
        return resp

class ResumeExportDOCXView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id: int):
        try:
            r = Resume.objects.get(pk=resume_id, user=request.user)
        except Resume.DoesNotExist:
            return Response({"detail": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

        schema = r.data.get("__schema") or (r.template.schema if r.template else {})
        docx_bytes = build_docx_bytes(r.data, schema)

        resp = HttpResponse(
            docx_bytes,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        resp["Content-Disposition"] = f'attachment; filename="resume-{resume_id}.docx"'
        return resp
