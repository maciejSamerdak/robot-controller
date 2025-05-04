export const BACKEND_URL = process.env.ROBOT_CLIENT_BACKEND_URL || "http://localhost:5487"
export const REFRESH_RATE = process.env.ROBOT_CLIENT_REFRESH_RATE || 10
export const REQUEST_TIMEOUT_MS = process.env.ROBOT_CLIENT_REQUEST_TIMEOUT_MS || 5000
export const FAN_MODES = {static: "static", proportional: "proportional"}
export const RUNNING_STATUS = "running"
