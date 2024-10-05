from rest_framework.response import Response
from rest_framework.views import APIView


class EnvironmentView(APIView):
    def get(self, request):
        env_variables = request.session.get("environment_variables")
        return Response({"status": "success", "output": env_variables})

    def post(self, request):
        environment_variables = request.data.get("body")
        request.session["environment_variables"] = environment_variables
        return Response({"status": "success", "output": environment_variables})
