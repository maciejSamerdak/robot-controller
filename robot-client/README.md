# Robot Client
Client app for interacting with Robot API.
Built with [**Next.js**](https://nextjs.org/)

## Installation
Install dependencies:
```bash
npm install
```

## Running
### Development server
```bash
npm run dev
```
### Production server
```bash
npm run build

npm run start
```
### Docker
```bash
docker build -t robot-client .

docker run -p 3000:3000 --name robot-client robot-client
```
In each case, application will be available at http://localhost:3000

## Configuration
### Environment variables
Environment variables can be set with `./.env` file. Dotenv file is not required for application to run.

 - `ROBOT_CLIENT_BACKEND_URL` - points to Robot API, defaults to `http://localhost:5487`
 - `ROBOT_CLIENT_REFRESH_RATE` - sets refresh rate in Hz for fetching state updates, defaults to `10`
 - `ROBOT_CLIENT_REQUEST_TIMEOUT_MS` - sets timeout for API requests in milliseconds, defaults to `5000`

 ### Docker build arguments
To be used with `docker build` using `--build-arg`
 - `host` - host on container itself, defaults to `0.0.0.0`
 - `port` - port exposed on container, defaults to `3000`
 - `api` - points to Robot API, defaults to `http://localhost:5487`
 - `refresh_rate` - sets refresh rate in Hz for fetching state updates, defaults to `10`
