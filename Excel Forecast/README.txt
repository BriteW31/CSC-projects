This folder takes the Excel Inventory Forecast in Python and upgrades it into an app from Angular.

This can be made into a PWA by first installing Angular's PWA program and the Global Server, then running ng build.

PWA install: ng add @angular/pwa
Global Server install: npm install -g http-server
Run app: http-server -c-1 dist/my-pwa-app

Note: the Excel file input is slightly less strict compared to Python. You can add additional headers (up to 10 headers) to your Excel file. 
Additionally, so long as a sheet contains the latest year number, you can use any name for that sheet.

An example Excel file has been added. More updates will be added to fix the exported Excel format.

Sample Outputs are also added.
