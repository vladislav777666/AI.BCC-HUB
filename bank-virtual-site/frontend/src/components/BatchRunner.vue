<template>
  <button @click="runBatch">Run Batch</button>
  <a href="/api/recommendations/csv">Export CSV</a>
</template>

<script>
import axios from 'axios'

export default {
  methods: {
    async runBatch() {
      await axios.post('/api/recommendations/run')
    }
  }
}
</script>