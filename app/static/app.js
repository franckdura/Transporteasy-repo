
//Set map options

myLatLng = { lat: 45.464664 , lng:9.188540 };
var options = {
    center: myLatLng,
    zoom: 13,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
};
//create Map
var map = new google.maps.Map(document.getElementById("googleMap"),options);
var transitLayer = new google.maps.TransitLayer();
transitLayer.setMap(map); //print the rest of the public transportation Network 

//create a direction service object to use the route method and get a answer to our request
var directionsService= new google.maps.DirectionsService();

// create a DirectionsRenderer object which we will use to display the route
var directionsDisplay = new google.maps.DirectionsRenderer();

//bind the directionsRender to the map
directionsDisplay.setMap(map);
let From = String("{{From}}");
let To = String("{{To}}");
print(From)
//function
function calcRoute(){
    //create request

    
    var request = {
        origin: "",
        destination: "",
        travelMode: google.maps.TravelMode.TRANSIT,//to get ONLY the public transportation in our request 
        transitOptions: google.maps.TransitOptions,
        //transitMode: google.maps.TransitMode.SUBWAY,
        unitSystem: google.maps.UnitSystem.IMPERIAL
    };
    var waypoints = [];
    //Pass the request to the route method
    directionsService.route(request, (result, status) => {
        if (status == google.maps.DirectionsStatus.OK){

            //get distance and time
            const output = document.querySelector('#output');
            var distance = result.routes[0].legs[0].distance.text; 
            var duration = result.routes[0].legs[0].duration.text;
            //output.innerHTML = "<div class='alert-info'> From: " + document.getElementById("from").value + ".<br/>To: "+ document.getElementById("to").value + ".<br/> Transit distance: "+distance+ ".<br/>Duration: "+duration+". </div>";
            output.innerHTML = "<div class='alert-info'> From: " + "" + ".<br/>To: " + "" + ".<br/> Transit distance: " + distance + ".<br/>Duration: " + duration + ". </div>";

            const detail = document.querySelector('#detail');
            //console.log(result) to see the result in the console
            var departure_station =  result.routes[0].legs[0].steps[1].transit.departure_stop.name;
            var arrival_station = result.routes[0].legs[0].steps[1].transit.arrival_stop.name;
            //detail.innerHTML = "<div class='alert-info-detail'></br>Departure station :"+departure_station+"</br> Arrival station :"+arrival_station;
            
            //display route
            directionsDisplay.setDirections(result);


            geocoder = new google.maps.Geocoder();
            



        }else{
            //delete route from map 
            directionsDisplay.setDirections({ routes: [] });

            //center map in spain 
            map.setCenter(myLatLng);

            //show error message 
            output.innerHTML="<div class='alert-danger'> Could not retrieve driving distance. </div>";
            }
    });
}

//create autocomplete object for all inputs (from et to), like that you begin to write something and you just have to click on the good one
var options = {
    types: ['(cities)']
}

var input1 = document.getElementById("from");
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById("to");
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);



