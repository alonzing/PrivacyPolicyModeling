# Privacy Policy Modeling - Front End

For back-end instructions, please refer to [this](https://github.com/alonzing/PrivacyPolicyModeling/tree/master/) page.

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 7.3.9.

## Development server
### Setting Up The Environment
* Install [Node.js](https://nodejs.org)
* Run `npm install -g @angular/cli`
* Run `npm install --save-dev @angular-devkit/build-angular`
* Run `npm audit fix`

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Connecting to Flask Server
 * Run with python 2.7 `python /src/server/management_utils/http_server.py`
 * Make sure the server is listening to the same port as is written in `ng-server/src/pp.service.ts` (i.e. `serverUrl = 'http://localhost:5000/';`). The default is `5000`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
