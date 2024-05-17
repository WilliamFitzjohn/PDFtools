<template>
  <div>
    <h1>Combine PDFs</h1>
    <form @submit.prevent="combinePDFs">
      <div v-for="(file, index) in files" :key="index">
        <input type="file" accept="application/pdf" @change="handleFileChange($event, index)" />
      </div>
      <button type="button" @click="addFile">Add another file</button>
      <button type="submit">Combine</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      files: [null]
    }
  },
  methods: {
    addFile() {
      this.files.push(null)
    },
    handleFileChange(event, index) {
      this.files[index] = event.target.files[0]
    },
    async combinePDFs() {
      const formData = new FormData()
      this.files.forEach((file, index) => {
        formData.append(`file${index + 1}`, file)
      })

      try {
        const response = await axios.post('/api/combine', formData)
        console.log(response.data)
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>