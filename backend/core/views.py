import io
import pandas as pd
from django.http import HttpResponse
from django.db.models import Avg, Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from .models import EquipmentBatch, EquipmentData
from .serializers import (
    EquipmentDataSerializer, 
    EquipmentBatchSerializer,
    CSVUploadSerializer,
    DashboardStatsSerializer
)


class CSVUploadView(APIView):
    """API view to handle CSV file uploads."""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = serializer.validated_data['file']
        
        try:
            # Read CSV with pandas
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create a new batch
            batch = EquipmentBatch.objects.create(
                user=request.user,
                filename=csv_file.name
            )
            
            # Save each row as EquipmentData
            equipment_data_list = []
            for _, row in df.iterrows():
                equipment_data_list.append(EquipmentData(
                    equipment_name=row['Equipment Name'],
                    type=row['Type'],
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature']),
                    batch=batch
                ))
            
            EquipmentData.objects.bulk_create(equipment_data_list)
            
            return Response({
                'message': 'CSV uploaded successfully',
                'batch_id': batch.id,
                'records_created': len(equipment_data_list)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error processing CSV: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class DashboardStatsView(APIView):
    """API view to return dashboard statistics."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get the latest batch
        latest_batch = EquipmentBatch.objects.first()
        
        if not latest_batch:
            return Response({
                'total_count': 0,
                'average_values': {
                    'flowrate': 0,
                    'pressure': 0,
                    'temperature': 0
                },
                'type_distribution': {},
                'latest_batch': None,
                'equipment_data': []
            })
        
        # Get equipment data for the latest batch
        equipment_data = EquipmentData.objects.filter(batch=latest_batch)
        
        # Calculate statistics
        total_count = equipment_data.count()
        
        # Average values
        averages = equipment_data.aggregate(
            avg_flowrate=Avg('flowrate'),
            avg_pressure=Avg('pressure'),
            avg_temperature=Avg('temperature')
        )
        
        average_values = {
            'flowrate': round(averages['avg_flowrate'] or 0, 2),
            'pressure': round(averages['avg_pressure'] or 0, 2),
            'temperature': round(averages['avg_temperature'] or 0, 2)
        }
        
        # Type distribution
        type_counts = equipment_data.values('type').annotate(count=Count('id'))
        type_distribution = {item['type']: item['count'] for item in type_counts}
        
        # Serialize equipment data
        serialized_data = EquipmentDataSerializer(equipment_data, many=True).data
        
        return Response({
            'total_count': total_count,
            'average_values': average_values,
            'type_distribution': type_distribution,
            'latest_batch': {
                'id': latest_batch.id,
                'uploaded_at': latest_batch.uploaded_at,
                'filename': latest_batch.filename
            },
            'equipment_data': serialized_data
        })


class PDFReportView(APIView):
    """API view to generate PDF report for the latest batch."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get the latest batch
        latest_batch = EquipmentBatch.objects.first()
        
        if not latest_batch:
            return Response(
                {'error': 'No data available for report generation'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get equipment data
        equipment_data = EquipmentData.objects.filter(batch=latest_batch)
        
        # Calculate statistics
        total_count = equipment_data.count()
        averages = equipment_data.aggregate(
            avg_flowrate=Avg('flowrate'),
            avg_pressure=Avg('pressure'),
            avg_temperature=Avg('temperature')
        )
        type_counts = equipment_data.values('type').annotate(count=Count('id'))
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center
        )
        elements.append(Paragraph("Chemical Equipment Report", title_style))
        elements.append(Spacer(1, 0.5 * inch))
        
        # Batch information
        elements.append(Paragraph(f"<b>Batch ID:</b> {latest_batch.id}", styles['Normal']))
        elements.append(Paragraph(f"<b>Uploaded:</b> {latest_batch.uploaded_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Paragraph(f"<b>Filename:</b> {latest_batch.filename}", styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Summary statistics
        elements.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Equipment Count', str(total_count)],
            ['Average Flowrate', f"{averages['avg_flowrate']:.2f}"],
            ['Average Pressure', f"{averages['avg_pressure']:.2f}"],
            ['Average Temperature', f"{averages['avg_temperature']:.2f}"],
        ]
        summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Type distribution
        elements.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
        type_data = [['Type', 'Count']]
        for item in type_counts:
            type_data.append([item['type'], str(item['count'])])
        
        type_table = Table(type_data, colWidths=[3 * inch, 2 * inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecfdf5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#a7f3d0')),
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Equipment data table
        elements.append(Paragraph("<b>Equipment Data</b>", styles['Heading2']))
        data_rows = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        for item in equipment_data:
            data_rows.append([
                item.equipment_name[:20],  # Truncate long names
                item.type,
                f"{item.flowrate:.2f}",
                f"{item.pressure:.2f}",
                f"{item.temperature:.2f}"
            ])
        
        data_table = Table(data_rows, colWidths=[1.5 * inch, 1.2 * inch, 1 * inch, 1 * inch, 0.8 * inch])
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c4b5fd')),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(data_table)
        
        # Build PDF
        doc.build(elements)
        
        # Return response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_batch_{latest_batch.id}.pdf"'
        
        return response


class EquipmentListView(APIView):
    """API view to list all equipment data from the latest batch."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        latest_batch = EquipmentBatch.objects.first()
        
        if not latest_batch:
            return Response({'equipment_data': []})
        
        equipment_data = EquipmentData.objects.filter(batch=latest_batch)
        serializer = EquipmentDataSerializer(equipment_data, many=True)
        
        return Response({
            'batch_id': latest_batch.id,
            'equipment_data': serializer.data
        })
