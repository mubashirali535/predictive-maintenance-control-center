import { useEffect, useMemo, useState } from "react";
import "./App.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import { connectWebSocket } from "./services/websocket";

import {
  startSimulation,
  stopSimulation,
  resetSimulation,
  getHistory,
} from "./services/api";


/* =========================================================
   REUSABLE SENSOR CHART
========================================================= */

function SensorChart({
  title,
  data,
  dataKey,
  yLabel,
  unit,
  decimals = 1,
}) {
  return (
    <section className="chart-panel">

      <div className="chart-header">
        <p className="section-label">LIVE SENSOR DATA</p>
        <h2>{title}</h2>
      </div>

      <div className="chart-container">

        {data.length === 0 ? (
          <div className="no-chart-data">
            Waiting for sensor data...
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">

            <LineChart
              data={data}
              margin={{
                top: 10,
                right: 20,
                left: 10,
                bottom: 20,
              }}
            >

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis
                dataKey="row"
                tick={{ fontSize: 12 }}
                label={{
                  value: "Simulation Row",
                  position: "insideBottom",
                  offset: -12,
                }}
              />

              <YAxis
                domain={["auto", "auto"]}
                tick={{ fontSize: 12 }}
                label={{
                  value: yLabel,
                  angle: -90,
                  position: "insideLeft",
                }}
              />

              <Tooltip
                formatter={(value) => [
                  `${Number(value).toFixed(decimals)} ${unit}`,
                  title,
                ]}
                labelFormatter={(label) => `Row ${label}`}
              />

              <Line
                type="monotone"
                dataKey={dataKey}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 5 }}
                isAnimationActive={false}
              />

            </LineChart>

          </ResponsiveContainer>
        )}

      </div>

    </section>
  );
}


/* =========================================================
   FAILURE PROBABILITY CHART
========================================================= */

function FailureProbabilityChart({ data }) {
  return (
    <section className="chart-panel">

      <div className="chart-header">
        <p className="section-label">MODEL PREDICTION</p>
        <h2>Failure Probability</h2>
      </div>

      <div className="chart-container">

        {data.length === 0 ? (
          <div className="no-chart-data">
            Waiting for prediction data...
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">

            <LineChart
              data={data}
              margin={{
                top: 10,
                right: 20,
                left: 10,
                bottom: 20,
              }}
            >

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis
                dataKey="row"
                tick={{ fontSize: 12 }}
                label={{
                  value: "Simulation Row",
                  position: "insideBottom",
                  offset: -12,
                }}
              />

              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 12 }}
                label={{
                  value: "Probability (%)",
                  angle: -90,
                  position: "insideLeft",
                }}
              />

              <Tooltip
                formatter={(value) => [
                  `${Number(value).toFixed(1)}%`,
                  "Failure Probability",
                ]}
                labelFormatter={(label) => `Row ${label}`}
              />

              <Line
                type="monotone"
                dataKey="failure_probability"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 5 }}
                isAnimationActive={false}
              />

            </LineChart>

          </ResponsiveContainer>
        )}

      </div>

    </section>
  );
}


/* =========================================================
   MAIN APP
========================================================= */

function App() {

  const [machineData, setMachineData] = useState(null);

  const [isConnected, setIsConnected] = useState(false);

  const [simulationStatus, setSimulationStatus] =
    useState("Ready");

  const [history, setHistory] = useState([]);

  const [isLoading, setIsLoading] = useState(false);


  /* =======================================================
     WEBSOCKET CONNECTION
  ======================================================= */

  useEffect(() => {

    const websocket = connectWebSocket({

      onOpen: () => {

        console.log(
          "Dashboard WebSocket connected"
        );

        setIsConnected(true);

      },


      onMessage: (data) => {

        console.log(
          "Machine event received:",
          data
        );


        setMachineData(data);


        setHistory((previousHistory) => {

          const exists = previousHistory.some(
            (item) => item.row === data.row
          );

          if (exists) {
            return previousHistory;
          }

          return [
            ...previousHistory,
            data,
          ].slice(-100);

        });

      },


      onClose: () => {

        console.log(
          "Dashboard WebSocket disconnected"
        );

        setIsConnected(false);

      },


      onError: (error) => {

        console.error(
          "Dashboard WebSocket error:",
          error
        );

        setIsConnected(false);

      },

    });


    return () => {

      websocket.close();

    };

  }, []);


  /* =======================================================
     LOAD BACKEND HISTORY
  ======================================================= */

  useEffect(() => {

    const loadHistory = async () => {

      try {

        const result = await getHistory();

        console.log(
          "History loaded:",
          result
        );


        if (Array.isArray(result)) {

          setHistory(result.slice(-100));


          if (result.length > 0) {

            setMachineData(
              result[result.length - 1]
            );

          }

        }

      } catch (error) {

        console.error(
          "Failed to load history:",
          error
        );

      }

    };


    loadHistory();

  }, []);


  /* =======================================================
     START SIMULATION
  ======================================================= */

  const handleStart = async () => {

    if (isLoading) {
      return;
    }

    try {

      setIsLoading(true);

      const result = await startSimulation();

      console.log(
        "Simulation started:",
        result
      );

      if (result?.started) {

        setSimulationStatus("Running");

      }

    } catch (error) {

      console.error(
        "Start simulation failed:",
        error
      );

    } finally {

      setIsLoading(false);

    }

  };


  /* =======================================================
     STOP SIMULATION
  ======================================================= */

  const handleStop = async () => {

    if (isLoading) {
      return;
    }

    try {

      setIsLoading(true);

      const result = await stopSimulation();

      console.log(
        "Simulation stopped:",
        result
      );

      setSimulationStatus("Stopped");

    } catch (error) {

      console.error(
        "Stop simulation failed:",
        error
      );

    } finally {

      setIsLoading(false);

    }

  };


  /* =======================================================
     RESET SIMULATION
  ======================================================= */

  const handleReset = async () => {

    if (isLoading) {
      return;
    }

    try {

      setIsLoading(true);

      const result = await resetSimulation();

      console.log(
        "Simulation reset:",
        result
      );


      setMachineData(null);

      setHistory([]);

      setSimulationStatus("Ready");

    } catch (error) {

      console.error(
        "Reset simulation failed:",
        error
      );

    } finally {

      setIsLoading(false);

    }

  };


  /* =======================================================
     CHART DATA
  ======================================================= */

  const chartData = useMemo(() => {

    return history
      .slice(-30)
      .map((item) => ({

        row: item.row,

        air_temperature:
          item.sensor_data?.air_temperature ?? null,

        process_temperature:
          item.sensor_data?.process_temperature ?? null,

        rotational_speed:
          item.sensor_data?.rotational_speed ?? null,

        torque:
          item.sensor_data?.torque ?? null,

        tool_wear:
          item.sensor_data?.tool_wear ?? null,

        failure_probability:
          item.prediction?.failure_probability != null
            ? item.prediction.failure_probability * 100
            : null,

      }));

  }, [history]);


  /* =======================================================
     CURRENT MACHINE RISK
  ======================================================= */

  const riskLevel =
    machineData?.prediction?.risk_level || "--";


  const riskClass =
    riskLevel.toLowerCase();


  /* =======================================================
     CURRENT FAILURE PROBABILITY
  ======================================================= */

  const failureProbability =
    machineData?.prediction?.failure_probability != null
      ? (
          machineData.prediction.failure_probability * 100
        ).toFixed(1)
      : "--";


  /* =======================================================
     CURRENT ALERT
  ======================================================= */

  const currentAlert =
    machineData?.prediction?.alert ||
    "No active alerts";


  /* =======================================================
     RENDER
  ======================================================= */

  return (

    <div className="dashboard">


      {/* =================================================
          HEADER
      ================================================= */}

      <header className="dashboard-header">

        <div>

          <h1>
            Predictive Maintenance
          </h1>

          <p>
            Control Center
          </p>

        </div>


        <div className="connection-status">

          <span
            className={`status-dot ${
              isConnected
                ? "connected"
                : "disconnected"
            }`}
          ></span>

          {isConnected
            ? "SYSTEM ONLINE"
            : "SYSTEM OFFLINE"}

        </div>

      </header>


      {/* =================================================
          MACHINE STATUS
      ================================================= */}

      <section className="status-panel">

        <div>

          <p className="section-label">
            MACHINE STATUS
          </p>

          <h2
            className={`machine-status ${riskClass}`}
          >
            {riskLevel}
          </h2>

        </div>


        <div className="machine-info">

          <span>
            Machine 01
          </span>

          <span>
            Simulation: {simulationStatus}
          </span>

        </div>

      </section>


      {/* =================================================
          SENSOR CARDS
      ================================================= */}

      <section className="sensor-grid">


        <div className="sensor-card">

          <p>
            Air Temperature
          </p>

          <h2>

            {machineData?.sensor_data?.air_temperature != null
              ? machineData.sensor_data.air_temperature.toFixed(1)
              : "--"}

            <span> K</span>

          </h2>

        </div>


        <div className="sensor-card">

          <p>
            Process Temperature
          </p>

          <h2>

            {machineData?.sensor_data?.process_temperature != null
              ? machineData.sensor_data.process_temperature.toFixed(1)
              : "--"}

            <span> K</span>

          </h2>

        </div>


        <div className="sensor-card">

          <p>
            Rotational Speed
          </p>

          <h2>

            {machineData?.sensor_data?.rotational_speed != null
              ? machineData.sensor_data.rotational_speed.toFixed(0)
              : "--"}

            <span> RPM</span>

          </h2>

        </div>


        <div className="sensor-card">

          <p>
            Torque
          </p>

          <h2>

            {machineData?.sensor_data?.torque != null
              ? machineData.sensor_data.torque.toFixed(1)
              : "--"}

            <span> Nm</span>

          </h2>

        </div>


        <div className="sensor-card">

          <p>
            Tool Wear
          </p>

          <h2>

            {machineData?.sensor_data?.tool_wear != null
              ? machineData.sensor_data.tool_wear.toFixed(0)
              : "--"}

            <span> min</span>

          </h2>

        </div>


      </section>


      {/* =================================================
          REAL-TIME SENSOR ANALYTICS
      ================================================= */}

      <section className="charts-section">

        <div className="charts-title">

          <p className="section-label">
            REAL-TIME MONITORING
          </p>

          <h2>
            Machine Sensor Analytics
          </h2>

        </div>


        <SensorChart
          title="Air Temperature"
          data={chartData}
          dataKey="air_temperature"
          yLabel="Temperature (K)"
          unit="K"
          decimals={1}
        />


        <SensorChart
          title="Process Temperature"
          data={chartData}
          dataKey="process_temperature"
          yLabel="Temperature (K)"
          unit="K"
          decimals={1}
        />


        <SensorChart
          title="Rotational Speed"
          data={chartData}
          dataKey="rotational_speed"
          yLabel="Speed (RPM)"
          unit="RPM"
          decimals={0}
        />


        <SensorChart
          title="Torque"
          data={chartData}
          dataKey="torque"
          yLabel="Torque (Nm)"
          unit="Nm"
          decimals={1}
        />


        <SensorChart
          title="Tool Wear"
          data={chartData}
          dataKey="tool_wear"
          yLabel="Tool Wear (min)"
          unit="min"
          decimals={0}
        />


        <FailureProbabilityChart
          data={chartData}
        />

      </section>


      {/* =================================================
          RISK SUMMARY
      ================================================= */}

      <section className="risk-panel">

        <div>

          <p className="section-label">
            FAILURE PROBABILITY
          </p>

          <div className="risk-value">
            {failureProbability}%
          </div>

        </div>


        <div className="risk-status">

          <p>
            RISK LEVEL
          </p>

          <strong
            className={`risk-level ${riskClass}`}
          >
            {riskLevel}
          </strong>

        </div>

      </section>


      {/* =================================================
          SIMULATION CONTROLS
      ================================================= */}

      <section className="control-panel">

        <div>

          <p className="section-label">
            SIMULATION CONTROL
          </p>

          <h2>
            Machine Simulation
          </h2>

        </div>


        <div className="control-buttons">

          <button
            className="start-button"
            onClick={handleStart}
            disabled={isLoading}
          >
            START
          </button>


          <button
            className="stop-button"
            onClick={handleStop}
            disabled={isLoading}
          >
            STOP
          </button>


          <button
            className="reset-button"
            onClick={handleReset}
            disabled={isLoading}
          >
            RESET
          </button>

        </div>

      </section>


      {/* =================================================
          ALERTS
      ================================================= */}

      <section className="alerts-panel">

        <div>

          <p className="section-label">
            ALERTS
          </p>

          <h2>
            Machine Event
          </h2>

        </div>


        <div
          className={`alert-message ${
            riskClass || "normal"
          }`}
        >

          {currentAlert}

        </div>

      </section>


      {/* =================================================
          PREDICTION HISTORY
      ================================================= */}

      <section className="history-panel">

        <div>

          <p className="section-label">
            PREDICTION HISTORY
          </p>

          <h2>
            Recent Predictions
          </h2>

        </div>


        <div className="history-list">

          {history.length === 0 ? (

            <div className="no-history">
              No prediction history
            </div>

          ) : (

            history
              .slice()
              .reverse()
              .slice(0, 10)
              .map((item, index) => (

                <div
                  className="history-row"
                  key={`${item.row}-${index}`}
                >

                  <span>
                    Row {item.row}
                  </span>


                  <span>

                    {item.prediction?.failure_probability != null
                      ? (
                          item.prediction.failure_probability
                          * 100
                        ).toFixed(1)
                      : "--"}

                    %

                  </span>


                  <span
                    className={`history-risk ${
                      item.prediction?.risk_level
                        ?.toLowerCase() || ""
                    }`}
                  >
                    {item.prediction?.risk_level || "--"}
                  </span>


                  <span>
                    {item.prediction?.status || "--"}
                  </span>

                </div>

              ))

          )}

        </div>

      </section>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer className="dashboard-footer">

        <span>
          Predictive Maintenance Control Center
        </span>

        <span>
          Real-Time AI Monitoring
        </span>

      </footer>


    </div>

  );

}


export default App;