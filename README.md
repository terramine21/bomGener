# bomGener
Подготавливает автоматическисозданный BOM(перечень элементов) под вставку в переченнь элементов схемы электрической принципиальной 

### Authentication (`/auth`)
| Method | Endpoint    | Description          |
|--------|-------------|----------------------|
| POST   | `/register` | Register new user    |
| POST   | `/login`    | Login and get JWT token |

### BOM Operations (`/BOM`)
| Method | Endpoint                      | Description                     |
|--------|-------------------------------|---------------------------------|
| POST   | `/upload/new`                 | Загрузить новый лист            |
| GET    | `/upload/list`                | Отобразить все загруженные листы |
| GET    | `/upload/{upload_id}`         | Отобразить позиции в листе |
| GET    | `/download/{upload_id}`       | Скачать excel файл         |
| DELETE | `/upload/{upload_id}`         | Удалить лист               |
| PATCH  | `/upload/{upload_id}/record/{record_id}` | Обновить параметры позиции |
