from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from .models import Cliente, Mascota, Cita
from .serializers import ClienteSerializer, MascotaSerializer, CitaSerializer
from .permissions import IsOwner, IsAdmin
from .database import get_db
from sqlalchemy.orm import Session
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, "is_admin", False)

class RegisterView(APIView):
    permission_classes = []  # Sin requerir autenticación
    
    def post(self, request):
        db: Session = next(get_db())
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            # Hashea la contraseña antes de guardar
            data = serializer.validated_data
            data['password'] = make_password(data['password'])
            cliente = Cliente(**data)
            db.add(cliente)
            db.commit()
            db.refresh(cliente)

            # Crear tokens JWT
            refresh = RefreshToken.for_user(cliente)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Usuario creado correctamente',
                'access_token': access_token,
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []  # No requiere autenticación

    def post(self, request):
        db: Session = next(get_db())
        email = request.data.get("email")
        password = request.data.get("password")

        # Obtener el usuario desde la base de datos
        cliente = db.query(Cliente).filter(Cliente.email == email).first()
        if cliente and cliente.check_password(password):
            refresh = RefreshToken.for_user(cliente)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)


# importaciones necesarias para la autenticación
class ClienteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
   
    # lista todos los clientes
    def list(self, request): 
        db: Session = next(get_db())
        clientes = db.query(Cliente).all()
        serializer = ClienteSerializer(clientes, many=True) 
        return Response(serializer.data)

    # obtiene un cliente por id
    def retrieve(self, request, pk=None): 
        db: Session = next(get_db())
        cliente = db.query(Cliente).filter(Cliente.id == pk).first()
        if cliente is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    # crea un nuevo cliente
    def create(self, request):
        db: Session = next(get_db())
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = Cliente(**serializer.validated_data)
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # actualiza un cliente por id
    def update(self, request, pk=None):
        db: Session = next(get_db())
        cliente = db.query(Cliente).filter(Cliente.id == pk).first()
        if cliente is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for key, value in request.data.items():
            setattr(cliente, key, value)
        db.commit()
        db.refresh(cliente)
        return Response(ClienteSerializer(cliente).data)

    # elimina un cliente por id
    def destroy(self, request, pk=None):
        db: Session = next(get_db())
        cliente = db.query(Cliente).filter(Cliente.id == pk).first()
        if cliente is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cliente.soft_delete = True
        db.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MascotaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # lista todas las mascotas
    def list(self, request):
        db: Session = next(get_db())
        mascotas = db.query(Mascota).all()
        serializer = MascotaSerializer(mascotas, many=True)
        return Response(serializer.data)

    # obtiene una mascota por id
    def retrieve(self, request, pk=None):
        db: Session = next(get_db())
        mascota = db.query(Mascota).filter(Mascota.id == pk).first()
        if mascota is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)

    # crea una nueva mascota
    def create(self, request):
        db: Session = next(get_db())
        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            mascota = Mascota(**serializer.validated_data)
            db.add(mascota)
            db.commit()
            db.refresh(mascota)
            return Response(MascotaSerializer(mascota).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # actualiza una mascota por id
    def update(self, request, pk=None):
        db: Session = next(get_db())
        mascota = db.query(Mascota).filter(Mascota.id == pk).first()
        if mascota is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for key, value in request.data.items():
            setattr(mascota, key, value)
        db.commit()
        db.refresh(mascota)
        return Response(MascotaSerializer(mascota).data)

    # elimina una mascota por id
    def destroy(self, request, pk=None):
        db: Session = next(get_db())
        mascota = db.query(Mascota).filter(Mascota.id == pk).first()
        if mascota is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mascota.soft_delete = True
        db.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CitaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Permisos personalizados para las acciones
    def get_permissions(self):
            if self.action == 'destroy':
                permission_classes = [IsAdminUser]  # Solo admin puede eliminar
            else:
                permission_classes = [IsAuthenticated]  # Otros pueden crear, editar, listar
            return [permission() for permission in permission_classes]

    # lista todas las citas
    def list(self, request):
        db: Session = next(get_db())
        citas = db.query(Cita).all()
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)

    # obtiene una cita por id
    def retrieve(self, request, pk=None):
        db: Session = next(get_db())
        cita = db.query(Cita).filter(Cita.id == pk).first()
        if cita is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CitaSerializer(cita)
        return Response(serializer.data)

    # crea una nueva cita
    def create(self, request):
        db: Session = next(get_db())
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            cita = Cita(**serializer.validated_data)
            db.add(cita)
            db.commit()
            db.refresh(cita)
            return Response(CitaSerializer(cita).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # actualiza una cita por id
    def update(self, request, pk=None):
        db: Session = next(get_db())
        cita = db.query(Cita).filter(Cita.id == pk).first()
        if cita is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for key, value in request.data.items():
            setattr(cita, key, value)
        db.commit()
        db.refresh(cita)
        return Response(CitaSerializer(cita).data)

    # elimina una cita por id
    def destroy(self, request, pk=None):
        db: Session = next(get_db())
        cita = db.query(Cita).filter(Cita.id == pk).first()
        if cita is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cita.soft_delete = True
        db.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)


