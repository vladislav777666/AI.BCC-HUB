<template>
  <form @submit.prevent="submitTx">
    <input v-model="form.client_code" type="number" placeholder="Client Code" required />
    <input v-model="form.date" type="date" placeholder="Date" required />
    <input v-model="form.category" placeholder="Category" required />
    <input v-model="form.amount" type="number" placeholder="Amount" required />
    <input v-model="form.currency" placeholder="Currency" required />
    <button type="submit">Add Transaction</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: { client_code: 0, date: '', category: '', amount: 0, currency: '' }
    }
  },
  methods: {
    async submitTx() {
      await axios.post('/api/upload/transactions', this.form)
      this.$emit('added')
    }
  }
}
</script>