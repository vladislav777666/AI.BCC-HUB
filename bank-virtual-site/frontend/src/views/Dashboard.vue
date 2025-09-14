<template>
  <div>
    <ClientForm @added="refresh" />
    <ClientList />
    <BatchRunner />
  </div>
</template>

<script>
import ClientForm from '../components/ClientForm.vue'
import ClientList from '../components/ClientList.vue'
import BatchRunner from '../components/BatchRunner.vue'

export default {
  components: { ClientForm, ClientList, BatchRunner },
  methods: {
    refresh() {
    }
  }
}
</script>