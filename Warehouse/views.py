from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductSerializer, MaterialSerializer, ProductMaterialSerializer, WarehouseSerializer

class MaterialReportView(APIView):
    def post(self, request):
        product_code = request.data.get('product_code')
        quantity = request.data.get('quantity')

        if not product_code or not quantity:
            return Response({'error': 'Product code and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(product_code=product_code)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        materials = ProductMaterial.objects.filter(product=product)
        material_report = []

        for product_material in materials:
            material = product_material.material
            required_quantity = product_material.quantity * quantity

            # Ombordagi xomashyolarni tekshirish
            warehouse_entries = Warehouse.objects.filter(material=material)
            taken_quantity = 0
            details = []

            for entry in warehouse_entries:
                if entry.remainder >= required_quantity - taken_quantity:
                    details.append({
                        'warehouse_id': entry.id,
                        'taken_quantity': required_quantity - taken_quantity,
                        'price': entry.price
                    })
                    taken_quantity = required_quantity
                    break
                else:
                    details.append({
                        'warehouse_id': entry.id,
                        'taken_quantity': entry.remainder,
                        'price': entry.price
                    })
                    taken_quantity += entry.remainder

            # Qolgan miqdorni hisoblash
            missing_quantity = max(0, required_quantity - taken_quantity)

            material_report.append({
                'material_name': material.name,
                'required_quantity': required_quantity,
                'warehouse_details': details,
                'missing_quantity': missing_quantity
            })

        return Response({'product_code': product_code, 'quantity': quantity, 'materials': material_report}, status=status.HTTP_200_OK)

