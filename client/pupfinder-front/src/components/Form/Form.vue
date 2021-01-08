<template>
  <div>
<form class="report-dog-form" @submit.prevent="onSubmit">
    <h3>Report a homeless dog in the neighborhood</h3>
    <label for="breed">Breed:</label>
    <input id="breed" v-model="breed"/><br/>

    <label for="chip_number">Chip number:</label>
    <input id="chip_number" v-model="chip_number"/><br/>

    <label for="description">Description:</label>
    <textarea id="description" v-model="description"></textarea><br/>
    <div class="form-group">
      <input type="file" @change="uploadFile">
    </div>
    <input class="button" type="submit" value="Submit">
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
       var data = new FormData();
       if(this.file) {
         data.append('file', this.file);
       }
       var dogReport = {
         breed: this.breed,
         chip_number: this.chip_number,
         description: this.description,
       }
       console.log(dogReport);
       this.sendImageToServer(data).then((response =>{
         dogReport['url'] = response;
         this.addReport(dogReport).then((response => {
           this.$router.push({name: "LocalMap", params: {address: this.address, center: this.center}})}));
       }));

       this.breed = '';
       this.chip_number = null;
       this.description = '';
     }
   },
    async sendImageToServer(data){
      try {
        console.log(data);
        var response = await axios.post('http://localhost:8000/api/photo-upload/', data,
            {headers:{
              'Content-Type': 'multipart/form-data'
            }});
        console.log(response.data['file_name']);
        return response.data['file_name'];

      } catch (error) {
        console.log(error.message);
      }

    },
    async addReport(report){
      try{
        report['status'] = 'HOMELESS';
        report['location'] = this.center;
        var reportStringified = JSON.stringify(report);
        console.log(reportStringified);
        var {data} = axios.post('http://localhost:8000/api/dogs/', reportStringified, {headers: {
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
    console.log(this.center);
  }
}
</script>

<style scoped>
form {
  max-width: 600px;
  background-color: orange;
}
</style>
