<template>
  <form @submit.prevent="submitTf">
    <input v-model="form.client_code" type="number" placeholder="Client Code" required />
    <input v-model="form.date" type="date" placeholder="Date" required />
    <input v-model="form.type" placeholder="Type" required />
    <input v-model="form.direction" placeholder="Direction" required />
    <input v-model="form.amount" type="number" placeholder="Amount" required />
    <input v-model="form.currency" placeholder="Currency" required />
    <button type="submit">Add Transfer</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: { client_code: 0, date: '', type: '', direction: '', amount: 0, currency: '' }
    }
  },
  methods: {
    async submitTf() {
      await axios.post('/api/upload/transfers', this.form)
      this.$emit('added')
    }
  }
}
</script>