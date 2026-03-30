This folder takes the Excel Inventory Forecast in Python and upgrades it into an app from Angular.

Commented code refers to past versions of the program. It has been improved and replaced.

This can be made into a PWA by first installing Angular's PWA program and the Global Server, then running ng build.

PWA install: ng add @angular/pwa
Global Server install: npm install -g http-server
Run app: http-server -c-1 dist/my-pwa-app

Note: the Excel file input is slightly less strict compared to Python. You can add additional headers (up to 10 headers) to your Excel file. 
Additionally, so long as a sheet contains the latest year number, you can use any name for that sheet.

Example Excel files have been added. More updates will be added to fix the exported Excel format. 
Older versions of code are found in the scrappedcode.txt file, these lines have been replaced by better versions.
Possible ideas to add to the app will be placed in ideas.txt.
Commented code will be removed once the final program is complete.
