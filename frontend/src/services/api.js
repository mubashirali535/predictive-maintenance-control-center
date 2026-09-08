const API_URL = "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

export function startSimulation() {
  return request("/simulation/start", {
    method: "POST",
  });
}

export function stopSimulation() {
  return request("/simulation/stop", {
    method: "POST",
  });
}

export function resetSimulation() {
  return request("/simulation/reset", {
    method: "POST",
  });
}
export function getHistory() {
  return request("/history");
}