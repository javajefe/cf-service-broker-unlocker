CloudFoundry Service Broker Unlocker
========================

This tool is based on [CloudFoundry Service Broker v2 implementation in Python](https://github.com/dwatrous/cf-service-broker-python) written by Daniel Watrous.

Working with CloudFoundry you can get in the following situation:
1. you've created an Application implementing [Service Broker API](http://docs.cloudfoundry.org/services/api.html) and deployed it in your CF account (org)
2. then you've created Service Broker from your Application using `cf create-service-broker`
3. then you've created a Service from you Service Broker using `cf create-service`
4. after some time you decide to delete your Service using `cf delete-service` but something went wrong and you get an error like this: "The service broker returned an invalid response for the request to http://your-service-broker-url/v2/service_instances/2c955c45-8e56-4367-91d6-b6ef496b940d"

So you can't delete your Service because the Service Broker returns some error. Potential causes for the situation can be:
- the Service Broker calls external resource and get some error
- the Service Broker can't connect to external resource at all
- the Service Broker is buggy
- etc.

Worse of all you can't delete your Service Broker too because there is a Service created by the Service Broker, so CF rejects such delete attempts. And that also means you can't delete your Application, so you're wasting your quotas (disk and memory).

In such situation you can use this tool as a workaround to clean your account from the Service, Service Broker and Application. Just keep in mind you should also be sure you're able to clean the external resource the Service Broker really uses to provision the Service.

So, how to use it:
1. deploy the tool, which is a trivial Application implementing only small part of Service Broker API. Just use `cf push`
2. list all your Applications using `cf apps` and find the Application implementing the Service Broker (let's name it **buggy-app**) and the tool Application (let's name it **unlocker-app**)
3. look at `urls` column for both, let's name these urls **buggy-app-url** and **unlocker-app-url**
4. now change the routes for these Applications: 
```
cf map-route unlocker-app cfapps.io --hostname buggy-app-url-hostname
cf unmap-route buggy-app cfapps.io --hostname buggy-app-url-hostname
```
5. and then try to delete your Service, Service Broker abd Application again
```
cf delete-service buggy-service
cf delete-service-broker buggy-service-broker
cf delete buggy-app
```
