// Chart.js handler for confidence visualization

let confidenceChartInstance = null;

function displayConfidenceChart(predictions) {
    const canvas = document.getElementById('confidenceChart');
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart if any
    if (confidenceChartInstance) {
        confidenceChartInstance.destroy();
    }
    
    // Prepare data
    const labels = predictions.map(p => p.class);
    const data = predictions.map(p => p.confidence);
    const colors = predictions.map((p, index) => {
        if (index === 0) return 'rgba(40, 167, 69, 0.8)';  // Green for top
        if (index === 1) return 'rgba(255, 193, 7, 0.8)';  // Yellow for 2nd
        return 'rgba(108, 117, 125, 0.8)';  // Gray for 3rd
    });
    
    // Create chart
    confidenceChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Độ tin cậy (%)',
                data: data,
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.8', '1')),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',  // Horizontal bar
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.x.toFixed(1) + '%';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}
