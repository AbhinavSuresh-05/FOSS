import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Bar, Scatter } from 'react-chartjs-2';
import './EquipmentChart.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const EquipmentChart = ({ typeDistribution, equipmentData }) => {
    // Bar Chart - Type Distribution
    const barChartData = {
        labels: Object.keys(typeDistribution),
        datasets: [
            {
                label: 'Equipment Count',
                data: Object.values(typeDistribution),
                backgroundColor: [
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(249, 115, 22, 0.8)',
                    'rgba(236, 72, 153, 0.8)',
                    'rgba(234, 179, 8, 0.8)',
                ],
                borderColor: [
                    'rgba(139, 92, 246, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(249, 115, 22, 1)',
                    'rgba(236, 72, 153, 1)',
                    'rgba(234, 179, 8, 1)',
                ],
                borderWidth: 2,
                borderRadius: 8,
            },
        ],
    };

    const barChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Equipment Type Distribution',
                color: '#fff',
                font: {
                    size: 16,
                    weight: '600',
                },
                padding: {
                    bottom: 20,
                },
            },
            tooltip: {
                backgroundColor: 'rgba(30, 27, 75, 0.9)',
                titleColor: '#fff',
                bodyColor: '#e2e8f0',
                borderColor: 'rgba(139, 92, 246, 0.3)',
                borderWidth: 1,
                cornerRadius: 8,
                padding: 12,
            },
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.6)',
                },
            },
            y: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.6)',
                    stepSize: 1,
                },
                beginAtZero: true,
            },
        },
    };

    // Scatter Chart - Temperature vs Pressure
    const scatterChartData = {
        datasets: [
            {
                label: 'Temp vs Pressure',
                data: equipmentData.map(item => ({
                    x: item.temperature,
                    y: item.pressure,
                })),
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 2,
                pointRadius: 8,
                pointHoverRadius: 12,
            },
        ],
    };

    const scatterChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Temperature vs Pressure',
                color: '#fff',
                font: {
                    size: 16,
                    weight: '600',
                },
                padding: {
                    bottom: 20,
                },
            },
            tooltip: {
                backgroundColor: 'rgba(30, 27, 75, 0.9)',
                titleColor: '#fff',
                bodyColor: '#e2e8f0',
                borderColor: 'rgba(139, 92, 246, 0.3)',
                borderWidth: 1,
                cornerRadius: 8,
                padding: 12,
                callbacks: {
                    label: (context) => {
                        return `Temp: ${context.parsed.x.toFixed(1)}°, Pressure: ${context.parsed.y.toFixed(1)}`;
                    },
                },
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Temperature (°C)',
                    color: 'rgba(255, 255, 255, 0.6)',
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.6)',
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Pressure (bar)',
                    color: 'rgba(255, 255, 255, 0.6)',
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.6)',
                },
            },
        },
    };

    const hasData = Object.keys(typeDistribution).length > 0;

    if (!hasData) {
        return null;
    }

    return (
        <div className="charts-container">
            <div className="chart-card">
                <div className="chart-wrapper">
                    <Bar data={barChartData} options={barChartOptions} />
                </div>
            </div>
            <div className="chart-card">
                <div className="chart-wrapper">
                    <Scatter data={scatterChartData} options={scatterChartOptions} />
                </div>
            </div>
        </div>
    );
};

export default EquipmentChart;
