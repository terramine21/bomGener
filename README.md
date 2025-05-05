# bomGener
Подготавливает автоматическисозданный BOM(перечень элементов) под вставку в переченнь элементов схемы электрической принципиальной, подготовленной в формате .docx

### Authentication (`/auth`)
| Метод | Эндпоинт    | Описание          |
|--------|-------------|----------------------|
| POST   | `/register` | Резистрация нового пользователя    |
| POST   | `/login`    | Получение JWT токена |

Все пользователи получают доступ к загруженным листам

### BOM Operations (`/BOM`)
| Метод | Эндпоинт                      | Описание                     |
|--------|-------------------------------|---------------------------------|
| POST   | `/upload/new`                 | Загрузить новый лист            |
| GET    | `/upload/list`                | Отобразить все загруженные листы |
| GET    | `/upload/{upload_id}`         | Отобразить позиции в листе |
| GET    | `/download/{upload_id}`       | Скачать excel файл         |
| DELETE | `/upload/{upload_id}`         | Удалить лист               |
| PATCH  | `/upload/{upload_id}/record/{record_id}` | Обновить параметры позиции |

### Клонирование репозитория и запуск

```
git clone https://github.com/your-repo/bom-management.git
cd bom-management

pip install -r requirements.txt

echo DB_URL=sqlite:///bom.db > .env
echo SECRET_KEY=mega-secret-key-here >> .env
echo ALGORITHM=HS256 >> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env

uvicorn main:app
```
### Отчет pylint 8.58/10
Из-за невозможности pylit проигнорировать папки виртуального окружения и кэша, была создана копия проекта внутри проекта с названием "bomGener_isolated"