<template>
  <div class="h-screen w-screen flex">
	<!-- container -->

	 <div class="flex-1 flex overflow-hidden">
    <!-- Scrollable container -->
    <div class="flex-1 overflow-y-scroll">
    <div v-for="dog in dogsInArea" v-bind:key="dog.dog_id">
      <button v-on:click="showPup(dog)" :value="dog.breed">{{dog['id']}}</button>
    </div>
  </div>
     </div>
  <div class="MapContainer" >
    <fieldset>
    <div>
    <l-map style="min-height: 70vh" ref="map"  @ready="onReady" @locationfound="onLocationFound"  @click="changeCenter" :zoom="zoom" :center="center">
      <LTileLayer :url="url"></LTileLayer>
            <LMarker v-for="dog in dogsInArea" @mouseover="$event.target.openPopup()" :key="dog.dog_id" :lat-lng="dog.place" :options="dog.options" :id="dog.id" v-on:click="showPup(dog)" :ref="`markers${dog.id}`">
              <LPopup :visible=dog.visible>
                <img :src="returnURL(dog)"/>
                {{dog.breed}} Nr {{dog.id}}
                {{dog.chip_number}}
                {{dog.description}}
              </LPopup>
            </LMarker>
    </l-map>

  </div>
    <div class="ui right icon">
              <input
                type="text"
                placeholder="Enter the address of your search"
                v-model="address"
                ref="autocomplete"
                @keypress.enter="locatorButtonPressed"
                class="input border border-gray-400 appearance-none rounded w-full px-3 py-3 pt-5 pb-2 focus focus:border-indigo-600 focus:outline-none active:outline-none active:border-indigo-600"
              />
              <button @click="locatorButtonPressed" class="bg-blue-500 text-white font-bold rounded">Go to location</button>
    </div>
    <button @click="pushRoute" class="bg-blue-500 text-white font-bold rounded">Report a lost pupper</button>
    </fieldset>
  </div>
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
      zoom: 15,
      address: this.address,
      center: [52.237049, 21.017532],
      dogsInArea: {},
      markers: []
    };
  },
  computed: {
    showComponent(){
      return true;
    }
  },
  methods: {
    onReady (mapObject) {
      mapObject.locate();
    },
    returnURL(dog){
      return dog.url;
    },
      onLocationFound(location){
      console.log(location);
    },
    changeCenter(e){
      console.log(e);
      if(typeof(e.latlng)!=="undefined") {
        this.center = [e.latlng.lat.toFixed(5), e.latlng.lng.toFixed(5)];
        this.getDogsInArea([e.latlng.lat.toFixed(5), e.latlng.lng.toFixed(5)]);
      }
      },
    showPup(dog){
      this.dog_id = parseInt(dog.id);
      let index = `markers${dog.id}`;
      console.log(this.$refs[index].leafletObject.openPopup());
      this.$refs[index].leafletObject.openPopup();
      this.center = dog.place;
    },
    async locatorButtonPressed() {
      if (this.address === "" || !this.address) {
        navigator.geolocation.getCurrentPosition(
            position => {
              this.center = [position.coords.latitude, position.coords.longitude];
              this.onCenter(this.center);
            },
            error => {
              console.log(error.message);
            },
        )
      } else {
        this.center = await this.getStreetAddressFrom(this.address);
        this.onCenter(this.center);
      }
    },
    async getStreetAddressFrom(text) {
      try {
        let {data} = await axios.get(
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
        let {data} = await axios.get(
            "https://api.geoapify.com/v1/geocode/reverse?", {params: {lat:latitude, lon:longitude, api_key:'5caffdbbde8941d48cddb778ded141f7', limit:'1' }});
      } catch (error) {
        console.log(error.message);
      }
    },
    pushRoute: function () {
      this.$router.push({
        name: "ReportPuppy",
        params: {address: this.address, center: this.center}
      });
    },
    placePupups(dogs) {
        if (dogs) {
          console.log(dogs);
        var i = 0;
        for (i; i < dogs.length; i++) {
          let markerOptions = {
            title: dogs[i][0]['dog_id'],
            icon: icon,
            clickable: true,
            draggable: false
          }
          let id = dogs[i][0]['dog_id'];
          let place = [dogs[i][1].latitude, dogs[i][1].longitude];
          let url = "http://localhost:8000/api/dogs/"+id.toString()+"/photo/"
          let description = dogs[i][0]['description'];
          let breed = dogs[i][0]['breed'];
          let chip_number = dogs[i][0]['chip_number'];
          this.dogsInArea[dogs[i][0]['dog_id']] = {options: markerOptions, place: place, id:id, url:url,
            description: description, breed: breed, chip_number:chip_number, visible:true};
      }}
    },
    async getDogsInArea(center) {
      try {
        let response = await axios.get('http://localhost:8000/api/dogs/',
            {params: {latitude: center[0],
                longitude: center[1]}});
        this.placePupups(response.data.dogs);
      } catch (error) {
        console.log(error.message);
      }
    },
    onCenter(newCenter){
      this.center = newCenter;
      this.getDogsInArea(newCenter);
    },
  },
  created(){
    if(typeof(this.$route.params.center) != "undefined"){
      this.center = this.$route.params.center;
      this.address = this.$route.params.address;
    }
   this.getDogsInArea(this.center);
   this.address = this.address || "";
   this.dog_id = 5;
   this.url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
   this.attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
   this.zoom=20;
  }
};
</script>

<style scoped>
button{
  height: 5vh;
  background-color:green;
}
</style>
