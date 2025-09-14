<template>
  <form @submit.prevent="submitClient">
    <input v-model="form.client_code" type="number" placeholder="Client Code" required />
    <input v-model="form.name" placeholder="Name" required />
    <select v-model="form.status" required>
      <option>Студент</option>
      <option>Зарплатный клиент</option>
      <option>Премиальный клиент</option>
      <option>Стандартный клиент</option>
    </select>
    <input v-model="form.age" type="number" placeholder="Age" required />
    <input v-model="form.city" placeholder="City" required />
    <input v-model="form.avg_monthly_balance_KZT" type="number" placeholder="Avg Balance KZT" required />
    <button type="submit">Add Client</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: { client_code: 0, name: '', status: '', age: 0, city: '', avg_monthly_balance_KZT: 0 }
    }
  },
  methods: {
    async submitClient() {
      await axios.post('/api/upload/profiles', this.form)
      this.$emit('added')
    }
  }
}
</script>