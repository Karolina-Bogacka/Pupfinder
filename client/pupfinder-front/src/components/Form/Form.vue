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
      <input type="file" @change="uploadFile" multiple>
    </div>

    <div class="form-group">
      <button class="btn btn-success btn-block btn-lg">Upload</button>
    </div>
    <input class="button" type="submit" value="Submit">
</form>
  </div>
  </template>

<script>
export default {
name: "Form",
  data(){
  return {
    breed: '',
    chip_number: null,
    description: "",
    files: null
  }
  },
  methods: {
    uploadFile (event) {
        this.files = event.target.files
    },
   onSubmit() {
     if (this.breed === '' && this.description === '' && this.chip_number === null) {
       alert('Review is incomplete. Please fill out every field.')
       return
     } else {
       const formData = new FormData();
       if(this.files) {
         for (const i of Object.keys(this.files)) {
           formData.append('files', this.files[i])
         }
       }
          /*axios.post('http://localhost:3000/api/file-upload', formData, {
          }).then((res) => {
            console.log(res)
          })*/
       var dogReport = {
         breed: this.breed,
         chip_number: this.chip_number,
         description: this.description,
       }
       console.log(dogReport);
       this.$emit('report-submitted', dogReport)

       this.breed = ''
       this.chip_number = null
       this.description = ''
     }
   }
 }
}
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
