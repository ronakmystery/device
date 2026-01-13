const MAX_POINTS = 300;

const ctx = document.getElementById("relayChart").getContext("2d");

document.getElementById("relayToggle").onclick = async () => {
    await fetch("/relay/toggle", { method: "POST" });
    updateState();
};


const relayChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Relay (1 = ON, 0 = OFF)",
            data: [],
            borderWidth: 2,
            stepped: true
        }]
    },
    options: {
        animation: false,
        responsive: true,
        scales: {
            x: { display: false },
            y: {
                min: 0,
                max: 1,
                ticks: {
                    stepSize: 1
                }
            }
        }
    }
});

async function updateChart() {
    const res = await fetch("/history");
    const history = await res.json();

    const data = history.slice(-MAX_POINTS);
    const labels = data.map((_, i) => i);
    const relay = data.map(s => s.relay ? 1 : 0);

    relayChart.data.labels = labels;
    relayChart.data.datasets[0].data = relay;
    relayChart.update();
}

async function updateState() {
    const res = await fetch("/state");
    const state = await res.json();

    document.getElementById("relayState").textContent =
        state.relay ? "ON" : "OFF";
}

setInterval(updateChart, 1000);
setInterval(updateState, 1000);

updateChart();
updateState();
