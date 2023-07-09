from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from utils import finance
from .models import Blacklist
from .serializers import AISerializer


class AIView(GenericAPIView):
    serializer_class = AISerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_authenticated:
            if self.check_ip_address(request):
                try:
                    response = finance(serializer.validated_data["search"])
                
                except ConnectionError:
                    Response({"message":"Failed to establish a connection", "status": False})
                
                except Exception as e:
                    return Response(
                        {"response": "AI is unavailable",
                         "message": str(e)},
                        status=status.HTTP_408_REQUEST_TIMEOUT,
                    )

                return Response({"response": response, "status":True}, status=status.HTTP_200_OK)

            return Response(
                {
                    "response": "You have exceeded your free trials, register and login to continue", 
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def check_ip_address(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        remote_addr = request.META.get("REMOTE_ADDR")
        num_proxies = 0  

        print(xff, remote_addr)

        if num_proxies is not None:
            if num_proxies == 0 or xff is None:
                ip = remote_addr
            else:
                address = xff.split(",")
                client_addr = address[-min(num_proxies, len(address))]
                ip = client_addr.strip()

        else:
            ip = "".join(xff.split()) if xff else remote_addr

        ip_obj, created = Blacklist.objects.get_or_create(ip_address=ip)

        if created or ip_obj.trials < 5:
            ip_obj.trials += 1

            ip_obj.save()

            return True

        return False
