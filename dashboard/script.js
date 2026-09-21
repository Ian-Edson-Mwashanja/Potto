// POTTO DASHBOARD
// Flask API
const API_URL ="http://127.0.0.1:5000/api/anomalies";
let lastKnownId = null;
let firstLoad = true;
// Store anomalies globally
let allAnomalies = [];
// CREATE MAP
const map = L.map("map").setView(
    [-18.1234, 31.0567],
    15
);
// OpenStreetMap tiles
L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);
// Marker layer
const markerLayer = L.layerGroup().addTo(map);
// LOAD ANOMALIES
async function loadAnomalies() {
    try {
        const response =
            await fetch(API_URL);
        if (!response.ok) {
            throw new Error(
                "API request failed"
            );
        }
        const anomalies =
            await response.json();
        checkForNewDetection(anomalies);
        console.log(
            "Received anomalies:",
            anomalies
        );
        allAnomalies = anomalies;
        updateStatistics(
            anomalies
        );
        displayMarkers(
            anomalies
        );
        displayTable(
            anomalies
        );
        updateLastUpdate();
    } catch (error) {
        console.error(
            "Error:",
            error
        );
        document.getElementById(
            "detectionTable"
        ).innerHTML = `
            <tr>
                <td colspan="7">
                    ❌ Could not connect to Potto API.
                </td>
            </tr>
        `;
    }
}
// UPDATE STATISTICS
function updateStatistics(anomalies) {
    const total =
        anomalies.length;
    const severe =
        anomalies.filter(
            anomaly =>
                anomaly.severity === "severe"
        ).length;
    const moderate =
        anomalies.filter(
            anomaly =>
                anomaly.severity === "moderate"
        ).length;
    const low =
        anomalies.filter(
            anomaly =>
                anomaly.severity === "low"
        ).length;
    document.getElementById(
        "totalAnomalies"
    ).textContent = total;
    document.getElementById(
        "severeAnomalies"
    ).textContent = severe;
    document.getElementById(
        "moderateAnomalies"
    ).textContent = moderate;
    document.getElementById(
        "lowAnomalies"
    ).textContent = low;
}
// MAP MARKERS
function displayMarkers(anomalies) {
    // Remove old markers
    markerLayer.clearLayers();
    anomalies.forEach(
        anomaly => {
            let icon;
            // Select icon based on severity
            if (
                anomaly.severity ===
                "severe"
            ) {
                icon = "🔴";
            }
            else if (
                anomaly.severity ===
                "moderate"
            ) {
                icon = "🟠";
            }
            else {
                icon = "🟢";
            }
            const marker =
                L.marker([
                    anomaly.latitude,
                    anomaly.longitude
                ]);
            marker.bindPopup(`

                <div>

                    <h3>
                        ${anomaly.type}
                    </h3>

                    <p>
                        ${icon}
                        Severity:
                        <strong>
                            ${anomaly.severity}
                        </strong>
                    </p>

                    <p>
                        Confidence:
                        <strong>
                            ${(anomaly.confidence * 100).toFixed(2)}%
                        </strong>
                    </p>

                    <p>
                        Latitude:
                        ${anomaly.latitude}
                    </p>

                    <p>
                        Longitude:
                        ${anomaly.longitude}
                    </p>

                    <p>
                        Device:
                        ${anomaly.device_id}
                    </p>

                    <p>
                        Detected:
                        ${anomaly.detected_at}
                    </p>
                </div>
            `);
            markerLayer.addLayer(
                marker
            );
        }
    );
}
// DISPLAY TABLE
function displayTable(anomalies) {
    const table =
        document.getElementById(
            "detectionTable"
        );
    table.innerHTML = "";
    if (
        anomalies.length === 0
    ) {
        table.innerHTML = `
            <tr>
                <td colspan="7">
                    No detections found.
                </td>
            </tr>
        `;
        return;
    }
    anomalies.forEach(
        anomaly => {
            const row =
                document.createElement(
                    "tr"
                );
            row.innerHTML = `
                <td>
                    <strong>
                        ${anomaly.type}
                    </strong>
                </td>
                <td>
                    <span
                        class="
                            severity
                            severity-${anomaly.severity}
                        "
                    >
                        ${anomaly.severity}
                    </span>
                </td>
                <td>
                    ${(anomaly.confidence * 100).toFixed(2)}%
                </td>
                <td>
                    ${anomaly.latitude}
                </td>
                <td>
                    ${anomaly.longitude}
                </td>
                <td>
                    ${anomaly.device_id}
                </td>
                <td>
                    ${anomaly.detected_at}
                </td>
            `;
            table.appendChild(
                row
            );

        }
    );
}
// SEARCH / FILTER
function filterDetections() {
    const search =
        document
            .getElementById(
                "searchInput"
            )
            .value
            .toLowerCase();
    const filtered =
        allAnomalies.filter(
            anomaly =>

                anomaly.type
                    .toLowerCase()
                    .includes(search)

                ||

                anomaly.severity
                    .toLowerCase()
                    .includes(search)

                ||

                anomaly.device_id
                    .toLowerCase()
                    .includes(search)

        );
    displayTable(
        filtered
    );
}
// LAST UPDATE
function updateLastUpdate() {
    const now =
        new Date();
    document.getElementById(
        "lastUpdate"
    ).textContent =
        now.toLocaleTimeString();

}
// AUTOMATIC REFRESH
// Refresh every 10 seconds
setInterval(
    () => {

        loadAnomalies();
        loadAnalytics();

    },
    10000
);
// START DASHBOARD
loadAnomalies();
loadAnalytics();
// ANALYTICS
let typeChart;
let severityChart;
async function loadAnalytics() {
    try {
        const response =
            await fetch(
                "http://127.0.0.1:5000/api/analytics"
            );
        const data =
            await response.json();
        createTypeChart(
            data.by_type
        );
        createSeverityChart(
            data.severity
        );
    } catch (error) {

        console.error(
            "Analytics error:",
            error
        );

    }

}
// TYPE CHART
function createTypeChart(data) {

    const labels =
        data.map(
            item => item.type
        );


    const values =
        data.map(
            item => item.total
        );


    const ctx =
        document
            .getElementById(
                "typeChart"
            );
    if (typeChart) {

        typeChart.destroy();

    }
    typeChart = new Chart(
        ctx,
        {
            type: "bar",

            data: {

                labels: labels,

                datasets: [{

                    label:
                        "Number of detections",

                    data: values

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {
                        display: false
                    }

                }
            }
        }
    );
}
// SEVERITY CHART
function createSeverityChart(
    severity
) {
    const ctx =
        document
            .getElementById(
                "severityChart"
            );
    if (severityChart) {
        severityChart.destroy();
    }
    severityChart = new Chart(
        ctx,
        {
            type: "doughnut",

            data: {

                labels: [
                    "Severe",
                    "Moderate",
                    "Low"
                ],

                datasets: [{

                    data: [

                        severity.severe,

                        severity.moderate,

                        severity.low

                    ]

                }]

            },
            options: {
                responsive: true
            }
        }
    );
}
// LOAD PRIORITIES
async function loadPriorities() {
    try {
        const response =
            await fetch(
                "http://127.0.0.1:5000/api/priorities"
            );
        const priorities =
            await response.json();
        displayPriorities(
            priorities
        );
    } catch (error) {

        console.error(
            "Priority error:",
            error
        );
    }
}
// DISPLAY PRIORITIES
function displayPriorities(
    priorities
) {
    const table =
        document.getElementById(
            "priorityTable"
        );
    table.innerHTML = "";
    priorities
        .slice(0, 10)
        .forEach(
            item => {
                const row =
                    document.createElement(
                        "tr"
                    );
                row.innerHTML = `
                    <td>
                        <span
                            class="
                                severity
                                severity-${
                                    item.priority
                                        .toLowerCase()
                                }
                            "
                        >
                            ${item.priority}
                        </span>
                    </td>
                    <td>
                        ${item.type}
                    </td>
                    <td>
                        ${item.severity}
                    </td>
                    <td>

                        ${
                            (
                                item.confidence
                                * 100
                            ).toFixed(2)
                        }%

                    </td>
                    <td>
                        ${item.priority_score}
                    </td>
                    <td>
                        ${item.latitude},
                        ${item.longitude}
                    </td>
                `;
                table.appendChild(
                    row
                );
            }
        );
}
function checkForNewDetection(data) {
    if (data.length === 0) {
        return;
    }
    // Get the newest detection
    const newestDetection = data.reduce((latest, current) => {
        return current.id > latest.id ? current : latest;
    });
    // First time loading the dashboard
    if (firstLoad) {
        lastKnownId = newestDetection.id;
        firstLoad = false;
        return;
    }
    // Check if a new detection has appeared
    if (newestDetection.id > lastKnownId) {
        lastKnownId = newestDetection.id;
        showNotification(newestDetection);
    }
}
function showNotification(detection) {
    const notification = document.getElementById("notification");
    const message = document.getElementById("notificationMessage");
    message.textContent =
        `${detection.type} detected with ${(detection.confidence * 100).toFixed(1)}% confidence.`;
    notification.style.display = "block";
    // Hide notification after 5 seconds
    setTimeout(() => {
        notification.style.display = "none";
    }, 5000);
}