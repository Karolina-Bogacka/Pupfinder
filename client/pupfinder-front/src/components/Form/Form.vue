<template>
  <div class="grid max-h-screen place-items-center">
<form  @submit.prevent="onSubmit" class="w-11/12 p-12 bg-white sm:w-8/12 md:w-1/2 lg:w-5/12">
  <h1 class="text-xl font-semibold">Hello there 👋, <span class="font-normal">please fill in the dog report</span></h1>
  <div class="flex justify-between gap-3">
  <span class="w-1/2">
    <label for="breed" class="block text-xs font-semibold text-gray-600 uppercase">Breed:</label>
    <input id="breed" placeholder="Unknown" v-model="breed" class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner"/>
    </span>
  <span class="w-1/2">
    <label for="chip_number" class="block text-xs font-semibold text-gray-600 uppercase">Chip number:</label>
    <input id="chip_number" placeholder="000000000000000" v-model="chip_number" class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner"/>
</span>
  </div>
    <label for="description" class="block mt-2 text-xs font-semibold text-gray-600 uppercase">Description:</label>
    <textarea id="description" placeholder="A very good dog" class="block w-full p-3 mt-2 text-gray-700 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner" v-model="description"></textarea><br/>
    <div class="form-group">
      <input type="file" class="bg-yellow-200 hover:bg-yellow-300 text-white font-bold py-3 px-6 rounded" @change="uploadFile"/>
    </div>
    <input type="submit" value="Submit" class="w-full py-3 mt-6 font-medium tracking-widest text-white uppercase bg-green shadow-lg focus:outline-none hover:bg-green-800 hover:shadow-none">
</form>
  </div>
  </template>

<script>
import axios from "axios";

export default {
name: "Form",
  props:{
    address: String,
    center: Float64Array
  },
  data(){
  return {
    breed: '',
    chip_number: null,
    description: "",
    file: null,
    address: "",
    center: null
  }
  },
  methods: {
    uploadFile (event) {
        this.file = event.target.files[0];
    },
   async onSubmit() {
     if (this.breed === '' && this.description === '' && this.chip_number === null) {
       alert('Review is incomplete. Please fill out every field.');
       return
     } else {
       let data = new FormData();
       if(this.file) {
         data.append('file', this.file);
       }
       let dogReport = {
         breed: this.breed,
         chip_number: this.chip_number,
         description: this.description,
       }
       if(data.entries().next().done){
         console.log("in");
         this.addReport(dogReport).then((response => {
             this.$router.push({name: "LocalMap", params: {address: this.address, center: this.center}})
           }));
       }else {
         this.sendImageToServer(data).then((response => {
           if(response && response!=="") {
             dogReport['url'] = response;
             console.log("in");
           }
           this.addReport(dogReport).then((response => {
             this.$router.push({name: "LocalMap", params: {address: this.address, center: this.center}})
           }));
         }));
       }

       this.breed = '';
       this.chip_number = null;
       this.description = '';
     }
   },
    async sendImageToServer(data){
      try {
        let response = await axios.post('http://localhost:8000/api/photo/', data,
            {headers:{
              'Content-Type': 'multipart/form-data'
            }});
        return response.data['file_name'];

      } catch (error) {
        console.log(error.message);
      }

    },
    async addReport(report){
      try{
        report['status'] = 'HOMELESS';
        report['location'] = this.center;
        let reportStringified = JSON.stringify(report);
        let {data} = axios.post('http://localhost:8000/api/dogs/', reportStringified, {headers: {
    'Content-Type': 'application/json'}}).then(function (response) {
            console.log(response);
          });
      } catch(error){
        console.log(error.message);
      }
    }
 },
  mounted() {
    this.center = this.$route.params.center;
    this.address = this.$route.params.address;
  }
}
</script>

<style scoped>
form {
  max-width: 600px;
}
</style>
