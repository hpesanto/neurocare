from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

from .utils import get_client_ip, get_user_agent
from .services import registrar_log


User = get_user_model()


class AuditTokenObtainPairView(TokenObtainPairView):
    """
    CustomTokenObtainPair com auditoria de login (sucesso e falha).
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        ip = get_client_ip(request)
        user_agent = get_user_agent(request)

        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == 200:
                try:
                    user = User.objects.get(username=username)
                    registrar_log(
                        usuario_login=username,
                        acao='LOGIN',
                        id_usuario=user.id,
                        ip=ip,
                        user_agent=user_agent,
                        metodo_http='POST',
                        caminho='/api/token/',
                    )
                except User.DoesNotExist:
                    pass

            return response

        except AuthenticationFailed:
            registrar_log(
                usuario_login=username,
                acao='LOGIN_FALHA',
                ip=ip,
                user_agent=user_agent,
                metodo_http='POST',
                caminho='/api/token/',
            )
            raise


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout: blacklist do refresh token e registra LOGOUT.
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'refresh token required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken(refresh_token)
        token.blacklist()

        user = request.user
        ip = get_client_ip(request)
        user_agent = get_user_agent(request)

        registrar_log(
            usuario_login=user.username,
            acao='LOGOUT',
            id_usuario=user.id,
            ip=ip,
            user_agent=user_agent,
            metodo_http='POST',
            caminho='/api/auth/logout/',
        )

        return Response(status=status.HTTP_205_RESET_CONTENT)

    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
