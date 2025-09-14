<template>
  <div>
    <TransactionForm @added="refresh" />
    <TransferForm @added="refresh" />
    <PushPreview :client_code="$route.params.id" />
  </div>
</template>

<script>
import TransactionForm from '../components/TransactionForm.vue'
import TransferForm from '../components/TransferForm.vue'
import PushPreview from '../components/PushPreview.vue'

export default {
  components: { TransactionForm, TransferForm, PushPreview },
  methods: {
    refresh() {
    }
  }
}
</script>