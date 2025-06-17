Run Server: uvicorn data_dawgs_web.asgi:application --reload

Run Web UI: npm start

Make Migrations: 
    python manage.py makemigrations
    python manage.py migrate




ERRORS:

DataTable.js:267 Uncaught TypeError: Cannot read properties of undefined (reading 'replace')
    at DataTable.js:267:1
    at Array.map (<anonymous>)
    at DataTable (DataTable.js:241:1)
    at renderWithHooks (react-dom.development.js:14128:1)
    at updateFunctionComponent (react-dom.development.js:17013:1)
    at beginWork (react-dom.development.js:18725:1)
    at HTMLUnknownElement.callCallback (react-dom.development.js:3724:1)
    at Object.invokeGuardedCallbackDev (react-dom.development.js:3768:1)
    at invokeGuardedCallback (react-dom.development.js:3825:1)
    at beginWork$1 (react-dom.development.js:23694:1)
    at performUnitOfWork (react-dom.development.js:22945:1)
    at workLoopSync (react-dom.development.js:22865:1)
    at renderRootSync (react-dom.development.js:22838:1)
    at performConcurrentWorkOnRoot (react-dom.development.js:22233:1)
    at workLoop (scheduler.development.js:227:1)
    at flushWork (scheduler.development.js:205:1)
    at performWorkUntilDeadline (scheduler.development.js:442:1)
    at run (setImmediate.js:39:1)
    at runIfPresent (setImmediate.js:67:1)
    at onGlobalMessage (setImmediate.js:104:1)


    DataTable.js:99 The above error occurred in the <DataTable> component:

    at DataTable (http://localhost:3000/static/js/main.chunk.js:175:81)
    at div
    at RtlProvider (http://localhost:3000/static/js/0.chunk.js:73260:7)
    at ThemeProvider (http://localhost:3000/static/js/0.chunk.js:71740:5)
    at ThemeProvider (http://localhost:3000/static/js/0.chunk.js:73690:5)
    at ThemeProvider (http://localhost:3000/static/js/0.chunk.js:68904:14)
    at App

Consider adding an error boundary to your tree to customize error handling behavior.
Visit https://reactjs.org/link/error-boundaries to learn more about error boundaries.




react-dom.development.js:23254 Uncaught TypeError: Cannot read properties of undefined (reading 'replace')
    at DataTable.js:267:1
    at Array.map (<anonymous>)
    at DataTable (DataTable.js:241:1)
    at renderWithHooks (react-dom.development.js:14128:1)
    at updateFunctionComponent (react-dom.development.js:17013:1)
    at beginWork (react-dom.development.js:18725:1)
    at beginWork$1 (react-dom.development.js:23672:1)
    at performUnitOfWork (react-dom.development.js:22945:1)
    at workLoopSync (react-dom.development.js:22865:1)
    at renderRootSync (react-dom.development.js:22838:1)
    at recoverFromConcurrentError (react-dom.development.js:22330:1)
    at performConcurrentWorkOnRoot (react-dom.development.js:22243:1)
    at workLoop (scheduler.development.js:227:1)
    at flushWork (scheduler.development.js:205:1)
    at performWorkUntilDeadline (scheduler.development.js:442:1)
    at run (setImmediate.js:39:1)
    at runIfPresent (setImmediate.js:67:1)
    at onGlobalMessage (setImmediate.js:104:1)





    VM154:2 Uncaught ReferenceError: process is not defined
    at 4043 (<anonymous>:2:13168)
    at r (<anonymous>:2:306599)
    at 8048 (<anonymous>:2:9496)
    at r (<anonymous>:2:306599)
    at 8641 (<anonymous>:2:1379)
    at r (<anonymous>:2:306599)
    at <anonymous>:2:315627
    at <anonymous>:2:324225
    at <anonymous>:2:324229
    at e.onload (index.js:1714:1)