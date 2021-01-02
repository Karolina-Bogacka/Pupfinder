var mymap = L.map('mapid',{
  center: [52.22, 21.01],
  zoom: 15
});
var marker = null;
var pointNumber = 0;

function AddTiles(map) {
  L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      maxZoom: 20,
      attribution:
        '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
    }
  ).addTo(map);
}
AddTiles(mymap);
console.log("in");
