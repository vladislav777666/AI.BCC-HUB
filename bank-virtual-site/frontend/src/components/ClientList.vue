<template>
  <ul>
    <li v-for="client in clients" :key="client.client_code">
      {{ client.name }} - <router-link :to="`/client/${client.client_code}`">Detail</router-link>
    </li>
  </ul>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return { clients: [] }
  },
  async mounted() {
    const resp = await axios.get('/api/clients')  // Add endpoint if needed
    this.clients = resp.data
  }
}
</script>