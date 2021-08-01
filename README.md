# Transporteasy

### Digital Innovation Lab project - Group05

## Who are we ?

We are students from the Politecnico di Milano, studying Computer Science and Datascience in the MSc Computer Science and Engineering. This project has been done during the Digital Innovation Lab course.

<p align="center">
<img src="/images/Logo_Politecnico_Milano.png">
</p>

## What is Transporteasy ?

The main goal of our applications is to let public transportation users know about possible disruptions of the network, as soon as they happen, and give them the ability to plan their route accordingly. For this, they can participate in and benefit from an active community that can report disruptions (i.e. delays, accidents, blocked tram tracks, broken elevators) in real time  during their trip and thus, let the others see where and what kind of problem they encountered. In a collaborative way, this would allow people to better choose the route they take to be on time and to improve their overall travel experience.

## Run it

To run it, clone this repository `git clone https://github.com/franckdeturchedura/DIL-Project.git`. Install `docker` and `docker-compose` if it's not already the case and, in the repository folder, execute `docker-compose up -d --build`.

To access all features, you will need a **Google API key**, which one you'll have to put in `instance/config.py`, in the variable `API_SECRET_KEY `.
Once done, make sure that you have activated the following APIs from your Google Cloud Console (where you have created the key).
+ [Get your key](https://developers.google.com/maps/documentation/javascript/get-api-key?)
+ [`Geocoding API`](https://developers.google.com/maps/documentation/geocoding/overview)
+ [`Places API`](https://developers.google.com/maps/documentation/places/web-service/overview)
+ [`Directions API`](https://developers.google.com/maps/documentation/directions/overview)
+ [`Maps Embed API`](https://developers.google.com/maps/documentation/embed/get-started)
+ [`Maps Javascript API`](https://developers.google.com/maps/documentation/javascript/overview)
+ [`Geolocation API`](https://developers.google.com/maps/documentation/geolocation/overview)

Once the containers (one for `mongodb` and one the the `flaskapp`) are running and you have finished the Gmaps APIs step, you can access the web application in your browser at `localhost:5000`.

## Technical considerations

+ Only the reports dated from less than 1 hour will be showed on the map.
+ Make sure the 2 containers are running.
+ If after signing in there is no map, please reload the page.
+ In the `/rating` page, we assumed rating a fake line M2. Its average grade is updated each time you submit a rate (the result is showed directly within this page).
+ The `/route` page only show all metro stations of Milan on the map. The feature is still under construction.
+ Do not use routes without loging in.
+ **IMPORTANT** : do not try to connect multiple users at the same time. We managed the connection with a unique boolean as a prototype.
+ Do not forget to **logout** at the end of your session (help button top right).
+ You can access the MongoDB database in its container from the terminal : `docker exec -it mongodb bash` ; `mongo` ; `use mongodb`
+ The 3 main collections in the DB are `User`, `Report` and `Line`.
+ Concerning the `Find my route` feature, please be enough precise in your requests. You should use either both autcompleted places for the creation of the report and to find your route or the two exactly same strings. If no route appears after submiting the form, it means it did not find/understand where you want to go/come from.
+ We only considered **metro station** for the `Find my route` feature.
+ **Remark** : when mixing addresses from the autocompletion and addresses fully written by hand, the exact location can vary a little and so the reports counter in the `Find a route` feature can be different from what you expect. Please do not mix autocompleted and 'hand written' strings for creating the report and then to find your route. In any case, the markers are on the map so you can easily see where are the reports.
+ As a future evolution of the `Find a route` feature, we would like to count the number of reports in an area around the given location, for each station on the route.
+ **Remark** : the GMAPS APIs do not provide any solution to easily get the names/locations of the stations given a certain route.


@Copyrights - All rights reserved
