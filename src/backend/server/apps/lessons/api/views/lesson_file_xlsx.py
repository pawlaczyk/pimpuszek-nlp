from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from server.settings import MEDIA_ROOT
import os


from ...models import LessonDir, LessonFile
from ...helpers.excel_tables import excel_to_json

from .utils.file_name import parse_filename


class LessonXlsxView(APIView):
    """Zwraca pliki excela dla lekcji"""

    def get(self, request):
        lesson_filename = request.query_params.get("filename")
        if lesson_filename:
            lesson_filename = parse_filename(lesson_filename)

        lesson_dirname = request.query_params.get("lesson")

        if lesson_filename and lesson_dirname:
            lesson_file_obj = LessonFile.objects.filter(
                filename=lesson_filename, lesson_dir__dir_name=lesson_dirname
            )
            if not lesson_file_obj.exists():
                # jak szukany plik w lekcji nie istnieje
                return Response(
                    f"Plik:{lesson_filename} nie isnieje w lekcji {lesson_dirname}",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                f"Pli: {[str(i) for i in lesson_file_obj]}",
                status=status.HTTP_200_OK,
            )

        if lesson_dirname:
            # zwraca wszsytkie pliki excela dla dane lekcji - przydatne do quizów z całej lekcji
            lesson_dir_obj = LessonDir.objects.filter(dir_name=lesson_dirname)
            if not lesson_dir_obj.exists():
                return Response(
                    f"Lekcja {lesson_dirname} NIE istnieje ",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # wszsytkei pliki dla tej lekcji/foderu
            lesson_file_list = LessonFile.objects.filter(lesson_dir=lesson_dir_obj[0])
            xlsx_file_list = [
                str(i) for i in lesson_file_list if str(i).split(".")[-1] == "xlsx"
            ]
            return Response(
                f"Pliki excel dla lekcji {lesson_dirname}: {xlsx_file_list}",
                # f"tuuu",
                status=status.HTTP_200_OK,
            )

        if lesson_filename:
            # szukam po pliku - np gdy źle zuploadowałam
            print("\n\n\n\n\nlesson_filename:", lesson_filename)

            # lesson_file_list = LessonFile.objects.filter(filename=lesson_filename)
            lesson_file_list = LessonFile.objects.all()
            for i in lesson_file_list:
                print("filename:", i.filename)

            print("---------------- tu ----------------", lesson_file_list)
            return Response(
                # f"Wszytkie lekcje w których plik {str(lesson_file_list)} się znajduje {[i.lesson_dir__dir_name for i in lesson_file_list]}",
                f"Wszytkie lekcje w których plik {str(lesson_file_list)} się znajduje",
                status=status.HTTP_200_OK,
            )

        # jak nie ma parametru to zwracam pliki excel dla wszsytkich lekcji
        response = []
        lesson_dir_list = LessonDir.objects.all()
        for lesson_dir in lesson_dir_list:
            lesson_file_list = LessonFile.objects.filter(lesson_dir=lesson_dir)
            xlsx_file_list = [
                str(i) for i in lesson_file_list if str(i).split(".")[-1] == "xlsx"
            ]
            response.append(
                {"lesson": str(lesson_dir), "excel_files": lesson_file_list}
            )

        return Response(
            f"Wszytkie Pliki excel {response}",
            status=status.HTTP_200_OK,
        )


class LessonXlsxToJsonView(APIView):
    """Zwraca Json z excela - potrzebne do zrobienia quizów"""

    def get(self, request):
        """Musi już dostać konkretnie któy plik mam zamienić na jsona"""
        lesson_filename = request.query_params.get("filename")
        lesson_dirname = request.query_params.get("lesson")

        if lesson_filename and lesson_dirname:
            lesson_file_obj = LessonFile.objects.filter(
                filename=lesson_filename, lesson_dir__dir_name=lesson_dirname
            )
            if lesson_file_obj.exists() and len(lesson_file_obj) == 1:
                # jak szukany plik w lekcji nie istnieje
                filepath = os.path.join(MEDIA_ROOT, lesson_dirname, lesson_filename)
                json_response = excel_to_json(filepath)

                return Response(
                    # f"Plik:{lesson_file_obj[0].lesson_file}",
                    json_response,
                    status=status.HTTP_200_OK,
                )

        return Response(
            f"Plik {lesson_filename} NIE istneije w lekcji {lesson_dirname}",
            status=status.HTTP_400_BAD_REQUEST,
        )
