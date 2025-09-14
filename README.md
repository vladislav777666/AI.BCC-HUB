# AI.BCC-HUB
Decentranhit 4.0

Проект "Идеальный виртуальный сайт банка" реализован как full-stack приложение с frontend на Vue 3 для админ-интерфейса тестирования и backend на FastAPI для обработки данных, интеграции модели и генерации пушей. Архитектура следует ТЗ: микросервисы (API, Model Service), DB (Postgres), очередь (Redis + Celery), контейнеризация (Docker). Push-подсистема интегрирована с Web Push (VAPID) для отправки уведомлений на телефон/браузер при вводе тестовых данных и генерации рекомендаций от ИИ (нейронки model.pkl). Когда данные вводятся во фронт (формы или CSV), фичи извлекаются, подаются в модель для ранжирования/пуша, и отправляется push через VAPID. Подписки хранятся в DB. Fallback - rule-based. Все работает: batch, export CSV, monitoring.

bank-virtual-site/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── uploads.py
│   │   │   ├── recommendations.py
│   │   │   ├── push.py
│   │   ├── models/
│   │   │   ├── features.py
│   │   │   ├── rank.py
│   │   ├── services/
│   │   │   ├── feature_extractor.py
│   │   │   ├── rules_engine.py
│   │   │   ├── text_generator.py
│   │   │   ├── tov_validator.py
│   │   │   ├── decision_enforcer.py
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   ├── session.py
│   │   ├── tasks/
│   │   │   ├── push_tasks.py
│   │   ├── utils/
│   │   │   ├── logging.py
│   │   │   ├── metrics.py
│   ├── migrations/
│   │   ├── env.py
│   │   ├── versions/
│   ├── tests/
│   │   ├── test_feature_extractor.py
│   │   ├── test_tov_validator.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── celery_worker.py
├── model-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── rank.py
│   │   ├── services/
│   │   │   ├── model_loader.py
│   │   │   ├── preprocessor.py
│   │   │   ├── explainer.py
│   ├── tests/
│   │   └── test_model.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   │   ├── sw.js
│   │   └── icon.png
│   ├── src/
│   │   ├── components/
│   │   │   ├── ClientForm.vue
│   │   │   ├── TransactionForm.vue
│   │   │   ├── TransferForm.vue
│   │   │   ├── ClientList.vue
│   │   │   ├── PushPreview.vue
│   │   │   ├── BatchRunner.vue
│   │   ├── views/
│   │   │   ├── Dashboard.vue
│   │   │   ├── ClientDetail.vue
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── router.js
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
├── data/
│   ├── generate_test_data.py
│   ├── clients.csv
│   ├── transactions.csv
│   └── transfers.csv
├── docs/
│   ├── openapi.yaml
│   ├── deployment.md
│   ├── runbooks.md
│   └── security.md
├── docker/
│   ├── docker-compose.yml
│   └── k8s/
├── .github/workflows/ci-cd.yaml
├── README.md
└── model.pkl