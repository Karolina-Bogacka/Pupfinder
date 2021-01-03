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

    <Form v-if="showComponent" @report-submitted="addReport"></Form>
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
import Form from "../Form/Form.vue";

var locCenter = locCenter || [52.237049, 21.017532];
export default {
  components: {
    Form,
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
     center: locCenter,
    };
  },
  computed: {
    centerPlace(){
      return locCenter;
    },
    showComponent(){
      return false;
    }
  },
  methods: {
    log(a) {
      console.log(a);
    },
    onCenter(newCenter){
      console.log(this.mapDiv);
      this.mapDiv.panTo(newCenter);
    },
    setupLeafletMap() {
      console.log(this.$center);
      this.mapDiv = L.map("mapDiv").setView(this.$center, 13);
      L.tileLayer(
          "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
          {
            maxZoom: 20,
            attribution:
                '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
          }
      ).addTo(this.mapDiv);
    },
    onEachFeature(feature, layer) {
      if (feature.properties && feature.properties.name) {
        layer.bindPopup(feature.properties.name);
    layer.on('mouseover', () => { layer.openPopup(); });
        layer.on('mouseout', () => { layer.closePopup(); });
      }
   },
    async locatorButtonPressed() {
      if (this.address === "" || !this.address) {
        navigator.geolocation.getCurrentPosition(
            position => {
              console.log(position.coords.latitude);
              console.log(position.coords.longitude);
              locCenter = [position.coords.latitude, position.coords.longitude];
              this.onCenter(locCenter);
            },
            error => {
              console.log(error.message);
            },
        )
      } else {
        locCenter = await this.getStreetAddressFrom(this.address);
        this.onCenter(locCenter);
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
    async addReport(report){
      try{
        report['status'] = 'HOMELESS';
        report['location'] = locCenter;
        var reportStringified = JSON.stringify(report);
        console.log(reportStringified);
        var {data} = axios.post('http://localhost:8000/api/dogs/', reportStringified, {headers: {
    'Content-Type': 'application/json'}}).then(function (response) {
            console.log(response);
          });
      } catch(error){
        console.log(error.message);
      }
    },
    async getDogsInArea(){
      try{
        var {data} = axios.get('http://localhost:8000/api/dogs/',
            {params: {latitude: locCenter[0], longitude: locCenter[1]}}).then(function (response) {
            console.log(response.data.dogs);
            return response.data.dogs;
          });
      }catch(error){
        console.log(error.message);
      }
    },
    async placePupups(){
      this.dogsInArea = await getDogsInArea();
      for(i = 0; i < this.dogsInArea.length; i++){
        var markerOptions = {
            title: this.dogsInArea[i]['dog_id'],
            clickable: true,
            draggable: false
        }
        marker = L.marker(e.latlng, markerOptions);
        console.log(marker);
        marker.addTo(map).on('mouseover', function(e) {
        console.log(e);
        if(e.originalEvent.ctrlKey){
          deletePoint(e.target.options.title, map);
        }
    });
      }
    }
  },
  mounted(){
   this.setupLeafletMap();
   locCenter = locCenter || [52.237049, 21.017532];
   this.address = this.address || "";
   this.getDogsInArea();
   var dogsInArea = [];
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
