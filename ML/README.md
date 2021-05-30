#### Данные: https://www.kaggle.com/rashikrahmanpritom/heart-attack-analysis-prediction-dataset

#### Задача: Предрасположенность к сердечным заболеваниям

#### Признаки:
* age - возраст
* sex - пол
* cp - тип боли в груди
* exng - стенокардия, вызванная физической нагрузкой
* trtbps - артериальное давление в состоянии покоя (в мм рт. ст.)
* thalachh - достигнутая максимальная частота пульса


#### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/AnnaSmelova/Machine_learning_in_business_course_project.git
$ cd Machine_learning_in_business_course_project
$ docker build -t flask_app:v0.1 flask_app/
```

#### Запускаем контейнер
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models flask_app:v0.1
```

#### Переходим на localhost:8181
