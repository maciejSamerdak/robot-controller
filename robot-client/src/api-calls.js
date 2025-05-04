import { BACKEND_URL, FAN_MODES, REQUEST_TIMEOUT_MS } from "@/const"

const API_PATHS = {
    robot_state: "/robot",
    robot_switch: "/robot/switch",
    robot_reset: "/robot/reset",
    robot_fan: "/robot/fan",
}


export const getState = async () => {
    let response
    try {
        response = await fetch(BACKEND_URL + API_PATHS.robot_state, { signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS) })
    } catch (error) {
        console.error(error)
        throw error
    }

    if (response.ok) {
        return await response.json()
    } else {
        console.error(`Failed to retrieve state from API with status ${response.status}`)
        return null
    }
}

export const postRobotSwitch = async () => {
    let response
    try {
        response = await fetch(BACKEND_URL + API_PATHS.robot_switch, { method: "POST", signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS) })
    } catch (error) {
        console.error(error)
        throw error
    }

    if (!response.ok) {
        console.error(`Failed to switch robot mode with status ${response.status}`)
    }
    return response
}

export const postRobotReset = async () => {
    let response
    try {
        response = await fetch(BACKEND_URL + API_PATHS.robot_reset, { method: "POST", signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS) })
    } catch (error) {
        console.error(error)
        throw error
    }

    if (!response.ok) {
        console.error(`Failed to reset robot with status ${response.status}`)
    }
    return response
}

export const postFanConfig = async (fanMode, fanSpeed) => {
    const body = fanMode === FAN_MODES.proportional ? { mode: fanMode } : { mode: fanMode, value: fanSpeed }
    let response
    try {
        response = await fetch(
            BACKEND_URL + API_PATHS.robot_fan,
            {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body),
                signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS)
            }
        )
    } catch (error) {
        console.error(error)
        throw error
    }

    if (!response.ok) {
        console.error(`Failed to switch robot mode with status ${response.status}`)
    }
    return response
}
