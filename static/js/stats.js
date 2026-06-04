const ctx = document.getElementById("classChart");

if (ctx) {
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: window.chartLabels,
            datasets: [{
                label: "Количество распознаваний",
                data: window.chartValues,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#dbe7f3"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.08)"
                    }
                },
                y: {
                    ticks: {
                        color: "#dbe7f3"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.08)"
                    }
                }
            }
        }
    });
}