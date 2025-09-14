import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
    .then(registration => {
        console.log('Service Worker зарегистрирован:', registration);

        return registration.pushManager.getSubscription()
            .then(subscription => {
                if (!subscription) {
                    return registration.pushManager.subscribe({
                        userVisibleOnly: true,
                        applicationServerKey: urlBase64ToUint8Array('<VAPID_PUBLIC_KEY>')
                    });
                } else {
                    return subscription;
                }
            });
    })
    .then(subscription => {
        fetch('/api/push/subscribe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(subscription)
        });
    });
}

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');
    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}