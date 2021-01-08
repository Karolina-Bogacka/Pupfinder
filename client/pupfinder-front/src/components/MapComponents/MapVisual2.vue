<template>
  <div style="height: 75vh; width: 50vw;">
    <div id="mapDiv">
    </div>
    <div class="ui right icon">
              <input
                type="text"
                placeholder="Enter the address of your search"
                v-model="address"
                ref="autocomplete"
              />
              <button @click="locatorButtonPressed"></button>
    </div>
    <button @click="pushRoute"></button>
  </div>
</template>
<script>

import {
  LMap,
  LIcon,
  LTileLayer,
  LMarker,
  LControlLayers,
  LTooltip,
  LPopup,
  LPolyline,
  LPolygon,
  LRectangle,
} from "@vue-leaflet/vue-leaflet";

import "leaflet/dist/leaflet.css";
import L from "leaflet";
import axios from 'axios'

const myCustomColour = '#247510'

const markerHtmlStyles = `
  background-color: ${myCustomColour};
  width: 3rem;
  height: 3rem;
  display: block;
  left: -1.5rem;
  top: -1.5rem;
  position: relative;
  border-radius: 3rem 3rem 0;
  transform: rotate(45deg);
  border: 1px solid #FFFFFF`

const icon = L.divIcon({
  className: "my-custom-pin",
  iconAnchor: [0, 24],
  labelAnchor: [-6, 0],
  popupAnchor: [0, -36],
  html: `<span style="${markerHtmlStyles}" />`
})

export default {
  components: {
    LMap,
    LIcon,
    LTileLayer,
    LMarker,
    LControlLayers,
    LTooltip,
    LPopup,
    LPolyline,
    LPolygon,
    LRectangle,
  },
  data() {
    return {
      zoom: 2,
      address: this.address,
     center: [52.237049, 21.017532]
    };
  },
  computed: {
    showComponent(){
      return true;
    }
  },
  methods: {
    setupLeafletMap() {
      console.log(this.config.globalProperties.$center);
      this.mapDiv = L.map("mapDiv").setView(this.config.globalProperties.$center, 13);
      L.tileLayer(
          "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
          {
            maxZoom: 20,
            attribution:
                '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
          }
      ).addTo(this.mapDiv);
      this.getDogsInArea();
      this.mapDiv.on("click", function (e) {
        app.config.globalProperties.$center = [e.latlng.lat.toFixed(5), e.latlng.lng.toFixed(5)];
        console.log(app.config.globalProperties.$center);
        }
      )
    },
    async locatorButtonPressed() {
      if (this.address === "" || !this.address) {
        navigator.geolocation.getCurrentPosition(
            position => {
              console.log(position.coords.latitude);
              console.log(position.coords.longitude);
              app.config.globalProperties.$center = [position.coords.latitude, position.coords.longitude];
              this.onCenter(app.config.globalProperties.$center);
            },
            error => {
              console.log(error.message);
            },
        )
      } else {
        app.config.globalProperties.$center = await this.getStreetAddressFrom(this.address);
        this.onCenter(app.config.globalProperties.$center);
      }
    },
    async getStreetAddressFrom(text) {
      try {
        var {data} = await axios.get(
            "https://api.geoapify.com/v1/geocode/search?", {params: {text: text, api_key:'5caffdbbde8941d48cddb778ded141f7', limit:'1' }});
        if (data.error_message) {
          console.log(data.error_message)
        } else {
          console.log(data.features[0].geometry.coordinates);
          return data.features[0].geometry.coordinates.reverse();
        }
      } catch (error) {
        console.log(error.message);
      }
    },
    async getFromCenter(latitude, longitude) {
      try {
        var {data} = await axios.get(
            "https://api.geoapify.com/v1/geocode/reverse?", {params: {lat:latitude, lon:longitude, api_key:'5caffdbbde8941d48cddb778ded141f7', limit:'1' }});
      } catch (error) {
        console.log(error.message);
      }
    },
    pushRoute: function () {
      this.$router.push({
        name: "ReportPuppy",
        params: {address: this.address, center: app.config.globalProperties.$center}
      });
    },
    placePupups(dogs) {
        this.dogsInArea = dogs;
        if (this.dogsInArea) {
        var i = 0;
        for (i; i < this.dogsInArea.length; i++) {
          var markerOptions = {
            title: this.dogsInArea[i][0]['dog_id'],
            icon: icon,
            clickable: true,
            draggable: false
          }
          var place = [this.dogsInArea[i][1].latitude, this.dogsInArea[i][1].longitude];
          var markerS = L.marker(place, markerOptions);
          markerS.addTo(this.mapDiv).on('mouseover', function (e) {
            this.dog_id = parseInt(e.target.options.title);
          });
      }}
    },
    async getDogsInArea() {
      try {
        console.log(app.config.globalProperties.$center);
        var response = await axios.get('http://localhost:8000/api/dogs/',
            {params: {latitude: app.config.globalProperties.$center[0],
                longitude: app.config.globalProperties.$center[1]}});
        this.placePupups(response.data.dogs);
      } catch (error) {
        console.log(error.message);
      }
    },
    onCenter(newCenter){
      console.log(this.mapDiv);
      this.mapDiv.panTo(newCenter);
      this.getDogsInArea();
    },
  },
  mounted(){
    if(typeof(this.$route.params.center)!="undefined"){
      app.config.globalProperties.$center = this.$route.params.center;
      this.address = this.$route.params.address;
    }
    /*if(typeof(app.config.globalProperties.$center) == "undefined") {
      app.config.globalProperties.$center = [52.237049, 21.017532];
  }*/
   this.setupLeafletMap();
   this.address = this.address || "";
   var dogsInArea = [];
   this.dog_id = 5;
   this.url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
   this.attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
   this.zoom=20;
  }
};
</script>

<style scoped>
#mapDiv {
 width: 80vw;
 height: 80vh;
}
button{
  width: 5vh;
  height: 5vh;
  color: darkolivegreen;
  background-color:green;
}
</style>
