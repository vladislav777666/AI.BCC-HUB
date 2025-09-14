<template>
  <div>
    <p>{{ preview.push_preview }}</p>
    <input v-model="edited" :placeholder="preview.push_preview" />
    <button @click="saveEdit">Save</button>
    <button @click="send">Send Push</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['client_code'],
  data() {
    return { preview: {}, edited: '' }
  },
  async mounted() {
    const resp = await axios.get(`/api/recommendations/${this.client_code}/preview`)
    this.preview = resp.data
    this.edited = this.preview.push_preview
  },
  methods: {
    async saveEdit() {
      await axios.patch(`/api/recommendations/${this.client_code}`, { push_text: this.edited })
    },
    async send() {
      await axios.post('/api/push/send', { client_code: this.client_code, channels: ['web'] })
    }
  }
}
</script>