'use client'

import { useEffect, useState } from "react"
import { getState, postRobotSwitch, postRobotReset, postFanConfig } from "@/api-calls"
import { FAN_MODES, RUNNING_STATUS, REFRESH_RATE } from "@/const"

const localStyles = {
  pageRoot: "text-base flex flex-col items-center",
  logWindow: "h-100 w-7/10 max-w-200 border border-black dark:border-gray-200 rounded-sm overflow-y-scroll",
  robotControls: "text-lg w-80 py-6",
  button: "h-10 w-35 text-white rounded-lg bg-sky-700 hover:bg-sky-900",
  control: "h-8 px-2 rounded-lg border border-black dark:border-neutral-200 disabled:bg-neutral-500 disabled:hover:bg-neutral-500 disabled:text-neutral-600 disabled:border-neutral-600 dark:hover:bg-neutral-800 hover:bg-neutral-200",
  warnText: "text-amber-500",
  errorText: "text-red-800",
  justifyBetween: "flex justify-between",
}
const refreshInterval = 1000 / REFRESH_RATE

export default function Home() {
  const [state, setState] = useState({ logs: [] })
  const [fanMode, setFanMode] = useState(FAN_MODES.proportional)
  const [fanSpeed, setFanSpeed] = useState(50)
  const [isRunning, setIsRunning] = useState(false)

  const handleFanModeChange = event => {
    const newFanMode = event.target.value
    setFanMode(event.target.value)
    updateFanConfig(newFanMode, fanSpeed)
  }

  const handleFanSpeedChange = event => {
    const newFanSpeed = event.target.value
    setFanSpeed(newFanSpeed)
    updateFanConfig(fanMode, newFanSpeed)
  }

  const updateState = async () => {
    try {
      const response = await getState()
      if (response) {
        setState(response)
      }
    } catch (error) {
      console.error(error)
      console.error("Failed to retrieve robot state")
    }
  }

  const switchRobotMode = async () => {
    try {
      const response = await postRobotSwitch()
      if (response.ok) {
        setIsRunning(!isRunning)
      }
    } catch (error) {
      console.error("Failed to get response on switch request")
    }
  }

  const resetRobot = async () => {
    try {
      const response = await postRobotReset()
      if (response.ok) {
        setIsRunning(false)
      }
    } catch (error) {
      console.error("Failed to get response on reset request")
    }
  }

  const updateFanConfig = async (fanMode, fanSpeed) => {
    try {
      await postFanConfig(fanMode, fanSpeed)
    } catch (error) {
      console.error("Failed to get response on fan update request")
    }
  }

  useEffect(() => {
    updateState().then(() => {
      if (state.status === RUNNING_STATUS) {
        setIsRunning(true)
      }
    })
  }, [])

  useEffect(() => {
    const intervalId = setInterval(updateState, refreshInterval)
    return () => { clearInterval(intervalId) }
  }, [])

  return (
    <div className={localStyles.pageRoot}>
      <div className="w-65">
        <div className={localStyles.justifyBetween}>
          <label>Current temperature: </label>
          <span><strong>{state.current_temperature} °C</strong></span>
        </div>
        <div className={localStyles.justifyBetween}>
          <label>Current power consumption: </label>
          <span><strong>{state.current_power_consumption} W</strong></span>
        </div>
        <div className={localStyles.justifyBetween}>
          <label>Status: </label>
          <span><strong>{state.status}</strong></span>
        </div>
        <div className={localStyles.justifyBetween}>
          <label>Fan speed: </label>
          <span><strong>{state.fan_speed} %</strong></span>
        </div>
        <div className={localStyles.justifyBetween}>
          <label>Uptime: </label>
          <span><strong>{state.uptime}</strong></span>
        </div>
      </div>
      <div id="log-output" className={localStyles.logWindow}>
        {state.logs.map((log, index) => {
          let logStyle = ""
          if (log.includes("ERROR")) {
            logStyle = localStyles.errorText
          } else if (log.includes("WARN")) {
            logStyle = localStyles.warnText
          }
          return (
            <div className={logStyle} key={index}>{log}</div>
          )
        })}
      </div>
      <div id="robot-controls" className={localStyles.robotControls}>
        <div id="status-controls" className={localStyles.justifyBetween}>
          <button className={localStyles.button} onClick={switchRobotMode}>
            {isRunning ? "Turn off" : "Turn on"}
          </button>
          <button className={localStyles.button} onClick={resetRobot}>Reset</button>
        </div>
        <div id="fan-controls" className="mt-4">
          <div className={`${localStyles.justifyBetween} mb-2`}>
            <label>Fan operation mode: </label>
            <select
              name="fan-control"
              id="fan-control-select"
              className={localStyles.control}
              onInput={handleFanModeChange}
              defaultValue={fanMode}
            >
              <option value={FAN_MODES.proportional}>
                Proportional
              </option>
              <option value={FAN_MODES.static}>
                Static
              </option>
            </select>
          </div>
          <div className={localStyles.justifyBetween}>
            <label>Fan speed: </label>
            <input
              type="number"
              min="0"
              max="100"
              value={fanSpeed}
              disabled={fanMode === FAN_MODES.proportional}
              onChange={handleFanSpeedChange}
              className={localStyles.control}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
